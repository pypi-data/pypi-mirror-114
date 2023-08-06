from datetime import datetime
import hashlib
from more_itertools import lstrip
import pandas as pd
from typing import List
import uuid

def hash_string(input_string: str) -> int:
    """
    This function accepts a string and returns an 8 digit integer representation
    Method: generate a sha256 hash of the string and use modulo division to truncate it's integer representation to 8 digits

    WARNING:
    This function WILL return the same integer value for a string each time it is passed in the same session
    This function WILL NOT return a unique value for every unique string combination
    """
    return int(hashlib.sha256(input_string.encode('utf-8')).hexdigest(), 16) % 10**8

def hash_list(input_list: List[str]) -> int:
    """This function accepts a list of strings and returns an 8 digit integer representation"""
    input_string = ''.join(input_list)
    return hash_string(input_string)

def make_timestamp() -> str:
    now = datetime.now()
    return now.strftime("%Y_%m_%d_%H_%M")

def parse_fqtn(fqtn: str) -> tuple:
    """
    Accepts a possible fully qualified table string and returns its component parts
    """
    database = None
    schema = None
    table = fqtn
    if fqtn.count('.') == 2:
        database = fqtn.split(".")[0]
        schema = fqtn.split(".")[1]
        table = fqtn.split(".")[-1]
    elif fqtn.count('.') == 1:
        schema = fqtn.split(".")[0]
        table = fqtn.split(".")[-1]
    return database, schema, table

def random_table_name() -> str:
    identifier = str(uuid.uuid4())
    table_name = ''.join(list(lstrip(hashlib.md5(identifier.encode('utf-8')).hexdigest(),
                            lambda x: x.isnumeric()))).upper()
    return table_name

def _cleanse_sql_data_type(dtype: str) -> str:
    """
    Converts a string to Snowflake compliant data type
    """
    if dtype.lower() in ["object", "text"]:
        return "string"
    else:
        return dtype.lower()

def _cleanse_sql_list(list_in: List[str]) -> List[str]:
    """
    Converts a list of strings to Snowflake compliant names
    """
    return [_cleanse_sql_name(n) for n in list_in]

def _cleanse_sql_name(name: str) -> str:
    """
    Converts a string to a snowflake compliant value
    """
    return name.replace(" ", "_").replace("-", "_").replace('"', '').replace(".","_").upper()

def _is_scary_sql(sql: str) -> str:
    """
    Checks a SQL string for presence of dangerous keywords
    """
    scary_sql_words = ["DELETE",
                       "TRUNCATE",
                       "DROP",
                       "ALTER",
                       "UPDATE",
                       "INSERT"]
    if any(word in sql.upper() for word in scary_sql_words):
        return True
    return False

def _is_valid_view_sql(sql: str) -> str:
    """
    Checks a SQL string for presence of structural keywords
    """
    mandatory_words = ["SELECT", "FROM"]
    if not all(word in sql.upper() for word in mandatory_words):
        return False
    return True