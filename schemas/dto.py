from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import date


class StaffCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    contact_number: Optional[str] = Field(None, max_length=15)
    emergency_contact: Optional[str] = Field(None, max_length=15)
    designation_id: Optional[int] = None
    department_id: Optional[int] = None
    address: Optional[str] = None
    date_of_joining: Optional[date] = None
    employment_type: str = Field(default="FULL_TIME")
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=10)
    aadhaar_number: Optional[str] = Field(None, max_length=20)


class StaffUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: Optional[str] = Field(None, min_length=2, max_length=150)
    email: Optional[EmailStr] = None
    contact_number: Optional[str] = Field(None, max_length=15)
    emergency_contact: Optional[str] = Field(None, max_length=15)
    designation_id: Optional[int] = None
    department_id: Optional[int] = None
    address: Optional[str] = None
    date_of_joining: Optional[date] = None
    employment_type: Optional[str] = None
    status: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=10)
    aadhaar_number: Optional[str] = Field(None, max_length=20)


class StaffListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    email: str
    designation_id: Optional[int]
    department_id: Optional[int]
    employment_type: str
    status: str
    date_of_joining: Optional[date]


class StaffOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    full_name: str
    email: str
    contact_number: Optional[str]
    emergency_contact: Optional[str]
    designation_id: Optional[int]
    department_id: Optional[int]
    address: Optional[str]
    date_of_joining: Optional[date]
    employment_type: str
    status: str
    date_of_birth: Optional[date]
    gender: Optional[str]
    aadhaar_number: Optional[str]


class StaffDesignationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: str
    is_active: bool


class BulkResponse(BaseModel):
    success_count: int
    error_count: int
    errors: list[str]
