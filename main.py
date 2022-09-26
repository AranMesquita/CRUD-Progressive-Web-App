from flask import Flask, render_template, request, jsonify, make_response
from server_data_base_class import Server_shopping_List
from pathlib import Path

app = Flask(__name__)


@app.get("/")
def start():
    return render_template('index.html')


@app.route("/server-shopping-list", methods=['POST', 'GET'])
def server_shopping_list():
    if request.method == "POST":
        try:
            server_shopping_List = Server_shopping_List()
            server_request = request.get_json()

            if list(server_request.keys())[0] == "add-item":
                server_request = server_request["add-item"]
                server_shopping_List.add(server_request)
                return 'item recieved'

            elif list(server_request.keys())[0] == "add-cached-list":
                server_request = server_request["add-cached-list"]
                server_shopping_List.add_list(server_request)
                return 'item recieved'

            elif list(server_request.keys())[0] == "remove-item":
                server_request = server_request["remove-item"]
                server_shopping_List.remove(server_request)
                return 'item recieved'

            elif list(server_request.keys())[0] == "remove-cached-list":
                server_request = server_request["remove-cached-list"]
                for item in server_request:
                    server_shopping_List.remove(item)
                return 'item recieved'

        except Exception as error:
            print(error)

    elif request.method == "GET":
        try:
            server_shopping_List = Server_shopping_List()

            return jsonify(server_shopping_List.read_cache())
        except Exception as error:
            print(error)

    else:
        return 'not item'


@app.get('/serviceWorker.js')
def worker():
    js = Path(__file__).parent / 'static' / 'javascript' / 'serviceWorker.js'
    text = js.read_text()
    resp = make_response(text)
    resp.content_type = 'application/javascript'
    resp.headers['Service-Worker-Allowed'] = '/'

    return resp


if __name__ == "__main__":
    app.run(debug=True)
