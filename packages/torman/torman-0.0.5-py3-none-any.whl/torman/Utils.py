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

import time
import pprint
import os
import json
import subprocess
from urllib.parse import urlparse

import sys

import coloredlogs, logging

# https://pythonrepo.com/repo/xolox-python-coloredlogs-python-generating-and-working-with-logs
# Create a logger object.
logger = logging.getLogger("Torman")
coloredlogs.install(level='INFO', 
                    fmt='%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s',
                    # logger=logger
                )



def sudo_process(cmd_str, sudo_pass,  detached=False):
    
    ls = cmd_str.split()
    
    sudo_pass_bytes = bytes(sudo_pass, encoding="raw_unicode_escape")

    pc =  subprocess.run(ls, check=True, capture_output=True,  input=sudo_pass_bytes)
    
    return pc

def is_absolute_url(url):
    return bool(urlparse(url).netloc)

def print_with_json_boundaries(data):
    boundary = config.get('JSON.boundary')
    
    if(isinstance(data, str)==False):
        data = json.dumps(data,  sort_keys=True, indent=4)
    
    print('{}\n{}\n{}'.format(boundary, data, boundary))
    
execs = {}
def timeExec(name):
    global execs
    
    # get exec name
    exec = execs.get(name)
        
    if(exec):     
        # Get start time
        start = exec.get('start')  
        # calculate elapsed
        elapsed =   time.time() - start 
        
        # add units to elapsed time
        if(elapsed < 1):
            elapsed = "%d%s" % (elapsed*1000, 'ms')
        else: 
            elapsed = "%d%s" % (elapsed, 's')  
        
        # remove reported measure
        execs.pop(name)     
        
        # return 
        return  elapsed
        
    else:        
        execs[name] = {
            'start' : time.time()
        }
  

# PPrint
pp = pprint.PrettyPrinter(indent=4)

def pprint(*args):
    global pp
    pp.pprint(args)
      