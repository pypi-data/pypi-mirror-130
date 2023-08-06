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

from collections import Counter
from getpass import getpass
from flask import abort, Flask, jsonify, request
from Utils import timeExec, sudo_process, is_absolute_url, pprint, logger
from waitress import serve
from fastcore.utils import Path


script = os.path.realpath(__file__)
# Home Dir
home_dir = os.path.dirname(script)
ports_file = os.path.join( home_dir, "config","torrc")


class args:
    verbose = True

ARGS = args()

max_requests = 10
ports = []
port_usage = {}

def get_ports():

    global ports_file
    global max_requests
    global port_usage
    
    with open(ports_file, 'r') as file:
        data = file.read()
        
        SOCKPorts=[]
        ControlPorts=[]
        
        pattern1 = re.compile(r'SOCKSPort\s+[\.:0-9]+:([0-9]+)')
        pattern2 = re.compile(r'ControlPort\s+([0-9]+)')
        
        for line in re.split("[\r\n]",data):    
            arr = pattern1.split(line)
            
            if len(arr)==3:   
                port = int(arr[1])     
                SOCKPorts.append(port)
                port_usage[port]= max_requests
                
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



def cycle_proxy():
    global ports
    global control_password
    global max_requests
    
    # Get the least used port
    c=Counter(port_usage)
    l = c.most_common()
    
    least_used_port = l[0][0]
    port_index = ports['SOCKPorts'].index(least_used_port)    
    
    # if control port password and value is zero, reload and reset port
    if control_password != None and port_usage.get(least_used_port) != None and port_usage[least_used_port] == 0 :   
        port_usage[least_used_port] =  max_requests
        reset_pass( ports['ControlPorts'][port_index] , control_password)
    
    if port_usage.get(least_used_port)==None:
        port_usage[least_used_port] =  max_requests
    else:
        port_usage[least_used_port] = port_usage[least_used_port] - 1        
    
    # print(port_usage, least_used_port)
    
    # make Proxy URL
    return 'socks5://127.0.0.1:{}'.format(least_used_port), least_used_port, port_usage[least_used_port]

     
def get_tor_session(proxy):
    
    # print("proxy", proxy)
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  proxy,
                       'https': proxy}
    return session


def debug(level, *args):
    
    
    if ARGS.verbose:
        
        print_str = '{}'.format(' '.join([str(i) for i in args]))        
        
        if level=='info':
            log = logger.info
        elif level=='warning':
            log = logger.warning
        elif level=='error':
            log = logger.error
        elif level=='critical':
            log = logger.critical
        else:
            log = logger.debug
            
        log(print_str)


def fetch_url(url):
    
    # get random proxy
    proxy, port, remaining = cycle_proxy()
    
    print(proxy, port, remaining)
    
    session = get_tor_session(proxy)    
    
    resp = session.get(url).text.strip()
    
    return resp, port, remaining

def grep_pids(pc_name):
    process = subprocess.run(['lsof','-i', '-P', '-n'], stdout=subprocess.PIPE)    
    process = subprocess.run(['grep', "^{}\s".format(pc_name)], stdout=subprocess.PIPE, input=process.stdout)
    resp_str = process.stdout.decode('utf-8')
    
    pattern1 = re.compile(r'^{}\s+([0-9]+)'.format(pc_name))
    
    pids = []
    
    for line in re.split("[\r\n]",resp_str):
        arr = pattern1.split(line)
        
        if len(arr) == 3 :
            pid = int(arr[1])            
            if pid not in pids:
                pids.append( pid )
            
    
    return pids

def running_tors():
    
    pids = grep_pids('tor')


    
    running = {
        'processes':[],      
        'instances':{
            'count' : 0,
            'ports':[],
            'control_ports':[]
        }
        
    }
    ps = []
    
    for pid in pids:
            
        p = psutil.Process( pid )        
        p_dict = p.as_dict()
        
        ps.append(p)
        
        # running['terminate']=p.terminate       
        
        running['processes'].append( {                
            'name' : p_dict['name'],
            'status' : p_dict['status'],
            'pid' : p_dict['pid'],
            'memory_percent' : p_dict['memory_percent'] * 100,
            
            'cwd' : p_dict['cwd'],
            'cpu_num' : p_dict['cpu_num'],
            'create_time' : p_dict['create_time']
        })
        
        # pprint(p_dict)
        
        for conn in p_dict['connections']:            
            if conn.status=='LISTEN':
                if(conn.laddr.ip=='0.0.0.0'):
                    running['instances']['ports'].append(conn.laddr.port)
                    running['instances']['count'] += 1
                else:
                    running['instances']['control_ports'].append(conn.laddr.port)
                    
    
    # print(running)

    return running, ps

