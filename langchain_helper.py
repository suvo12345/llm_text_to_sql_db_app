import os
import google.generativeai as palm
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
# import pymysql
import urllib

from langchain_core.output_parsers.list import CommaSeparatedListOutputParser
from langchain_core.prompts.prompt import PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain

load_dotenv()

def get_few_shot_db_chain():


    llm = GoogleGenerativeAI(model="models/gemini-1.0-pro", google_api_key=os.getenv('google_api_key'), temperature=0.2)

    PROMPT_SUFFIX = """Only use the following tables:
                        {table_info}

                        Question: {input}"""

    _mysql_prompt = """You are a MySQL expert. 
                Given an input question, always remove the prefix "sql" from the start of the query and create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
                Unless the user specifies a limit in the question to extract specofic number of rows, query for at most {top_k} results using the LIMIT clause as per MySQL. 
                You can order the results to return the most informative data in the database.
                Never query for all columns from a table. You must query only the columns that are needed to answer the question. 
                Wrap each column name in backticks (`) to denote them as delimited identifiers.
                Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
                Pay attention to use CURDATE() function to get the current date, if the question involves "today". 
                stock field defines the number of t-shirts left so total t-shirts left will be summation of stock field.

                Use the following format:

                Question: Question here
                SQLQuery: SQL Query to run
                SQLResult: Result of the SQLQuery
                Answer: SQLResult in a table format

                """

    MYSQL_PROMPT = PromptTemplate(
                    input_variables=["input", "table_info", "top_k"],
                    template=_mysql_prompt + PROMPT_SUFFIX,
                )

    db_user="root"
    db_password="suvo@1987"
    db_password_updated = urllib.parse.quote_plus(db_password)
    db_host="localhost"
    db_name="atliq_tshirts"

    db = SQLDatabase.from_uri(f"mysql+mysqlconnector://root:{db_password_updated}@{db_host}/{db_name}", 
                                    sample_rows_in_table_info=3)

    # print(db.table_info)



    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, use_query_checker=True, prompt=MYSQL_PROMPT)
    # chain = db_chain("Give me all Levi’s T-shirts revenue post discount?")

    return db_chain
