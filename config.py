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
    SECRET_KEY='67d57e074eef3689893ec2a7d2f324b0d572d18730e72a092b540891836f2d7047e358a7064f2fcd528153cfaad0e52892b1a520c81fdda3bb086fa8a9d1e64c3320a931b9e5cbcdc6179ec1d4c2dc12bf7bb4ab4a5dbd1f2569117dd92f3f91354083de190e70b0d19d896c1b8d6a76807cbcc93cac958b27ba100a01477e716d03bfad6441eb84d076b823924a84af3f2ceb415d2148d1211028d796c17cee37e01c227a2b3ccfea2e1a00f24a9a3d6e5184319cbd7e2cadf9f8147459c2f0574bcbb354f7a18f045f857f1af4d8eb449d315c7850bd1e374a334ac9c9a97020e451a1d3ee66ec166fbe2d1a822ee7aeb552bb702f89fe3fd6611c351dd7f0'
    JWT_ERROR_MESSAGE_KEY='message'

    JWT_ACCESS_TOKEN_EXPIRES=60*60*24*1

