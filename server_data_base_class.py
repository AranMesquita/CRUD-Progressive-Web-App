import json
import os

file = f'{os.getcwd()}\\data-base.json'


class Server_shopping_List:

    def __init__(self, file: str = file) -> None:
        self.file = file
        self.cache_list: set[str] = set(self.read_cache())

    def read_cache(self) -> list | list[str]:
        with open(file=self.file, mode='r') as cache_file:
            read = cache_file.read()
            if not read:
                return []

            return json.loads(read)

    def add(self, item: str):
        self.cache_list.add(item)
        with open(file=self.file, mode='w') as cache_file:
            json.dump(list(self.cache_list), cache_file)
            return

    def add_list(self, array: list[str]):
        with open(file=self.file, mode='w') as cache_file:
            self.cache_list = set(list(self.cache_list) + array)
            json.dump(list(self.cache_list), cache_file)
            return

    def remove(self, item: str):
        if item in self.cache_list:
            self.cache_list.remove(item)
            with open(file=self.file, mode='w') as cache_file:
                json.dump(list(self.cache_list), cache_file)
            return
        return
