from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define the base class for model classes
Base = declarative_base()

# Define the User class
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(30))
    password = Column(String(30))
    online = Column(Boolean)
    ip_addr = Column(String(50))
    port = Column(Integer)


# Define the Message class
class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP, default=datetime.now)
    sender_id = Column(Integer, ForeignKey('users.user_id'))
    receiver_id = Column(Integer, ForeignKey('users.user_id'))
    message_text = Column(String)


class Database:
    @staticmethod
    def get_user_id(db, ip_addr, port):
        Session = sessionmaker(bind=db)
        with Session() as session:
            query = select(User.user_id).where((User.ip_addr == ip_addr) & (User.port == port))
            result = session.execute(query)
            user_id = result.scalar()
            return user_id

    @staticmethod
    def log_in(db, username, password):
        with db.connect() as conn:
            query = select(User).filter_by(user_name=username, password=password)
            result = conn.execute(query).fetchone()
            if result:
                # Extract attributes from the result and create a User object
                user_id, user_name, password, online, ip_addr, port = result
                user = User(user_id=user_id, user_name=user_name, password=password, online=online, ip_addr=ip_addr, port=port)
                return user
            else:
                return None

    @staticmethod
    def signup(db, user_name, password, ip_addr, port):
        Session = sessionmaker(bind=db)
        with Session() as session:
            new_user = User(user_name=user_name, password=password, online=True, ip_addr=ip_addr, port=port)
            session.add(new_user)
            session.commit()

    @staticmethod
    def update_user_connection(db, user_name, ip_addr, port):
        Session = sessionmaker(bind=db)
        with Session() as session:
            user = session.query(User).filter_by(user_name=user_name).first()
            if user:
                user.ip_addr = ip_addr
                user.port = port
                session.commit()

    @staticmethod
    def update_user_status(db, user_name):
        Session = sessionmaker(bind=db)
        with Session() as session:
            user = session.query(User).filter_by(user_name=user_name).first()
            if user:
                user.online = True
                session.commit()

    @staticmethod
    def get_active_users(db):
        Session = sessionmaker(bind=db)
        with Session() as session:
            users = session.query(User.user_name).all()
            return [user.user_name for user in users]

    @staticmethod
    def get_user(db, username):
        with db.connect() as conn:
            query = select(User).filter_by(user_name=username)
            result = conn.execute(query).fetchone()
            if result:
                # Extract attributes from the result and create a User object
                user_id, user_name, password, online, ip_addr, port = result
                user = User(user_id=user_id, user_name=user_name, password=password, online=online, ip_addr=ip_addr, port=port)
                return user
            else:
                return None

    @staticmethod
    def add_message(db, sender_id, receiver_id, message_text):
        Session = sessionmaker(bind=db)
        with Session() as session:
            new_message = Message(sender_id=sender_id, receiver_id=receiver_id, message_text=message_text)
            session.add(new_message)
            session.commit()

    @staticmethod
    def get_used_ports(db):
        with db.connect() as conn:
            query = select(User.port).distinct()
            result = conn.execute(query)
            port_numbers = [row[0] for row in result.fetchall()]
            return port_numbers
