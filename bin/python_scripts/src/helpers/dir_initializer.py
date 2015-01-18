import logging
import os
from fs_manager import FSManager
from script_manager import ScriptManager

DIRS_TO_INIT = [
"env",
"env/downloads",
"build"
]

class DirInitializer:

    def prepareDirectories(self):
        """
        Creates following directories (relative to base) if they're not found.

        env
        env/downloads
        build
        """
        for toInit in DIRS_TO_INIT:
            self.__makeRelativeDir(toInit)

    def __makeRelativeDir(self, relativePath):
        fullPath = "%s/%s" % (FSManager.getBaseDir(), relativePath)

        try:
            logging.debug("Checking if %s has to be created." % fullPath)

            if not os.path.exists(fullPath):
                logging.debug("%s doesn't exist. Creating it now." % fullPath)
                os.mkdir(fullPath)
            else:
                logging.debug("%s already exists." % fullPath)
        except os.error, e:
            ScriptManager.terminateScript("Hit an os.error during creation of %s. Error details are %s" % (fullPath, e))
