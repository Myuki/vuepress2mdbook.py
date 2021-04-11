#!/usr/bin/env python3

import os
import re
import sys

from book_config import BookConfig

if __name__ == "__main__":
  inputDirPath: str = ""
  outputDirPath: str = sys.path[0] + "/output"

  # Check command
  if len(sys.argv) == 2:
    inputDirPath = sys.argv[1]
  elif len(sys.argv) == 3:
    inputDirPath = sys.argv[1]
    outputDirPath = sys.argv[2]
  else:
    if len(sys.argv) == 1:
      print("Error, please specific input path")
    else:
      print("Error, command wrong")
    sys.exit(1)

  # Check input path
  if not inputDirPath.startswith("/") and re.match(r"[A-Za-z]\:", inputDirPath) == None:
    inputDirPath = sys.path[0] + "/" + inputDirPath
  # Check output path
  if not os.path.exists(outputDirPath):
    os.makedirs(outputDirPath)

  # Read VuePress config
  vuepressConfigPath = inputDirPath + "/.vuepress/config.js"
  vuepressConfigRaw: str = ""
  with open(vuepressConfigPath, "r") as vuepressConfigFile:
    vuepressConfigRaw = vuepressConfigFile.read()
  config = BookConfig()
  config.setVuepressConfig(vuepressConfigRaw)
  config.outputMdbookConfig(outputDirPath)
