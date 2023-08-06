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

from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Initialize multiple TOR instances and proxy to them using an API'

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

# LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="torman", 
        version=VERSION,
        author="Anthony Mugendi",
        author_email="ngurumugz@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'tor', 'manager', 'proxy', 'multiple', 'anonymous'],
        license='Apache License 2.0',
        platforms='any',
        
        entry_points = {
            'console_scripts': ['torman=torman:main'],
        },
        
        classifiers= [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Intended Audience :: Telecommunications Industry',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Internet',
            'Topic :: System :: Networking',
        ]
)