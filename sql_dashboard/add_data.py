import os
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error


def DBConnect(dbName=None):
    """
    Parameters
    ----------
    dbName :
        Default value = None)
    Returns
    -------
    """
    conn = mysql.connect(host='localhost', user='root', password='my_pass',
                         database=dbName, buffered=True)
    cur = conn.cursor()
    return conn, cur


def emojiDB(dbName: str) -> None:
    conn, cur = DBConnect(dbName)
    dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
    cur.execute(dbQuery)
    conn.commit()


def createDB(dbName: str) -> None:
    """
    Parameters
    ----------
    dbName :
        str:
    dbName :
        str:
    dbName:str :
    Returns
    -------
    """
    conn, cur = DBConnect()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
    conn.commit()
    cur.close()


def createTables(dbName: str) -> None:
    """
    Parameters
    ----------
    dbName :
        str:
    dbName :
        str:
    dbName:str :
    Returns
    -------
    """
    conn, cur = DBConnect(dbName)
    sqlFile = 'day5_schema.sql'
    fd = open(sqlFile, 'r')
    readSqlFile = fd.read()
    fd.close()

    sqlCommands = readSqlFile.split(';')

    for command in sqlCommands:
        try:
            res = cur.execute(command)
        except Exception as ex:
            print("Command skipped: ", command)
            print(ex)
    conn.commit()
    cur.close()

    return


def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parameters
    ----------
    df :
        pd.DataFrame:
    df :
        pd.DataFrame:
    df:pd.DataFrame :
    Returns
    -------
    """
    cols_2_drop = ['IMSI', 'IMEI', 'Start', 'Start ms', 'End', 'End ms', 'Last Location Name', 'Dur. (ms).1',
                   'UL TP > 300 Kbps (%)','50 Kbps < UL TP < 300 Kbps (%)']
    try:
        df = df.drop(columns=cols_2_drop, axis=1)
        df = df.fillna(0)
    except KeyError as e:
        print("Error:", e)

    return df


def db_execute_fetch(*args, many=False, tablename='', rdf=True, **kwargs) -> pd.DataFrame:
    """
    Parameters
    ----------
    *args :
    many :
         (Default value = False)
    tablename :
         (Default value = '')
    rdf :
         (Default value = True)
    **kwargs :
    Returns
    -------
    """
    connection, cursor1 = DBConnect(**kwargs)
    if many:
        cursor1.executemany(*args)
    else:
        cursor1.execute(*args)

    # get column names
    field_names = [i[0] for i in cursor1.description]

    # get column values
    res = cursor1.fetchall()

    # get row count and show info
    nrow = cursor1.rowcount
    if tablename:
        print(f"{nrow} recrods fetched from {tablename} table")

    cursor1.close()
    connection.close()

    # return result
    if rdf:
        return pd.DataFrame(res, columns=field_names)
    else:
        return res


if __name__ == "__main__":
    createDB(dbName='teldata')
    emojiDB(dbName='teldata')
    createTables(dbName='teldata')

    df = pd.read_excel('../Week1_challenge_data_source.xlsx',
                       dtype={'Bearer Id': str, 'IMSI': str, 'MSISDN/Number': str, 'IMEI': str,
                              'Handset Manufacturer': str, 'Handset Type': str}, engine='openpyxl')

    insert_to_tweet_table(dbName='tweets', df=df, table_name='TweetInformation')
