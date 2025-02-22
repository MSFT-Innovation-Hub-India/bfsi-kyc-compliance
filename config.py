import os
from dotenv import load_dotenv
load_dotenv()

class DefaultConfig:
    server = 'contosobank.database.windows.net'
    database = 'transactions'
    username = 'contosoadmin'
    password = 'M1cr0s0ft'
    driver = '{ODBC Driver 18 for SQL Server}'

    PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
    MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")
    BING_CONNECTION_NAME = os.getenv("BING_CONNECTION_NAME")

