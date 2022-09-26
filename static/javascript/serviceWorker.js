const staticPyPWA = "dev-pypwa-v4"
const assets = [
    "/static/assets/CSS/styles.css",
    "/static/javascript/pwa-scaffold.js",
    
    "/static/Python/Cached_shopping_list_class.py",
    "/static/Python/emoji_by_best_match_search.py",
    "/static/Python/emoji_dictionary.py",
    "/static/Python/item_class.py",
    "/static/Python/server_requests.py",
    "/static/Python/shopping_list.py",
    "/static/Python/user_shopping_list_class.py",
    "/static/Python/utils.py",
    "/static/assets/Json/Add to server cache.json",
    "/static/assets/Json/Remove from server cache.json",
    "/static/assets/Json/user_shopping_list.json",

    "/static/pyscript/pyscript.css",
    "/static/pyscript/pyscript.js",
    "/static/pyscript/pyscript.py",

    "/static/assets/images/favicon.png",
    "/static/assets/images/favicon-72x72.png",
    "/static/assets/images/favicon-96x96.png",
    "/static/assets/images/favicon-128x128.png",
    "/static/assets/images/favicon-144x144.png",
    "/static/assets/images/favicon-152x152.png",
    "/static/assets/images/favicon-192x192.png",
    "/static/assets/images/favicon-384x384.png",
    "/static/assets/images/favicon-512x512.png",

    "/static/pyodide/pyodide.js",
    "/static/pyodide/packages.json",
    "/static/pyodide/pyodide_py.tar",
    "/static/pyodide/pyodide.asm.js",
    "/static/pyodide/pyodide.asm.data",
    "/static/pyodide/pyodide.asm.wasm",
    "/static/pyodide/micropip-0.1-py3-none-any.whl",
    "/static/pyodide/pyparsing-3.0.7-py3-none-any.whl",
    "/static/pyodide/packaging-21.3-py3-none-any.whl",
    "/static/pyodide/distutils.tar",
]

self.addEventListener("install", installEvent => {
    installEvent.waitUntil(
        caches.open(staticPyPWA).then(cache => {
            cache.addAll(assets).then(r => {
                console.log("Cache assets downloaded");
            }).catch(err => console.log("Error caching item", err))
            console.log(`Cache ${staticPyPWA} opened.`);
        }).catch(err => console.log("Error opening cache", err))
    )
})

self.addEventListener("fetch", fetchEvent => {
    fetchEvent.respondWith(
        caches.match(fetchEvent.request).then(res => {
            return res || fetch(fetchEvent.request)
        }).catch(err => console.log("Cache fetch error: ", err))
    )
})