from aiohttp import web

names_db = {
    1: "Sophia",
    2: "Michael",
}


async def get_names(request):
    return web.json_response(names_db)


async def get_name_by_id(request):
    name_id = request.match_info.get("id")
    response = {
        "id": name_id,
        "name": names_db.get(int(name_id), "Unknown"),
    }
    return web.json_response(response)


async def add_name(request):
    data = await request.json()
    new_id = len(names_db) + 1
    names_db[new_id] = data.get("name")
    return web.json_response({"id": new_id, "name": names_db[new_id]}, status=201)


app = web.Application()
app.router.add_get("/names", get_names)
app.router.add_get("/names/{id}", get_name_by_id)
app.router.add_post("/names", add_name)

web.run_app(app)
