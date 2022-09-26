from datetime import datetime as dt
from item_class import Item
from emoji_by_best_match_search import emoji_by_best_match_search
from user_shopping_list_class import User_shopping_List
from Cached_shopping_list_class import Cached_shopping_List
import asyncio
from server_requests import server_request
from utils import add_class, remove_class

shopping_list = []
total_cost = float(0)
cached_user_shopping_list = User_shopping_List()

# define the task template that will be use to render new templates to the page
task_template = Element("task-template").select(".task", from_content=True)
task_list = Element("list-tasks-container")
new_task_content = Element("new-task-content")
total = Element("total-cost-container")


def add_item(*args, **kwargs):
    global cached_user_shopping_list
    # ignore empty task
    if not new_task_content.element.value:
        return None

    # create task
    item_id = f"task-{len(shopping_list)}"
    item_object = Item(id=item_id, name=new_task_content.element.value, buy=True,
                       created_at=dt.now(), price=float(0))

    shopping_list.append(item_object)
    cached_user_shopping_list.add(new_task_content.element.value)
    asyncio.create_task(server_request(str(new_task_content.element.value), "add-item", True, '/home/pyodide/Add to server cache.json')
                        )
    # add the task element to the page as new node in the list by cloning from a
    # template
    shopping_list_container = task_template.clone(item_id, to=task_list)
    list_item_html = shopping_list_container.select("li")
    list_item_html.element.innerText = item_object.name
    div_list_item = shopping_list_container.select(".emoji")
    div_list_item.element.innerHTML = f"{emoji_by_best_match_search(item_object.name)} " + \
        f'{list_item_html.element.innerText}'
    task_list.element.appendChild(shopping_list_container.element)
    price_input = shopping_list_container.select("input")

    def check_if_bought(evt=None):
        item_object.buy = not item_object.buy
        if not item_object.buy:
            add_class(div_list_item, "line-through")
            cached_user_shopping_list.remove(item_object.name)
            asyncio.create_task(server_request(str(item_object.name), "remove-item", True, '/home/pyodide/Remove from server cache.json')
                                )
            return
        else:
            remove_class(div_list_item, "line-through")
            cached_user_shopping_list.add(item_object.name)
            asyncio.create_task(server_request(str(item_object.name), "add-item", True, '/home/pyodide/Add to server cache.json')
                                )
            return

    def calculate_cost(*args, **kwargs):
        try:
            def multiplier(item: str) -> int:
                multiplier: int = 0
                for num in item:
                    if num.isnumeric() and multiplier == 0:
                        multiplier = int(num)
                        continue
                    elif num.isnumeric() and multiplier > 0:
                        multiplier = (multiplier * 10) + int(num)
                        continue
                    elif not num.isnumeric():
                        continue
                return multiplier if multiplier > 0 else 1

            price = price_input.element.value
            total_html = Element("total-float")
            global total_cost

            if total_cost == float(0):
                item_object.price = float(price) * multiplier(item_object.name)
                total_cost = float(price) * multiplier(item_object.name)
                total_html.write(
                    f'Total: R{round(float(total_cost), 2)}')
                return
            if total_cost != float(0):
                total_cost = (total_cost + (float(price) * multiplier(item_object.name))) - \
                    (item_object.price if item_object.price > float(0) else float(0))
                item_object.price = float(price) * multiplier(item_object.name)
                total_html.write(f'Total: R{round(float(total_cost), 2)}')
                return
        except Exception as error:
            print(error)
            return

    def add_cost(e):
        if e.key == "Enter":
            calculate_cost()

    new_task_content.clear()
    div_list_item.element.onclick = check_if_bought
    price_input.element.onkeydown = add_cost


def add_task_event(e):
    if e.key == "Enter":
        add_item()


def add_cached_item(item: str):
    item_id = f"task-{len(shopping_list)}"

    item_object = Item(id=item_id, name=item, buy=True,
                       created_at=dt.now(), price=float(0))

    shopping_list.append(item_object)

    shopping_list_container = task_template.clone(item_id, to=task_list)
    list_item_html = shopping_list_container.select("li")
    list_item_html.element.innerText = item_object.name
    div_list_item = shopping_list_container.select(".emoji")
    div_list_item.element.innerHTML = f"{emoji_by_best_match_search(item_object.name)} " + \
        f'{list_item_html.element.innerText}'
    task_list.element.appendChild(shopping_list_container.element)
    price_input = shopping_list_container.select("input")

    def check_if_bought(evt=None):
        item_object.buy = not item_object.buy
        if not item_object.buy:
            add_class(div_list_item, "line-through")
            cached_user_shopping_list.remove(item_object.name)
            asyncio.create_task(server_request(str(item_object.name), "remove-item", True, '/home/pyodide/Remove from server cache.json')
                                )
            return
        else:
            remove_class(div_list_item, "line-through")
            cached_user_shopping_list.add(item_object.name)
            asyncio.create_task(server_request(str(item_object.name), "add-item", True, '/home/pyodide/Add to server cache.json')
                                )
            return

    def calculate_cost(*args, **kwargs):
        try:
            def multiplier(item: str) -> int:
                multiplier: int = 0
                for num in item:
                    if num.isnumeric() and multiplier == 0:
                        multiplier = int(num)
                        continue
                    elif num.isnumeric() and multiplier > 0:
                        multiplier = (multiplier * 10) + int(num)
                        continue
                    elif not num.isnumeric():
                        continue
                return multiplier if multiplier > 0 else 1

            price = price_input.element.value
            total_html = Element("total-float")
            global total_cost

            if total_cost == float(0):
                item_object.price = float(price) * multiplier(item_object.name)
                total_cost = float(price) * multiplier(item_object.name)
                total_html.write(f'Total: R{round(float(total_cost), 2)}')
                return
            if total_cost != float(0):
                total_cost = (total_cost + (float(price)) * multiplier(item_object.name)) - \
                    (item_object.price if item_object.price >
                     float(0) else float(0))
                item_object.price = float(price) * multiplier(item_object.name)
                total_html.write(f'Total: R{round(float(total_cost), 2)}')
                return
        except Exception as error:
            print(error)
            return

    def add_cost(e):
        if e.key == "Enter":
            calculate_cost()

    new_task_content.clear()
    price_input.element.onkeydown = add_cost
    div_list_item.element.onclick = check_if_bought


async def add_cached_list():
    server_shopping_list = await server_request()
    for item in server_shopping_list:
        add_cached_item(item)


async def on_load_add_or_remove_from_offline_cache(file: str, add_or_remove: str):
    cache = Cached_shopping_List(file)
    if not cache.read_cache():
        return
    try:
        server_request: bool = await server_request(item=cache.read_cache(), add_or_remove=add_or_remove, POST=True, file=file)
        if not server_request:
            return
        cache.remove()
    except Exception as error:
        return f"exception occured:\n{error}\nun-able to added cache"


new_task_content.element.onkeypress = add_task_event


if __name__ == '__main__':
    asyncio.create_task(add_cached_list())
    asyncio.create_task(on_load_add_or_remove_from_offline_cache(
        file='/home/pyodide/Add to server cache.json', add_or_remove='add-cached-list'))
    asyncio.create_task(on_load_add_or_remove_from_offline_cache(
        file='/home/pyodide/Remove from server cache.json', add_or_remove='remove-cached-list'))
