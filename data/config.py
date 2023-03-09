import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = '5733192318:AAGJAH6rAfxPaVvgeL2bjMmLmiY-_SSiR54'

admins_id = [
    720207278
]
IP = 'localhost'
PGUSER = 'postgres'
PGPASSWORD = 'adminpass123'
DATABASE = 'gino'
POSTGRES_URI = f'postgresql://postgres:adminpass123@localhost/gino'

print(f'{BOT_TOKEN}, {IP}, {PGUSER}, {PGPASSWORD}, {DATABASE}, {POSTGRES_URI}')