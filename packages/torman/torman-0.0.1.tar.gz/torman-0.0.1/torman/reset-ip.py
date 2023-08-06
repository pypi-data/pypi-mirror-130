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


from stem import Signal
from stem.control import Controller



def reset_pass(port, password):
    # print("{}:{}".format(port,password))
    with Controller.from_port(port=port) as controller:
        controller.authenticate(password=password)
        controller.signal(Signal.NEWNYM)
        
        
# port = 9091
# password='giraffe'
if __name__ == "__main__":
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--password', type=str, required=True)

    # Parse the argument
    args = parser.parse_args()
    
    reset_pass(args.port, args.password)