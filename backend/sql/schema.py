from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from backend.sql.database import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    manager = Column(String(100))

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    role = Column(String(100))
    joining_date = Column(Date)
    salary = Column(Float)
    status = Column(String(50), default="Active")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date)
    status = Column(String(50))
    hours_worked = Column(Float)

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    leave_type = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(50))

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    category = Column(String(100))
    amount = Column(Float)
    date = Column(Date)
    status = Column(String(50))
    description = Column(String(255))
