from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum


class Account(BaseModel):
    id: Optional[UUID] = None
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    bank_name: Optional[str] = None
    account_type: Optional[str] = None
    balance: Optional[float] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    ifsc_code: Optional[str] = None
    branch_name: Optional[str] = None
    description: Optional[str] = None


class Budget(BaseModel):
    id: Optional[UUID] = None
    year: Optional[int] = None
    month: Optional[int] = None
    amount: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ExportInfo(BaseModel):
    export_date: Optional[datetime] = None
    app_version: Optional[str] = None
    data_format: Optional[str] = None
    total_transactions: Optional[int] = None
    total_accounts: Optional[int] = None
    total_budgets: Optional[int] = None


class Category(Enum):
    OTHER = "other"
    TRANSFER = "transfer"


class TypeEnum(Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    TRANSFER = "transfer"


class Transaction(BaseModel):
    id: Optional[UUID] = None
    date: Optional[datetime] = None
    type: Optional[TypeEnum] = None
    title: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[Category] = None
    location: Optional[str] = None
    photos: Optional[List[Any]] = None
    sms_content: Optional[str] = None
    account_id: Optional[UUID] = None


class FinanceInfo(BaseModel):
    export_info: Optional[ExportInfo] = None
    transactions: Optional[List[Transaction]] = None
    accounts: Optional[List[Account]] = None
    budgets: Optional[List[Budget]] = None
