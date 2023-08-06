# Copyright 2021 Anthony Mugendi
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import re
import random
import os
import sys
import subprocess
import psutil

from getpass import getpass
from flask import abort, Flask, jsonify, request
from Utils import timeExec, sudo_process, is_absolute_url, pprint
from waitress import serve
from fastcore.utils import Path


script = os.path.realpath(__file__)
# Home Dir
home_dir = os.path.dirname(script)
ports_file = os.path.join( home_dir, "config","torrc");



def get_ports(file):

    with open(file, 'r') as file:
        data = file.read()
        
        SOCKPorts=[]
        ControlPorts=[]
        
        pattern1 = re.compile(r'SOCKSPort\s+[\.:0-9]+:([0-9]+)')
        pattern2 = re.compile(r'ControlPort\s+([0-9]+)')
        
        for line in re.split("[\r\n]",data):    
            arr = pattern1.split(line)
            
            if len(arr)==3:        
                SOCKPorts.append(int(arr[1]))
                
        for line in re.split("[\r\n]",data):  
            arr = pattern2.split(line)
            
            if len(arr)==3:        
                ControlPorts.append(int(arr[1]))
                
        
        return {'SOCKPorts':SOCKPorts, 'ControlPorts':ControlPorts}

def make_torrc_file(instances_count=4):
    ports = []
    control_ports = []
    starting_port = 9060

    while len(ports) < instances_count:
        
        control_port = starting_port+1   
        
        # if  is_free_port(starting_port) and  is_free_port(control_port) :
        
        ports.append(f"SOCKSPort 0.0.0.0:{starting_port}")
        control_ports.append(f"ControlPort {control_port}")
        
        starting_port += 10
        
        
    # Use fastutils to create and write ports file
    Path(ports_file).mk_write('{}\n{}'.format( '\n'.join(ports) , '\n'.join(control_ports)) )


ports = get_ports(ports_file)
port_usage = {}
max_requests = 10
control_password=''

tor_status={}
tor_process= None

  
 
def is_free_port(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def reset_pass(port, password):
    
    global home_dir
    
    print('Resetting IP for {}...'.format(port))
    
    # make command
    cmd = '{} "{}" --port {} --password "{}"' .format(sys.executable, os.path.join(home_dir, 'reset-ip.py'), port, password)

    # execute command
    os.system(cmd)    

def random_proxy():
    global ports
    global control_password
    global max_requests
    
    random_port = random.choice(ports['SOCKPorts'])
    port_index = ports['SOCKPorts'].index(random_port)
    
    
    # if control port password and value is zero, reload and reset port
    if control_password != None and port_usage.get(random_port) != None and port_usage[random_port] == 0 :   
        port_usage[random_port] =  max_requests
        reset_pass( ports['ControlPorts'][port_index] , control_password)
    
    if port_usage.get(random_port)==None:
        port_usage[random_port] =  max_requests
    else:
        port_usage[random_port] = port_usage[random_port] - 1        
    
    # print(port_usage, random_port)
    
    # make Proxy URL
    return 'socks5://127.0.0.1:{}'.format(random_port), random_port
        
def get_tor_session(proxy):
    
    # print("proxy", proxy)
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  proxy,
                       'https': proxy}
    return session

def fetch_url(url):
    # get random proxy
    proxy, port = random_proxy()
    
    session = get_tor_session(proxy)    
    
    resp = session.get(url).text.strip()
    
    return resp, proxy

