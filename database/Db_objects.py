from __future__ import annotations
import datetime
from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Any, List


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = 'Client'
    id_client: Mapped[int] = mapped_column(primary_key=True)
    FIO: Mapped[str]
    INN: Mapped[str]
    phone: Mapped[str]
    requests: Mapped[List["Request"]] = relationship()


class Lawyer(Base):
    __tablename__ = 'Lawyer'
    id_lawyer: Mapped[int] = mapped_column(primary_key=True)
    FIO: Mapped[str]
    salary: Mapped[str]
    requests: Mapped[List["Request"]] = relationship()


class PaymentStatus(Base):
    __tablename__ = 'Payment_status'
    id_payment_status: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]
    payments: Mapped[List["Payment"]] = relationship()


class Payment(Base):
    __tablename__ = 'Payment'
    id_payment: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[str]
    id_payment_status: Mapped[int] = mapped_column(ForeignKey("Payment_status.id_client"))
    requests: Mapped[List["Request"]] = relationship()


class ContractStatus(Base):
    __tablename__ = 'Contract_status'
    id_contract_status: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]
    contracts: Mapped[List["Contract"]] = relationship()


class Contract(Base):
    __tablename__ = 'Contract'
    id_contract: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str]
    id_contract_status: Mapped[int] = mapped_column(ForeignKey("Contract_status.id_contract_status"))
    requests: Mapped[List["Request"]] = relationship()


class RequestStatus(Base):
    __tablename__ = 'Request_status'
    id_request_status: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]
    requests: Mapped[List["Request"]] = relationship()


class Request(Base):
    __tablename__ = 'Request'
    id_request: Mapped[int] = mapped_column(primary_key=True)
    id_client: Mapped[int] = mapped_column(ForeignKey("Client.id_client"))
    id_request_status: Mapped[int] = mapped_column(ForeignKey("Request_status.id_request_status"))
    id_contract: Mapped[int] = mapped_column(ForeignKey("Contract.id_contract"))
    id_payment: Mapped[int] = mapped_column(ForeignKey("Payment.id_payment"))
    id_lawyer: Mapped[int] = mapped_column(ForeignKey("Payment.id_lawyer"))
    production_sheet: Mapped["ProductionSheet"] = relationship(back_populates="parent")


class ProductionStatus(Base):
    __tablename__ = 'Production_status'
    id_production_status: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]
    production_sheets: Mapped[List["ProductionSheet"]] = relationship()


class ProductionSheet(Base):
    __tablename__ = 'Production_sheet'
    id_production_sheet: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    id_production_status: Mapped[int] = mapped_column(ForeignKey("Production_status.id_production_status"))
    request_id: Mapped[int] = mapped_column(ForeignKey("Request.id_request"))
    request: Mapped["Request"] = relationship(back_populates="child")
    production_steps_in_sheet: Mapped["ProductionStepsInSheet"] = relationship(back_populates="parent")



class Competence(Base):
    __tablename__ = 'Competence'
    id_competence: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Brewer(Base):
    __tablename__ = 'Brewer'
    id_brewer: Mapped[int] = mapped_column(primary_key=True)
    FIO: Mapped[str]
    salary: Mapped[int]


class Parameter(Base):
    __tablename__ = 'Parameter'
    id_parameter: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Equipment(Base):
    __tablename__ = 'Equipment'
    id_equipment: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    resource: Mapped[str]


class EquipmentParameters(Base):
    __tablename__ = 'Equipment_parameters'
    id_equipment_parameters: Mapped[int] = mapped_column(primary_key=True)
    val: Mapped[str]
    data_time: Mapped[str]


class ProductionStep(Base):
    __tablename__ = 'Production_step'
    id_production_step: Mapped[int] = mapped_column(primary_key=True)
    data_time: Mapped[str]
    log: Mapped[str]


class ProductionStepsInSheet(Base):
    __tablename__ = 'Production_steps_in_sheet'
    id_production_steps_in_sheet: Mapped[int] = mapped_column(primary_key=True)


class Spoilage(Base):
    __tablename__ = 'Spoilage'
    id_spoilage: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[str]
    item: Mapped[str]
