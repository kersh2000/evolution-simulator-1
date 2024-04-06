import os
from dotenv import load_dotenv

load_dotenv('.env')

jwt_secret = os.getenv('SECRET_KEY')
jwt_algorithm = os.getenv('ALGORITHM')
jwt_expire_mins = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