def running_tors():
    # lsof -i -P -n | grep tor
    cmd = 'lsof -i -P -n'
    ls = cmd.split()
    # print(cmd)
    
    process = subprocess.run(ls, stdout=subprocess.PIPE)    
    process = subprocess.run(['grep','tor'], stdout=subprocess.PIPE, input=process.stdout)
    resp_str = process.stdout.decode('utf-8')
    
    running = {
        'process':{
            'pid':None,
        }  ,      
        'instances':{
            'count' : 0,
            'ports':[],
            'control_ports':[]
        }
        
    }
    
    
    pattern1 = re.compile(r'^tor\s+([0-9]+).+?\(LISTEN\)')
    p = None
    
    for line in re.split("[\r\n]",resp_str):
        arr = pattern1.split(line)
                
        if len(arr) == 3:  
        
            p = psutil.Process( int(arr[1]) )        
            p_dict = p.as_dict()
            
            # running['terminate']=p.terminate
            
            
            running['process'] = {                
                'name' : p_dict['name'],
                'status' : p_dict['status'],
                'pid' : p_dict['pid'],
                'memory_percent' : p_dict['memory_percent'] * 100,
                
                'cwd' : p_dict['cwd'],
                'cpu_num' : p_dict['cpu_num'],
                'create_time' : p_dict['create_time']
            }
            
            # pprint(p_dict)
            
            for conn in p_dict['connections']:            
                if conn.status=='LISTEN':
                    if(conn.laddr.ip=='0.0.0.0'):
                        running['instances']['ports'].append(conn.laddr.port)
                        running['instances']['count'] += 1
                    else:
                        running['instances']['control_ports'].append(conn.laddr.port)
                        
                    
            break
                

    return running, p

def start_tor(requests, password, instances=4):
    
    global max_requests
    global control_password
    global tor_status
    global tor_process
    
    max_requests = requests
    control_password = password
    
    # mAKE tORRC fILE
    make_torrc_file(instances)
    
    # start tor instances...
    cmd = '{} "{}" &'.format(sys.executable, os.path.join( home_dir, "start-tor.py"))
    # cmd = 'sudo tor -f "{}" &'.format(ports_file)
    
    os.system(cmd)
    
    print('''  
   ┌───────────────────────────────────┐                      
   └──┐  ┌─────────────────────────────┘
      │  │   ______________________    
      │  │  / _ \_  __ \_  __ \__  \   
      │  │ ( (_) )  | \/|  | \// __ \__
      │  │  \___/|__|   |__|  (_____  /
      └──┘                          \/ 
   ┌                                   ┐
   │  Manage TOR Proxies like a Boss!  │
   └                                   ┘ ''')
    
    print("    > Started {} TOR instances.".format(len(ports['SOCKPorts'])))
    
    
  
def stop_tor():
    print("Stopping TOR...")
    # global tor_process    
    tor_status , tor_process = running_tors()
    # 
    if tor_process:    
        # print(tor_status)
        print("Stopping {} with PID:{}".format(tor_status['process']['name'], tor_status['process']['pid']))
        # print(tor_process)
        tor_process.terminate()



def start():
    # Args needed
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(description='Run Multiple TOR processes exposed via a REST API')
    
    # Add an argument   
    parser.add_argument('--control-pass', type=str, required=False, default=None, help='TOR Control Password.')
    parser.add_argument('--server', type=int, required=False, default=6930, help="REST API Port. Default=6930")
    parser.add_argument('--instances', type=int, required=False, default=4, help="TOR Instances to start. Default=4")
    parser.add_argument('--refresh-after', type=int, required=False, default=50, help="API Calls after which TOR Passwords refresh. Default 50")    
    parser.add_argument('--stop', action="store_true", help="Stop All Tor Processes")

    # Parse the argument
    args = parser.parse_args()
    
    # If stop
    if args.stop:
        stop_tor()
            
    else:    
        print(args)        
        # APP 
        app = Flask(__name__)
        
        @app.route("/", methods=["GET"])
        def indexDir():
            
            # start timing operation
            timeExec('fetchPage')  
            
            if request.json and 'url' in request.json:
                url = request.json['url']
                if is_absolute_url(url) == False:
                    abort(440)   
            else:
                abort(440)    
                
            
            resp, port = fetch_url(url)
            
            response = {
                'meta': {
                    'took' : timeExec('fetchPage'),
                    'proxy': port
                },
                'response': resp
            }
                
            return jsonify(response), 200
        
        # start TOR      
        start_tor(args.refresh_after, args.control_pass, args.instances)
        
        print('    > Starting server on port {} ' .format(args.server) ) 
               
        # app.run()
        serve(app, host="0.0.0.0", port=args.server)
    
    

if __name__ == "__main__":
    
    start()
    
    