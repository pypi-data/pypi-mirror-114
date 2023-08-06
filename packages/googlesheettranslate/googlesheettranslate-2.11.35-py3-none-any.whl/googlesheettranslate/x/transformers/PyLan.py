from .. import Jsi18n


class PyLan(Jsi18n):

    def wrap_file(self, lang_key: str, content_list: list) -> list:
        return ["{\"" + lang_key.lower() + "\":", "{"] + content_list + ["}", "}"]
