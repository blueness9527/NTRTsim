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

# Purpose: Installs/upgrades NTRT.

import logging

from helpers.conf_manager import ConfManager
from helpers.dir_initializer import DirInitializer

# Configure logging
logging.basicConfig(level=logging.DEBUG)

logging.debug("== BEGIN: Configuration Generation ==")
confManager = ConfManager()
confManager.verifyConf()
logging.debug("== END: Configuration Generation ==")

# Prepare our directories
logging.debug("== BEGIN: Directory Preparation ==")
dirInitializer = DirInitializer()
dirInitializer.prepareDirectories()
logging.debug("== END: Directory Preparation ==")

