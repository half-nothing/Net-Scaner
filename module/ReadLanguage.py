from json5.lib import load


class Product:
    def __init__(self, d):
        self.__dict__ = d


config = load(open("config.json5", "r", encoding="UTF-8", errors="ignore"), object_hook=Product)
language = load(open(f"lang/{config.language}.json5", "r", encoding="UTF-8", errors="ignore"), object_hook=Product)
