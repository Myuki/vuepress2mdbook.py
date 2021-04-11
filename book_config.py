import json
import re
import toml


class BookConfig:
  __vuepressConfig: dict = {}
  __mdbookConifg: dict = {}

  __contents: list = []

  def setVuepressConfig(self, vuepressConfigRaw: str):
    # Standardize VuePress config as JSON
    vuepressConfigString: str = vuepressConfigRaw.lstrip("module.exports = ")
    for match in re.findall(r"\s\w+\:\s", vuepressConfigString):
      key: str = match.strip().rstrip(":")
      indent: str = match[0]
      vuepressConfigString = vuepressConfigString.replace(match, indent + "\"" + key + "\": ")
    self.__vuepressConfig = json.loads(vuepressConfigString)

    # Parsing contents
    for chapter in self.__vuepressConfig["themeConfig"]["sidebar"]:
      pass

  def vuepress2mdbook(self):
    if self.__vuepressConfig == {}:
      print("Error, no VuePress config")
    # Convert metadata
    ## Book
    book: dict = {}
    book["title"] = self.__vuepressConfig["title"]
    book["author"] = ""
    book["description"] = self.__vuepressConfig["description"]
    self.__mdbookConifg["book"] = book

    ## Build
    build: dict = {}
    build["build-dir"] = self.__vuepressConfig["dest"]
    build["create-missing"] = False
    self.__mdbookConifg["build"] = build

    ## output
    output: dict = {}

    ### output.html
    html: dict = {}
    html["site-url"] = self.__vuepressConfig["base"]
    html["no-section-label"] = True

    #### output.html.print
    html["print"] = {"enable": False}

    #### output.html.search
    if (not self.__vuepressConfig["themeConfig"]["search"]):
      html["search"] = {"enable": False}

    output["html"] = html
    self.__mdbookConifg["output"] = output

  def outputMdbookConfig(self, outputDirPath: str):
    if self.__mdbookConifg == {}:
      self.vuepress2mdbook()
    with open(outputDirPath + "/book.toml", 'x') as configFile:
      toml.dump(self.__mdbookConifg, configFile)
