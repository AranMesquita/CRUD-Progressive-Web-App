import json
from Cached_shopping_list_class import Cached_shopping_List
from user_shopping_list_class import User_shopping_List
from pyodide.http import pyfetch


async def server_request(item: str | list[str] = None, add_or_remove: str = None, POST: bool = False, file: str = None):
    if POST:
        cached_shopping_List = Cached_shopping_List(file)
        response = await pyfetch(
            url="/server-shopping-list",
            method="POST",
            headers={
                "Content-Type": "application/json",
                'Accept': 'application/json',
            },
            body=json.dumps({add_or_remove: item})
        )
        try:
            if not response.ok:
                if add_or_remove == "add-item":
                    cached_shopping_List.add(item)
                    return
                elif add_or_remove == "remove-item":
                    cached_shopping_List.add(item)
                    return
                return print(f'!response.ok:\n{add_or_remove}\nitem added to cache')
            return False
        except:
            if add_or_remove == "add-item":
                cached_shopping_List.add(item)
                return
            elif add_or_remove == "remove-item":
                cached_shopping_List.add(item)
                return
            return print(f'exception occurred:\nitem added to cache')

    response = await pyfetch(
        url="/server-shopping-list",
        method="GET",
        headers={
            "Content-Type": "application/json",
            'Accept': 'application/json',
        }
    )
    try:
        response = await response.json()
        return response
    except:
        cached_user_shopping_List = User_shopping_List()
        return cached_user_shopping_List.read_cache()
