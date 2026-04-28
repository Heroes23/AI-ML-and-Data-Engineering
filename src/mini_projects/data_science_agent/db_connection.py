from os import getcwd, environ
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

# Path to the environment file
env_path = getcwd() + "/src/mini_projects/data_science_agent/.env"

# Load the variables and values
load_dotenv(env_path)

# URL
host = environ.get('POSTGRES_HOST')
user = environ.get('POSTGRES_USER')
password = environ.get('POSTGRES_PASSWORD')
db = environ.get('POSTGRES_DB')
port = environ.get('POSTGRES_PORT')

url = f'postgresql://{user}:{password}@{host}:{port}/{db}'
print(url)
# Engine from SQLAlchemy
engine = create_engine(url=url)

# Database
database = SQLDatabase(engine=engine)

# OpenAI Model
model = ChatOpenAI(model='gpt-5', api_key=environ.get('OPENAI_API_KEY'))

# SQL Toolkit
sql_toolkit = SQLDatabaseToolkit(db=database, llm=model)