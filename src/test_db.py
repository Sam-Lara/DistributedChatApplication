from peer import Peer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
import threading
from database import Database
import random

# Define the connection parameters
username = "postgres"
password = "RuntotheSun10"
host_url = "localhost"
port = 5432
database_name = "postgres"
app_schema = "chat"

# Create the SQLAlchemy engine
connection_string = f"postgresql+psycopg2://{username}:{password}@{host_url}:{port}/{database_name}"
db = create_engine(connection_string, connect_args={"options": f"-csearch_path={app_schema}"})

print(Database.get_used_ports(db))
