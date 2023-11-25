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

from database.Db_objects import Base, Client, Lawyer, PaymentStatus, Payment, ContractStatus, Contract

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

    async def add_lawyer(self, fio: str, salary: str):
        session = await self.get_session()
        try:
            lawyer = Lawyer(FIO=fio, salary=salary)
            session.add(lawyer)
        finally:
            await session.commit()
            await session.close()

    async def dell_lawyer(self, id_lawyer: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Lawyer).where(Lawyer.id_lawyer == id_lawyer)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                await session.delete(item)
                return True
        finally:
            await session.commit()
            await session.close()

    async def edit_lawyer(self, id: int, fio: str, salary: str) -> bool:
        session = await self.get_session()
        try:
            q = select(Lawyer).where(Lawyer.id_lawyer == id)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                item.FIO = fio
                item.salary = salary
                return True
        finally:
            await session.commit()
            await session.close()

    async def get_paymentStatuses(self) -> List[PaymentStatus]:
        session = await self.get_session()
        try:
            q = select(PaymentStatus)
            paymentStatuses = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in paymentStatuses:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()

    async def add_paymentStatus(self, status: str):
        session = await self.get_session()
        try:
            paymentStatus = PaymentStatus(status=status)
            session.add(paymentStatus)
        finally:
            await session.commit()
            await session.close()

    async def dell_paymentStatus(self, id_payment_status: int) -> bool:
        session = await self.get_session()
        try:
            q = select(PaymentStatus).where(PaymentStatus.id_payment_status == id_payment_status)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                await session.delete(item)
                return True
        finally:
            await session.commit()
            await session.close()

    async def edit_paymentStatus(self, id: int, status: str) -> bool:
        session = await self.get_session()
        try:
            q = select(PaymentStatus).where(PaymentStatus.id_payment_status == id)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                item.status = status
                return True
        finally:
            await session.commit()
            await session.close()

    async def get_payments(self) -> List[Payment]:
        session = await self.get_session()
        try:
            q = select(Payment)
            payments = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in payments:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()

    async def add_payment(self, amount: str, id_payment_status: int):
        session = await self.get_session()
        try:
            payment = Payment(amount=amount, id_payment_status=id_payment_status)
            session.add(payment)
        finally:
            await session.commit()
            await session.close()

    async def dell_payment(self, id_payment: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Payment).where(Payment.id_payment == id_payment)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                await session.delete(item)
                return True
        finally:
            await session.commit()
            await session.close()

    async def edit_payment(self, id: int, amount: str, id_payment_status: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Payment).where(Payment.id_payment == id)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                item.amount = amount
                item.id_payment_status = id_payment_status
                return True
        finally:
            await session.commit()
            await session.close()

    async def get_contractStatuses(self) -> List[ContractStatus]:
        session = await self.get_session()
        try:
            q = select(ContractStatus)
            contractStatus = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in contractStatus:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()

    async def add_contractStatus(self, status: str):
        session = await self.get_session()
        try:
            contractStatus = ContractStatus(status=status)
            session.add(contractStatus)
        finally:
            await session.commit()
            await session.close()

    async def dell_contractStatus(self, id_contract_status: int) -> bool:
        session = await self.get_session()
        try:
            q = select(ContractStatus).where(ContractStatus.id_contract_status == id_contract_status)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                await session.delete(item)
                return True
        finally:
            await session.commit()
            await session.close()

    async def edit_contractStatus(self, id: int, status: str) -> bool:
        session = await self.get_session()
        try:
            q = select(ContractStatus).where(ContractStatus.id_contract_status == id)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                item.status = status
                return True
        finally:
            await session.commit()
            await session.close()

    async def get_contracts(self) -> List[Contract]:
        session = await self.get_session()
        try:
            q = select(Contract)
            contracts = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in contracts:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()

    async def add_contract(self, link: str, id_contract_status: int):
        session = await self.get_session()
        try:
            contract = Contract(link=link, id_contract_status=id_contract_status)
            session.add(contract)
        finally:
            await session.commit()
            await session.close()

    async def dell_contract(self, id_contract: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Contract).where(Contract.id_contract == id_contract)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                await session.delete(item)
                return True
        finally:
            await session.commit()
            await session.close()

    async def edit_contract(self, id: int, link: str, id_contract_status: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Contract).where(Contract.id_contract == id)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                item.link = link
                item.id_contract_status = id_contract_status
                return True
        finally:
            await session.commit()
            await session.close()


db = DataBase()

if __name__ == "__main__":
    tracemalloc.start()
    asyncio.run(DataBase.init_db())
