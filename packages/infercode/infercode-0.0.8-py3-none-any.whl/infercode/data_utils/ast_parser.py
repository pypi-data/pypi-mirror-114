import sys
from pathlib import Path
# To import upper level modules
sys.path.append(str(Path('.').absolute().parent))
from os import path
from .vocabulary import Vocabulary
from .language_util import LanguageUtil
from tree_sitter import Language, Parser
from pathlib import Path
import glob, os
import numpy as np


class ASTParser():
    import logging
    LOGGER = logging.getLogger('ASTParser')
    def __init__(self, language: str):

        self.language = language

        # ------------ To initialize for the treesitter parser ------------
        home = str(Path.home())
        cd = os.getcwd()
        os.chdir(path.join(home, ".tree-sitter", "bin"))
        Languages = {}
        for file in glob.glob("*.so"):
          try:
            lang = os.path.splitext(file)[0]
            Languages[lang] = Language(path.join(home, ".tree-sitter", "bin", file), lang)
          except:
            print("An exception occurred to {}".format(lang))
        os.chdir(cd)
        self.parser = Parser()
        lang = Languages.get(language)
        self.parser.set_language(lang)
        # -----------------------------------------------------------------

       
    def parse(self, code_snippet):
        return self.parser.parse(code_snippet)