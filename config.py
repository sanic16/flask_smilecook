import os
from dotenv import load_dotenv

load_dotenv()

db = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}

print(db)

class Config:
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=f'postgresql+psycopg2://{db["user"]}:'\
                            f'{db["password"]}@{db["host"]}:{db["port"]}/{db["database"]}'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
