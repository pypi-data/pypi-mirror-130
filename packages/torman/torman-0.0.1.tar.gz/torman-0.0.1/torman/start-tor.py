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

import subprocess
import os 
from fastcore.utils import Path



def start_tor(ports_file):
    
    cmd = 'tor -f {}'.format(ports_file)
    ls = cmd.split()
    # print(cmd)    
    process = subprocess.run(ls, stdout=subprocess.PIPE)
    resp_str = process.stdout.decode('utf-8')
    
   
# Fork out process...
pid = os.fork()
# if pid == 0:    
#     print("  Tor Processes Running!")

        
# port = 9091
# password='giraffe'
if __name__ == "__main__":
    # Home Dir
    home_dir = Path(__file__).parent.absolute()
    ports_file = os.path.join( home_dir, "config","torrc");

    start_tor(ports_file)
    
  