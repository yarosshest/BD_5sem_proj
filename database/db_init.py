import configparser
import pathlib
from asyncio import get_event_loop

from database.async_db import DataBase as Db


async def db_init():
    db = Db()
    await db.init_db()

    p = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
    config = configparser.ConfigParser()
    config.read(p)


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(db_init())
