#!/bin/bash

# Copyright 2012, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
# 
# The NASA Tensegrity Robotics Toolkit (NTRT) v1 platform is licensed
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

# Purpose: Helper class/methods for script management (e.g. terminating a script with a helpful error message).

import sys

class ScriptManager:

    @staticmethod
    def terminateScript(terMsg, exitCode=1):
        """
        Displays terMsg and then terminates with provided exit code. 
        """
        print >>sys.stderr, terMsg 
        sys.exit(exitCode)
