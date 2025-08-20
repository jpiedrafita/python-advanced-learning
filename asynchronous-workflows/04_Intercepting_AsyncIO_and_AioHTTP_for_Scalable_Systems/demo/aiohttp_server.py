import asyncio
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


async def sse_handler(request):
    # Initialize a streaming response
    r = web.StreamResponse()
    # Set headers
    r.headers["Content-Type"] = "text/event-stream"
    r.headers["Cache-Control"] = "no-cache"
    r.headers["Connection"] = "keep-alive"
    # Send headers to client
    await r.prepare(request)
    counter = 0
    # Stream data events up to 3 times
    while counter < 3:
        counter += 1
        data = "Temperature: 70 \n"
        # Send event data chunk
        await r.write(data.encode("utf-8"))
        # Non-blocking delay for 1 second
        await asyncio.sleep(1)

    # Finalize stream
    await r.write_eof()
    return r


app = web.Application()
app.router.add_get("/names", get_names)
app.router.add_get("/names/{id}", get_name_by_id)
app.router.add_post("/names", add_name)

app.router.add_get("/events", sse_handler)

# gunicorn aiohttp_server:app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker --workers 2
# web.run_app(app)
