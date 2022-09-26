import json

#file = f'{os.getcwd()}\\static\\user-shopping-list\\user_shopping_list.json'
file = '/home/pyodide/user_shopping_list.json'


class User_shopping_List:

    def __init__(self, file: str = file) -> None:
        self.file = file
        self.cache_list: set[int] = set(self.read_cache())

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

    def remove(self, item: str):
        if item in self.cache_list:
            self.cache_list.remove(item)
            with open(file=self.file, mode='w') as cache_file:
                json.dump(list(self.cache_list), cache_file)
            return
        return
