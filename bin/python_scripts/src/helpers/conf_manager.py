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

# Purpose: Manages configuration files during setup/upgrades.

from fs_manager import FSManager
from script_manager import ScriptManager

import logging

# The location of generated conf files (relative to the base dir).
CONF_RELATIVE = "/conf/"

# The location of default conf files (relative to the base dir).
CONF_DEFAULT_RELATIVE = "/conf/default/"

class ConfManager:

    def verifyConf(self):
        """
        Determines which (if any) conf files are absent.

        If any conf files are absent, the user will be notified, and prompted to create them.
        """
        logging.debug("Checking if any conf files need to be generated.")

        # Get list of files in default and live conf folders.
        defaultList = self.__getDefaultList()
        generatedList = self.__getConfList()

        logging.debug("Default conf files: %r" % (defaultList))
        logging.debug("Generated conf files: %r" % (generatedList))

        # Stores names of all conf files that have to be generated (excludes the .default suffix).
        missingConf = []

        # Determine which conf files have not been created.
        for confName in defaultList:
            if confName not in generatedList:
                missingConf.append(confName)

        logging.debug("Missing conf file length is %d, missing files %r" % (len(missingConf), missingConf))

        if len(missingConf) > 0:
            self.__generateConfFiles(missingConf)


    def __generateConfFiles(self, toGenerate):
        """
        Generates the conf files listed in toGenerate. Each name in toGenerate should exclude
        the .default suffix (e.g. bullet.conf, *not* bullet.conf.default). Files will be copied
        from conf/default into conf.
        """
        logging.debug("Generating configuration files.")

        # Create absolute paths to our default and generated conf directories
        defaultDir = "%s%s" % (FSManager.getBaseDir(), CONF_DEFAULT_RELATIVE)
        confDir = "%s%s" % (FSManager.getBaseDir(), CONF_RELATIVE)

        logging.debug("Default directory is %s, and generated directory is %s" % (defaultDir, confDir))

        for confName in toGenerate:
            defaultPath = "%s%s.default" % (defaultDir, confName)
            genPath = "%s%s" % (confDir, confName)
            FSManager.copyFile(defaultPath, genPath)

        logging.debug("Configuration file generation complete.")

        ScriptManager.terminateScript("Your installation was missing %d configuration files. Their names are %r. They have now been generated in /conf. Edit them as necessary, then run setup again to proceed." % (len(toGenerate), toGenerate), 0)

    def __getDefaultList(self):
        fileList = FSManager.getDirFileList(FSManager.getBaseDir()+CONF_DEFAULT_RELATIVE)

        # Remove '.default' suffix so we can check equivalency against generated files.
        for i in range(0, len(fileList)):
            if fileList[i].endswith(".conf.default"):
                fileList[i] = fileList[i].rsplit(".", 1)[0]

        return fileList

    def __getConfList(self):
        return FSManager.getDirFileList(FSManager.getBaseDir()+CONF_RELATIVE)

