import asyncio
from __init__ import bot, log
from web import keep_alive, web_server
from aiohttp import web

BIND_ADDRESS = "0.0.0.0"
PORT = "8080"

async def start_services():        
        server = web.AppRunner(web_server())
        await server.setup()
        await web.TCPSite(server, BIND_ADDRESS, PORT).start()
        log.info("Web Server Initialized Successfully")
        log.info("=========== Service Startup Complete ===========")
  
        asyncio.create_task(keep_alive())
        log.info("Keep Alive Service Started")
        log.info("=========== Initializing Web Server ===========")

if __name__ == "__main__":
     loop = asyncio.get_event_loop()
     loop.run_until_complete(start_services())
     bot.run()
     log.info('Bot Started!')
