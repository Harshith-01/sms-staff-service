from sqlalchemy import (
    Boolean, Column, Date, ForeignKey, Integer,
    String, Text, TIMESTAMP, CheckConstraint, SmallInteger, BigInteger, Time
)
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String(20), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    role_name = Column(String(50), unique=True, nullable=False)


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = Column(String(20), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class StaffDesignation(Base):
    __tablename__ = "staff_designations"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=False, default="SUPPORT")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())


class NonTeachingStaff(Base):
    __tablename__ = "non_teaching_staff"

    id = Column(String(20), primary_key=True)
    user_id = Column(String(20), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    designation_id = Column(Integer, ForeignKey("staff_designations.id", ondelete="SET NULL"))
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))

    email = Column(String(255), nullable=False)
    contact_number = Column(String(15))
    emergency_contact = Column(String(15))
    address = Column(Text)

    date_of_joining = Column(Date)
    employment_type = Column(String(50), nullable=False, default="FULL_TIME")
    status = Column(String(30), nullable=False, default="ACTIVE")

    date_of_birth = Column(Date)
    gender = Column(String(10))
    aadhaar_number = Column(String(20))

    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    designation = relationship("StaffDesignation")
    department = relationship("Department")

    __table_args__ = (
        CheckConstraint(
            "employment_type IN ('FULL_TIME','PART_TIME','CONTRACT','DAILY_WAGE')",
            name="chk_staff_employment_type",
        ),
        CheckConstraint(
            "status IN ('ACTIVE','INACTIVE','TERMINATED','ON_LEAVE')",
            name="chk_staff_status",
        ),
    )


# Reference-only for timetable read
class TimetableEntry(Base):
    __tablename__ = "timetable_entries"
    id = Column(BigInteger, primary_key=True)
    academic_term_id = Column(Integer, ForeignKey("academic_terms.id", ondelete="CASCADE"), nullable=False)
    class_section_id = Column(Integer, ForeignKey("class_sections.id", ondelete="CASCADE"), nullable=False)
    weekday = Column(SmallInteger, nullable=False)
    period_no = Column(SmallInteger, nullable=False)
    subject_id = Column(Integer, nullable=False)
    teacher_id = Column(String(20), nullable=False)
    room_code = Column(String(30))
    entry_type = Column(String(20), nullable=False, default="REGULAR")
    is_active = Column(Boolean, nullable=False, server_default=text("true"))


class AcademicTermRef(Base):
    __tablename__ = "academic_terms"
    id = Column(Integer, primary_key=True)


class ClassSectionRef(Base):
    __tablename__ = "class_sections"
    id = Column(Integer, primary_key=True)
