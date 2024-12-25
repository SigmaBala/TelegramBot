from aiohttp import web
import asyncio, aiohttp, logging, traceback

WEB_URL = "https://telegram-bot-4klo.onrender.com"
WEB_SLLEP = 3*60


log = logging.getLogger(__name__)


routes = web.RouteTableDef()

@routes.get('/', allow_head=True)
async def hello(request):
    return web.Response(text="Hello, world!")


def web_server():
    app = web.Application()
    app.add_routes(routes)
    return app


async def keep_alive():
    if WEB_URL:
        while True:
            await asyncio.sleep(WEB_SLLEP)
            try:
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as session:
                    async with session.get(WEB_URL) as resp:
                        log.info(
                            "Pinged {} with response: {}".format(
                                WEB_URL, resp.status
                            )
                        )
            except asyncio.TimeoutError:
                log.warning("Couldn't connect to the site URL..!")
            except Exception:
                traceback.print_exc()
