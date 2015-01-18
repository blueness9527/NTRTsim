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

# Purpose: Helper class/methods for file system management (including directory traversal, file creation, etc).

from os import listdir
from os.path import isfile, join
import os
import shutil
import logging

from script_manager import ScriptManager

# The expected current working directory when this file is called.
CWD_EXPECTED = "src"

class FSManager:


    @staticmethod
    def getDirFileList(fromPath):
        """
        Returns a list of strings containing an entry for each file in fromPath
        """
        fileList = [ f for f in listdir(fromPath) if isfile(join(fromPath,f)) ]
        return fileList

    @staticmethod
    def getBaseDir():
        """
        Returns an absolute path to NTRT's base directory.
        """
        # Verify that our cwd is currently in python_scripts
        cwd = os.getcwd()
        cwdSplit = cwd.split("/")

        if cwdSplit[-1] != CWD_EXPECTED:
            # Not running from the expected directory.
            ScriptManager.terminateScript("Expected current working directory to be '%s', but it was '%s'." % (CWD_EXPECTED, cwdSplit[-1]))

        # Traverse backwards to the base dir. We do this by moving up 3 levels
        # (setup/python_scripts/src)
        baseDir = "/".join(cwdSplit[:-3])

        return baseDir

    @staticmethod
    def copyFile(srcPath, destPath):
        """
        Copies file from srcPath to destPath
        """
        #TODO: Add error checking here for exceptions during copy.
        logging.debug("Copying %s to %s" % (srcPath, destPath))

        shutil.copy(srcPath, destPath)
