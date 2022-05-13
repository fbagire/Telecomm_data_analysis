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
    conn = mysql.connect(host='localhost', user='root', password='fefe@888',
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
                   'UL TP > 300 Kbps (%)', '50 Kbps < UL TP < 300 Kbps (%)']
    try:
        df = df.drop(columns=cols_2_drop, axis=1)
    except KeyError as e:
        print("Error:", e)

    return df


def insert_to_tweet_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:
    """
    Parameters
    ----------
    dbName :
        str:
    df :
        pd.DataFrame:
    table_name :
        str:
    dbName :
        str:
    df :
        pd.DataFrame:
    table_name :
        str:
    dbName:str :
    df:pd.DataFrame :
    table_name:str :
    Returns
    -------
    """
    conn, cur = DBConnect(dbName)

    df = preprocess_df(df)

    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO {table_name} ("Bearer Id","MSISDN/Number","Avg RTT DL (ms)", "Avg RTT UL (ms)",
        "10 Kbps < UL TP < 50 Kbps (%)","250 Kbps < DL TP < 1 Mbps (%)","50 Kbps < DL TP < 250 Kbps (%)",
        "Activity Duration DL (ms)","Activity Duration UL (ms)","Avg Bearer TP DL (kbps)","Avg Bearer TP UL (kbps)",
        "DL TP < 50 Kbps (%)","DL TP > 1 Mbps (%)","Dur. (s)","Email DL (Bytes)","Email Total (megabytes)",
        "Email UL (Bytes)","Gaming DL (Bytes)","Gaming Total (megabytes)","Gaming UL (Bytes)","Google DL (Bytes)",
        "Google Total (megabytes)","Google UL (Bytes)","Handset Manufacturer","Handset Type","Nb of sec with Vol DL < 6250B",
        "Nb of sec with Vol UL < 1250B","Netflix DL (Bytes)","Netflix Total (megabytes)","Netflix UL (Bytes)",
        "Other DL (Bytes)", "Other Total (megabytes)", "Other UL (Bytes)","Social Media DL (Bytes)", "Social Media Total (megabytes)",
        "Social Media UL (Bytes)","Total DL (Bytes)","Total Data (megabytes)","Total UL (Bytes)","UL TP < 10 Kbps (%)",
        "Youtube DL (Bytes)","Youtube Total (megabytes)","Youtube UL (Bytes)")
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
                row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22],
                row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33],
                row[34], row[35], row[36], row[37], row[38], row[39], row[40], row[41], row[42])

        try:
            # Execute the SQL command
            cur.execute(sqlQuery, data)
            # Commit your changes in the database
            conn.commit()
            print("Data Inserted Successfully")
        except Exception as e:
            conn.rollback()
            print("Error: ", e)
    return


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
        print(f"{nrow} records fetched from {tablename} table")

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

    df = pd.read_excel('../Week1_challenge_data_cleaned.xlsx',
                       dtype={'Bearer Id': str, 'IMSI': str, 'MSISDN/Number': str, 'IMEI': str,
                              'Handset Manufacturer': str, 'Handset Type': str}, engine='openpyxl')

    insert_to_tweet_table(dbName='teldata', df=df, table_name='TelcomData')
