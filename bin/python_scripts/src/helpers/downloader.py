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

import urllib2
import logging
import time

from fs_manager import FSManager

class Downloader:

    def __init__(self, targetURL, baseRelativeFolder, destFileName, maxAttempts=3, failDelay=3):
        """
        Creates a Downloader object for the provided target/local parameters.

        targetURL: Target to download.
        baseRelativeFolder: The file's destination relative to NTRTSim's base dir.
        destFileName: The name of the file when saved locally in baseRelativeFolder
        maxAttempts: The number of download attempts before Downloader fails.
        failDelay: Number of seconds between failed attempts.
        """
        self.targetURL = targetURL
        self.baseRelativeFolder = baseRelativeFolder
        self.destFileName = destFileName
        self.maxAttempts = maxAttempts
        self.failDelay = failDelay
        self.failedAttempts = 0
        self.fullLocalPath = "%s/%s/%s" % (FSManager.getBaseDir(), self.baseRelativeFolder, self.destFileName)

    def downloadTarget(self):
        """
        Attempts to download from target to the local specified path/file.

        Returns nothing on success.

        If more than maxAttempts failures occur, throws DownloaderException with details..
        """
        while self.failedAttempts < self.maxAttempts:
            try:
                self.__attemptDownload()
                return
            except DownloaderException, e:
                logging.error("Hit error while attempting to download %s to %s. Exception message is '%s'" % (self.targetURL, self.fullLocalPath, e))
                logging.debug("Waiting %d seconds before re-attempting download." % self.failDelay)

                self.failedAttempts += 1

                time.sleep(self.failDelay)


        raise DownloaderException("Attempted download of %s to %s, but it failed %d times which exceeds maxAttempts." % (self.targetURL, self.fullLocalPath, self.failedAttempts))

    def __attemptDownload(self):
        fileSize = None
        fileSizeDL = None
        destFile = None

        try:
            fileName = self.destFileName
            url = urllib2.urlopen(self.targetURL)

            destFile = open(self.fullLocalPath, 'wb')
            meta = url.info()

            fileSize = int(meta.getheaders("Content-Length")[0])
            print "Downloading: %s Bytes: %s" % (fileName, fileSize)

            fileSizeDL = 0
            blockSize = 8192
            while True:
                buffer = url.read(blockSize)
                if not buffer:
                    break

                fileSizeDL += len(buffer)
                destFile.write(buffer)
                status = r"%10d  [%3.2f%%]" % (fileSizeDL, fileSizeDL * 100. / fileSize)
                status = status + chr(8)*(len(status)+1)
                print status,
        except IOError, e:
            raise DownloaderException("Hit IOError during download with error message %s" % (e))
        finally:
            if destFile:
                destFile.close()

        if fileSizeDL != fileSize:
            raise DownloaderException("Expected file of size %d, but the downloaded file is %d." % (fileSize, fileSizeDL))



class DownloaderException(Exception):
    pass

