import json


class Cached_shopping_List:

    def __init__(self, file: str) -> None:
        self.file = file
        self.cache_list: set[int] = set(self.read_cache())

    def read_cache(self) -> list | list[str]:
        with open(file=self.file, mode='r') as cache_file:
            read = cache_file.read()
            if not read:
                return []

            return json.loads(read)

    def add_list(self, array: list[str]):
        with open(file=self.file, mode='w') as cache_file:
            self.cache_list = set(list(self.cache_list) + array)
            json.dump(list(self.cache_list), cache_file)
            return

    def add(self, item: str):
        self.cache_list.add(item)
        with open(file=self.file, mode='w') as cache_file:
            json.dump(list(self.cache_list), cache_file)
            return

    def remove(self):
        with open(file=self.file, mode='w') as add_to_server_cache:
            add_to_server_cache.write("")
        return
