import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = 'bot_token'

admins_id = [
    int("admins_id")
]
IP = 'localhost'
PGUSER = 'postgres'
PGPASSWORD = 'data_base_password'
DATABASE = 'gino'
POSTGRES_URI = f'postgresql://postgres:adminpass123@localhost/gino'

print(f'{BOT_TOKEN}, {IP}, {PGUSER}, {PGPASSWORD}, {DATABASE}, {POSTGRES_URI}')