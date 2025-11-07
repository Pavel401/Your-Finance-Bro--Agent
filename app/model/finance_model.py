from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum


class Account(BaseModel):
    id: Optional[UUID] = None
    account_name: Optional[str] = Field(None, alias="accountName")
    account_number: Optional[str] = Field(None, alias="accountNumber")
    bank_name: Optional[str] = Field(None, alias="bankName")
    account_type: Optional[str] = Field(None, alias="accountType")
    balance: Optional[float] = None
    is_active: Optional[bool] = Field(None, alias="isActive")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    ifsc_code: Optional[str] = Field(None, alias="ifscCode")
    branch_name: Optional[str] = Field(None, alias="branchName")
    description: Optional[str] = None

    class Config:
        populate_by_name = True


class Budget(BaseModel):
    id: Optional[UUID] = None
    year: Optional[int] = None
    month: Optional[int] = None
    amount: Optional[float] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    class Config:
        populate_by_name = True


class ExportInfo(BaseModel):
    export_date: Optional[datetime] = Field(None, alias="exportDate")
    app_version: Optional[str] = Field(None, alias="appVersion")
    data_format: Optional[str] = Field(None, alias="dataFormat")
    total_transactions: Optional[int] = Field(None, alias="totalTransactions")
    total_accounts: Optional[int] = Field(None, alias="totalAccounts")
    total_budgets: Optional[int] = Field(None, alias="totalBudgets")

    class Config:
        populate_by_name = True


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
    sms_content: Optional[str] = Field(None, alias="smsContent")
    account_id: Optional[UUID] = Field(None, alias="accountId")

    class Config:
        populate_by_name = True


class FinanceInfo(BaseModel):
    export_info: Optional[ExportInfo] = Field(None, alias="exportInfo")
    transactions: Optional[List[Transaction]] = None
    accounts: Optional[List[Account]] = None
    budgets: Optional[List[Budget]] = None

    class Config:
        populate_by_name = True
