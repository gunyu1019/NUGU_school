import logging
from aiohttp import web

from config import parser
from route.meal import meal
from route.timetable import timetable

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    route = web.RouteTableDef()

    app = web.Application()
    app.add_routes([web.post('/api/NUGU/meal', meal),
                    web.post('/api/NUGU/timetable', timetable)])
    web.run_app(app,
                host=parser.get('DEFAULT', 'host'),
                port=parser.get('DEFAULT', 'port'),
                access_log_format=parser.get('DEFAULT', 'access_log_format'))