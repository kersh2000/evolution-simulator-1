import os
from dotenv import load_dotenv

load_dotenv('.env')

server_port = int(os.getenv('SERVER_PORT', 8000))

database_hostname = os.getenv('DB_HOSTNAME')
database_name = os.getenv('DB_NAME')
database_password = os.getenv('DB_PASSWORD')
database_username = os.getenv('DB_USERNAME')

jwt_secret = os.getenv('SECRET_KEY')
jwt_algorithm = os.getenv('ALGORITHM')
jwt_expire_mins = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))