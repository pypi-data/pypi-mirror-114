from .itransformer import InterfaceTransform
from .. import Jsi18n


class PyLan(Jsi18n):
    def __init__(self):
        """ implementation of interface transformation """
        super(InterfaceTransform, self).__init__("Pyi18n")

    def wrap_file(self, lang_key: str, content_list: list) -> list:
        return ["{\"" + lang_key + "\":", "{"] + content_list + ["}", "}"]
