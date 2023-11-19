from __future__ import annotations

import asyncio
import configparser
import pathlib
import tracemalloc
from typing import List

from sqlalchemy import NullPool, MetaData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from database.Db_objects import Base

meta = MetaData()

p = pathlib.Path(__file__).parent.parent.joinpath('config.ini')

config = configparser.ConfigParser()
config.read(p)

BDCONNECTION = config['DEFAULT']["BDCONNECTION"]


async def session_gen(session_maker: async_sessionmaker):
    while True:
        async with session_maker() as async_session:
            await async_session.begin()
            try:
                yield async_session
            finally:
                await async_session.close()


class DataBase:
    def __init__(self):
        print("db class inited")

    def __call__(self):
        return self

    engine = create_async_engine(
        BDCONNECTION,
        echo=False,
        poolclass=NullPool,
    )

    async_sessionmaker = async_sessionmaker(engine, expire_on_commit=True)

    async def get_session(self) -> AsyncSession:
        async with self.async_sessionmaker() as async_session:
            await async_session.begin()
            return async_session

    @staticmethod
    async def init_db() -> None:
        engine = create_async_engine(
            BDCONNECTION,
            echo=False,
            poolclass=NullPool,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        await engine.dispose()


db = DataBase()

if __name__ == "__main__":
    tracemalloc.start()
    asyncio.run(DataBase.init_db())
