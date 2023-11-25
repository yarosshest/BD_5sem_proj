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

from database.Db_objects import Base, Client, Lawyer, PaymentStatus, Payment, ContractStatus, Contract, RequestStatus, \
    Request, ProductionStatus, ProductionSheet

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

    async def get_requestStatuses(self) -> List[RequestStatus]:
        session = await self.get_session()
        try:
            q = select(RequestStatus)
            requestStatus = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in requestStatus:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()

    async def add_requestStatus(self, status: str):
        session = await self.get_session()
        try:
            requestStatus = RequestStatus(status=status)
            session.add(requestStatus)
        finally:
            await session.commit()
            await session.close()

    async def dell_requestStatus(self, id_request_status: int) -> bool:
        session = await self.get_session()
        try:
            q = select(RequestStatus).where(RequestStatus.id_request_status == id_request_status)
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

    async def edit_requestStatus(self, id: int, status: str) -> bool:
        session = await self.get_session()
        try:
            q = select(RequestStatus).where(RequestStatus.id_request_status == id)
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

    async def get_requests(self) -> List[Request]:
        session = await self.get_session()
        try:
            q = select(Request)
            requests = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in requests:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()

    async def add_request(self, id_client: int, id_lawyer: int, id_payment: int, id_contract: int,
                          id_request_status: int):
        session = await self.get_session()
        try:
            request = Request(id_client=id_client, id_lawyer=id_lawyer, id_payment=id_payment, id_contract=id_contract,
                              id_request_status=id_request_status)
            session.add(request)
        finally:
            await session.commit()
            await session.close()

    async def dell_request(self, id_request: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Request).where(Request.id_request == id_request)
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

    async def edit_request(self, id: int, id_client: int, id_lawyer: int, id_payment: int, id_contract: int,
                           id_request_status: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Request).where(Request.id_request == id)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                item.id_client = id_client
                item.id_lawyer = id_lawyer
                item.id_payment = id_payment
                item.id_contract = id_contract
                item.id_request_status = id_request_status
                return True
        finally:
            await session.commit()
            await session.close()

    async def get_ProductionStatuses(self) -> List[ProductionStatus]:
        session = await self.get_session()
        try:
            q = select(ProductionStatus)
            productionStatus = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in productionStatus:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()

    async def add_ProductionStatus(self, status: str):
        session = await self.get_session()
        try:
            productionStatus = ProductionStatus(status=status)
            session.add(productionStatus)
        finally:
            await session.commit()
            await session.close()

    async def dell_ProductionStatus(self, id_Production_status: int) -> bool:
        session = await self.get_session()
        try:
            q = select(ProductionStatus).where(ProductionStatus.id_production_status == id_Production_status)
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

    async def edit_ProductionStatus(self, id: int, status: str) -> bool:
        session = await self.get_session()
        try:
            q = select(ProductionStatus).where(ProductionStatus.id_production_status == id)
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

    async def get_ProductionSheets(self) -> List[ProductionSheet]:
        session = await self.get_session()
        try:
            q = select(ProductionSheet)
            productionSheet = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in productionSheet:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()

    async def add_ProductionSheet(self, name: str, id_production_status: int, request_id: int):
        session = await self.get_session()
        try:
            productionSheet = ProductionSheet(name=name, id_production_status=id_production_status, request_id=request_id)
            session.add(ProductionSheet)
        finally:
            await session.commit()
            await session.close()

    async def dell_ProductionSheet(self, id_Production_sheet: int) -> bool:
        session = await self.get_session()
        try:
            q = select(ProductionSheet).where(ProductionSheet.id_production_sheet == id_Production_sheet)
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

    async def edit_ProductionSheet(self, id: int, name: str, id_production_status: int, request_id: int) -> bool:
        session = await self.get_session()
        try:
            q = select(ProductionSheet).where(ProductionSheet.id_production_sheet == id)
            result = await session.execute(q)
            item = result.scalars().unique().first()
            if item is None:
                return False
            else:
                item.name = name
                item.id_production_status = id_production_status
                item.request_id = request_id
                return True
        finally:
            await session.commit()
            await session.close()

db = DataBase()

if __name__ == "__main__":
    tracemalloc.start()
    asyncio.run(DataBase.init_db())
