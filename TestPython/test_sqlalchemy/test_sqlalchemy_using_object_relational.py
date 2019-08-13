from sqlalchemy import Column, Integer, String, func, DateTime, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

__author__ = 'R.Azh'

Base = declarative_base()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # use default=func.now() to set the default hiring time
    # of an Employee to be the current time when an Employee record was created
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    # Use cascade='delete, all' to propagate the deletion of a Department onto its Employees
    department = relationship(
        Department,
        backref=backref('employees',
                        uselist=True,
                        cascade='delete,all')
    )


from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:123456@localhost/postgres')

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)


print('############################## creating tables using Base #####################################')

#  to create tables in db: creates all tables in the db which are defined by Base's subclasses
# if Table Models have been defined in different modules(files) we should import all Table models before calling the
# next line to be created in db
Base.metadata.create_all(bind=engine)

# drop table
# Employee.__table__.drop(engine)


print('################################## some queries ############################################')

d = Department(name='IT')
emp1 = Employee(name='John', department=d)
s = session()
s.add(d)
s.add(emp1)

s.commit()

s.delete(d)
s.commit()

r = s.query(Employee).all()
for row in r:
    print(row)

emp2 = Employee(name='Marry')
print(emp2.hired_on)
s.add(emp2)
print(emp2.hired_on)
s.commit()
# hired_on gets value after commit because func.now() will translate into sql now()
print(emp2.hired_on)

rs = s.execute(select([func.now()]))
print(rs.fetchone())

for dep in s.query(Department).all():
    s.delete(dep)
for emp in s.query(Employee).all():
    s.delete(emp)
s.commit()

print(s.query(Department).count())
print(s.query(Employee).count())


it = Department(name='IT')
financial = Department(name='Financial')
john = Employee(name='John', department=it)
marry = Employee(name='Marry', department=financial)

s.add(it)
s.add(financial)
s.add(john)
s.add(marry)
s.commit()

cathy = Employee(name='Cathy', department=financial)
s.add(cathy)
s.commit()

r = s.query(Employee).filter(Employee.name.startswith('C')).one().name
print(r)
r = s.query(Employee).join(Employee.department).filter(Employee.name.startswith('C'),
                                                       Department.name == 'Financial').all()[0].name
print(r)

r = s.query(Employee).filter(Employee.hired_on > func.now()).count()
print(r)

r = s.query(Employee).filter(Employee.hired_on < func.now()).count()
print(r)


print('############################### many to many ##################################')


class Department2(Base):
    __tablename__ = 'department2'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    employees = relationship('Employee2', secondary='department_employee_link')


class Employee2(Base):
    __tablename__ = 'employee2'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    departments = relationship(Department2, secondary='department_employee_link')


class DepartmentEmployeeLink(Base):
    __tablename__ = 'department_employee_link'
    department_id = Column(Integer, ForeignKey('department2.id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee2.id'), primary_key=True)


Base.metadata.create_all(bind=engine)

print('################################## some queries ############################################')

it = Department2(name='IT')
financial = Department2(name='Financial')
john = Employee2(name='John')
marry = Employee2(name='Marry')
cathy = Employee2(name='Cathy')
cathy.departments.append(financial)
financial.employees.append(marry)
john.departments.append(it)
s.add(it)
s.add(financial)
s.add(john)
s.add(marry)
s.add(cathy)
s.commit()

print('############## updating with object ####################')
# updating value
john.name = 'Johny'
s.commit()
r = s.query(Employee2).filter(Employee2.name == 'Johny').all()[0].name
print(r)
r = s.query('employee2')
print('query:', r)

print(cathy.departments[0].name)
print(marry.departments[0].name)
print(john.departments[0].name)
print(list(e.name for e in it.employees))
print(list(e.name for e in financial.employees))


print('############## query ###################')

r = s.query(Employee2).filter(Employee2.departments.any(Department2.name == 'IT')).all()[0].name
print(r)

r = s.query(Department2).filter(Department2.employees.any(Employee2.name == 'John'))
print(r)

r = s.execute('select * from department')
print([r for r in r])

result = s.execute("select * from department where name=:name", {'name': 'IT'})
print([r for r in result])

# execute a SQL expression construct
result = s.execute(select([Department]).where(Department.name == 'Financial'))
print([r for r in result])
