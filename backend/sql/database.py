from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from backend.sql import schema
    Base.metadata.create_all(bind=engine)
    
    # Seed data if empty
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM employees"))
        if result.scalar() == 0:
            seed_data(conn)
        conn.commit()

def seed_data(conn):
    conn.execute(text("""
        INSERT INTO departments (id, name, manager) VALUES 
        (1, 'Engineering', 'Alice Smith'),
        (2, 'HR', 'Bob Johnson'),
        (3, 'Sales', 'Charlie Brown'),
        (4, 'Marketing', 'Diana Prince')
    """))
    conn.execute(text("""
        INSERT INTO employees (id, name, department_id, role, joining_date, salary, status) VALUES
        (1, 'Dave', 1, 'Senior Developer', '2022-01-10', 120000, 'Active'),
        (2, 'Eve', 1, 'Developer', '2023-03-15', 95000, 'Active'),
        (3, 'Frank', 2, 'Recruiter', '2021-11-20', 70000, 'Active'),
        (4, 'Grace', 3, 'Sales Lead', '2020-05-01', 110000, 'Active'),
        (5, 'Hank', 1, 'QA Engineer', '2023-06-10', 85000, 'Active'),
        (6, 'Ivy', 4, 'Marketing Manager', '2019-02-15', 105000, 'Active')
    """))
    conn.execute(text("""
        INSERT INTO leave_requests (id, employee_id, leave_type, start_date, end_date, status) VALUES
        (1, 1, 'Annual', '2023-12-20', '2023-12-31', 'Approved'),
        (2, 2, 'Sick', '2023-10-01', '2023-10-02', 'Approved'),
        (3, 4, 'Annual', '2024-01-15', '2024-01-20', 'Pending'),
        (4, 1, 'Sick', '2024-02-10', '2024-02-12', 'Approved')
    """))
    conn.execute(text("""
        INSERT INTO expenses (id, employee_id, category, amount, date, status, description) VALUES
        (1, 4, 'Travel', 1500.00, '2023-08-15', 'Approved', 'Client visit to NY'),
        (2, 1, 'Hardware', 1200.00, '2023-09-01', 'Approved', 'New MacBook Pro'),
        (3, 6, 'Marketing', 5000.00, '2023-11-05', 'Approved', 'Ad campaign'),
        (4, 2, 'Hardware', 200.00, '2024-01-10', 'Pending', 'Monitor')
    """))
    conn.execute(text("""
        INSERT INTO attendance (id, employee_id, date, status, hours_worked) VALUES
        (1, 1, '2024-02-01', 'Present', 8.0),
        (2, 2, '2024-02-01', 'Present', 8.0),
        (3, 3, '2024-02-01', 'Present', 7.5),
        (4, 4, '2024-02-01', 'Absent', 0.0),
        (5, 1, '2024-02-02', 'Present', 8.5),
        (6, 2, '2024-02-02', 'Present', 8.0)
    """))

def get_schema():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    schema = {}
    for table_name in tables:
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col['name'] for col in columns]
    return schema

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
