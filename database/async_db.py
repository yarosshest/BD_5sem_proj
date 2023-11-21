from __future__ import annotations

import asyncio
import configparser
import pathlib
import string
import tracemalloc
from typing import List

from sqlalchemy import NullPool, MetaData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from database.Db_objects import Base, Client, Lawyer

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

    async def get_clients(self) -> List[Client]:
        session = await self.get_session()
        try:
            q = select(Client)
            clients = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in clients:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()

    async def add_client(self, fio: str, inn: str, phone: str):
        session = await self.get_session()
        try:
            client = Client(FIO=fio, INN=inn, phone=phone)
            session.add(client)
        finally:
            await session.commit()
            await session.close()

    async def dell_client(self, id_client: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Client).where(Client.id_client == id_client)
            result = await session.execute(q)
            client = result.scalars().unique().first()
            if client is None:
                return False
            else:
                await session.delete(client)
                return True
        finally:
            await session.commit()
            await session.close()

    async def edit_client(self, id_client: int, fio: str, inn: str, phone: str) -> bool:
        session = await self.get_session()
        try:
            q = select(Client).where(Client.id_client == id_client)
            result = await session.execute(q)
            client = result.scalars().unique().first()
            if client is None:
                return False
            else:
                client.FIO = fio
                client.INN = inn
                client.phone = phone
                return True
        finally:
            await session.commit()
            await session.close()

    async def get_lawyers(self) -> List[Lawyer]:
        session = await self.get_session()
        try:
            q = select(Lawyer)
            lawyers = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in lawyers:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()


db = DataBase()

if __name__ == "__main__":
    tracemalloc.start()
    asyncio.run(DataBase.init_db())
