import asyncio

import asyncpg
from aiohttp import web

DB_DSN = "postgresql://userdb:user@localhost:5432/names_db"


async def init_db_schema():
    conn = await asyncpg.connect(DB_DSN)

    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS names (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """
    )

    count = await conn.fetchval("SELECT COUNT(*) FROM names")
    if count == 0:
        await conn.execute(
            "INSERT INTO names (name) VALUES ($1), ($2)", "Sophia", "Michael"
        )

    await conn.close()


async def init_db_pool():
    pool = await asyncpg.create_pool(
        dsn=DB_DSN,
        min_size=5,
        max_size=20,
        max_inactive_connection_lifetime=300,
    )

    return pool


async def get_names(request):
    async with request.app["db_pool"].acquire() as conn:
        rows = await conn.fetch("SELECT id, name FROM names ORDER BY id")
        result = {row["id"]: row["name"] for row in rows}
        return web.json_response(result)


async def get_name_by_id(request):
    name_id = int(request.match_info.get("id"))
    async with request.app["db_pool"].acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, name FROM names WHERE id = $1",
            name_id,
        )
        if not row:
            return web.json_response(
                {"error": "Name not found"},
                status=404,
            )
        response = {
            "id": row["id"],
            "name": row["name"],
        }
    return web.json_response(response)


async def add_name(request):
    data = await request.json()
    name = data.get("name")

    async with request.app["db_pool"].acquire() as conn:
        new_id = await conn.fetchval(
            "INSERT INTO names (name) VALUES ($1) RETURNING id", name
        )

    return web.json_response({"id": new_id, "name": name})


async def sse_handler(request):
    r = web.StreamResponse()
    r.headers["Content-Type"] = "text/event-stream"
    r.headers["Cache-Control"] = "no-cache"
    r.headers["Connection"] = "keep-alive"
    await r.prepare(request)
    counter = 0
    while counter < 3:
        counter += 1
        data = "Temperature: 70 \n"
        await r.write(data.encode("utf-8"))
        await asyncio.sleep(1)

    await r.write_eof()
    return r


async def on_startup(app):
    await init_db_schema()
    app["db_pool"] = await init_db_pool()


async def on_cleanup(app):
    if app["db_pool"]:
        await app["db_pool"].close()


async def create_app():
    app = web.Application()

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    app.router.add_get("/names", get_names)
    app.router.add_get("/names/{id}", get_name_by_id)
    app.router.add_post("/names", add_name)
    app.router.add_get("/events", sse_handler)

    return app


# For running directly with `python app.py`
if __name__ == "__main__":
    web.run_app(asyncio.run(create_app()))