def start_tor(requests, password, instances=4):
    
    global max_requests
    global control_password
    global tor_status
    global tor_process
    global ports
    
    max_requests = requests
    control_password = password
    
    # mAKE tORRC fILE
    make_torrc_file(instances)
    
    # start tor instances...
    cmd = '{} "{}" &'.format(sys.executable, os.path.join( home_dir, "start-tor.py"))
    # cmd = 'sudo tor -f "{}" &'.format(ports_file)
    
    os.system(cmd)
    
    # get ports
    if len(ports) == 0:
        ports = get_ports()

    print(''',---------.    ,-----.    .-------.    ,---.    ,---.   ____    ,---.   .--. 
\          \ .'  .-,  '.  |  _ _   \   |    \  /    | .'  __ `. |    \  |  | 
 `--.  ,---'/ ,-.|  \ _ \ | ( ' )  |   |  ,  \/  ,  |/   '  \  \|  ,  \ |  | 
    |   \  ;  \  '_ /  | :|(_ o _) /   |  |\_   /|  ||___|  /  ||  |\_ \|  | 
    :_ _:  |  _`,/ \ _/  || (_,_).' __ |  _( )_/ |  |   _.-`   ||  _( )_\  | 
    (_I_)  : (  '\_/ \   ;|  |\ \  |  || (_ o _) |  |.'   _    || (_ o _)  | 
   (_(=)_)  \ `"/  \  ) / |  | \ `'   /|  (_,_)  |  ||  _( )_  ||  (_,_)\  | 
    (_I_)    '. \_/``".'  |  |  \    / |  |      |  |\ (_ o _) /|  |    |  | 
    '---'      '-----'    ''-'   `'-'  '--'      '--' '.(_,_).' '--'    '--' 
    ┌                                   ┐
    │  Manage TOR Proxies like a Boss!  │
    └                                   ┘
''')
    
    logger.info("Started {} TOR instances.".format(len(ports['SOCKPorts'])))
    
    
 
def stop_tor():    
    
    # global tor_process    
    tor_status , tor_processes = running_tors()    
    
    for tor_process in tor_processes:
        
        index = tor_processes.index(tor_process)
        
        status = tor_status['processes'][index]
        
        debug("warning","Stopping {} with PID:{}".format(status['name'], status['pid']))
        # print(tor_process)
        tor_process.terminate()


def stop():
        
    # stop all tor processes
    stop_tor()    
    # stop all torman processes
    pids = grep_pids('torman')
    
    if len(pids)>0:
        pids = [str(i) for i in pids]
        cmd = "kill -9 {}".format(' '.join(pids))
        
        debug("warning","Stopping Torman process with PIDS: {}".format(', '.join(pids)))
        
        os.system(cmd) 


def start():
    # Args needed
    import argparse
    
    
    global ARGS

    # Create the parser
    parser = argparse.ArgumentParser(description='Run Multiple TOR processes exposed via a REST API')
    
    # Add an argument   
    parser.add_argument('--control-pass', type=str, required=False, default=None, help='TOR Control Password.')
    parser.add_argument('--server', type=int, required=False, default=6930, help="REST API Port. Default=6930")
    parser.add_argument('--instances', type=int, required=False, default=4, help="TOR Instances to start. Default=4")
    parser.add_argument('--refresh-after', type=int, required=False, default=50, help="API Calls after which TOR Passwords refresh. Default 50")    
    parser.add_argument('--stop', action="store_true", help="Stop All Tor Processes")
    parser.add_argument('--verbose', action="store_true", help="Show API Requests")

    # Parse the argument
    args = parser.parse_args()
    
    ARGS = args
    
    
    
    # If stop
    if args.stop:
        stop()
        
            
    else:    
        # print(args)        
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
                
            
            debug("info", "PROXY Loading", url)
            
            resp, port, remaining = fetch_url(url)
            
            took = timeExec('fetchPage')
            
            debug("info", "TOR done in", took)
            
            response = {
                'meta': {
                    'took' : took ,
                    'proxy': {
                        "port" : port,
                        "remaining-requests" : remaining
                    }
                },
                'response': resp
            }
                
            return jsonify(response), 200
        
        # start TOR      
        start_tor(args.refresh_after, args.control_pass, args.instances)
        
        debug("info", "Params: [control-pass:{},refresh-after:{} requests,server-port:{}]".format(args.control_pass, args.refresh_after, args.server))
               
        # app.run()
        serve(app, host="0.0.0.0", port=args.server)
    
    

if __name__ == "__main__":
    
    start()
    
    
    
    