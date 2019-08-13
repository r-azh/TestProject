
# the Session establishes all conversations with the database and represents a “holding zone” for all the objects which
# you’ve loaded or associated with it during its lifespan. It provides the entrypoint to acquire a Query object, which
# sends queries to the database using the Session object’s current database connection, populating result rows into
# objects that are then stored in the Session, inside a structure called the Identity Map - a data structure that
# maintains unique copies of each object, where “unique” means “only one object with a particular primary key”.
from bson import ObjectId

from sqlalchemy.ext.declarative import declarative_base

print('################################## session create ############################################')

from sqlalchemy import create_engine, String, Column
from sqlalchemy.orm import sessionmaker

# an Engine, which the Session will use for connection resources
some_engine = create_engine('postgresql+psycopg2://postgres:123456@localhost/postgres')

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

# create a Session
session = Session()

Base = declarative_base()


class FooBar(Base):
    __tablename__ = 'foobar'
    id = Column(String, primary_key=True)
    foo = Column(String)
    bar = Column(String)

    def __init__(self, foo, bar):
        self.id = str(ObjectId())
        self.foo = foo
        self.foo = bar

Base.metadata.create_all(bind=some_engine)

# work with session
myobject = FooBar('foo', 'bar')
session.add(myobject)
session.commit()

print('################################## add config to session ############################################')
# Adding Additional Configuration to an Existing sessionmaker()

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# configure Session class with desired options
Session = sessionmaker()

# later, we create the engine
engine = create_engine('postgresql+psycopg2://postgres:123456@localhost/postgres')

# associate it with our custom Session class
Session.configure(bind=engine)

# work with the session
session = Session()


print('################################## ad-hoc session ############################################')
# Creating Ad-Hoc Session Objects with Alternate Arguments
# for special cases such as a Session that binds to an alternate source of connectivity, or a Session that should have
# other arguments such as expire_on_commit established differently from what most of the application wants

# at the module level, the global sessionmaker,
# bound to a specific Engine
Session = sessionmaker(bind=engine)

# later, some unit of code wants to create a
# Session that is bound to a specific Connection
conn = engine.connect()
session = Session(bind=conn)


# # # When do I make a sessionmaker?
# - Just one time, somewhere in your application’s global scope. It should be looked upon as part of your
# application’s configuration.

# - If your application starts up, does imports, but does not know what database it’s going to be connecting to, you can
#  bind the Session at the “class” level to the engine later on, using sessionmaker.configure().

# # # When do I construct a Session, when do I commit it, and when do I close it?
# 1- As a general rule, keep the lifecycle of the session separate and external from functions and objects that access
# and/or manipulate database data. This will greatly help with achieving a predictable and consistent transactional scope.
# 2- Make sure you have a clear notion of where transactions begin and end, and keep transactions short, meaning,
# they end at the series of a sequence of operations, instead of being held open indefinitely.

# Keep the lifecycle of the session (and usually the transaction) separate and external. For example, we can further
# separate concerns using a context manager:

from contextlib import contextmanager


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class ThingOne(object):
    def go(self, session):
        session.query(FooBar).update({"foo": 5})


class ThingTwo(object):
    def go(self, session):
        session.query(FooBar).update({"bar": 18})


def run_my_program():
    with session_scope() as session:
        ThingOne().go(session)
        ThingTwo().go(session)


# How can I get the Session for a certain object?
session = Session.object_session(myobject)

# or the newer Runtime Inspection API system can also be used:
# Runtime Inspection API:  The inspection module provides the inspect() function, which delivers runtime information
# about a wide variety of SQLAlchemy objects, both within the Core as well as the ORM.
from sqlalchemy import inspect
session = inspect(myobject).session


# Is the session thread-safe?
# The Session is very much intended to be used in a non-concurrent fashion, which usually means in only one thread at a time.
# The Session should be used in such a way that one instance exists for a single series of operations within a single
# transaction by:
# - by associating a Session with the current thread
# - Another is to use a pattern where the Session is passed between functions and is otherwise not shared with other
# threads.
# The bigger point is that you should not want to use the session with multiple concurrent threads. That would be like
#  having everyone at a restaurant all eat from the same plate.



# 1-Create a single scoped_session registry when the web application first starts, ensuring that this object is
#  accessible by the rest of the application.
# 2-Ensure that scoped_session.remove() is called when the web request ends, usually by integrating with the web
#  framework’s event system to establish an “on request end” event.
# the above pattern is just one potential way to integrate a Session with a web framework, one which in particular
#  makes the significant assumption that the web framework associates web requests with application threads.