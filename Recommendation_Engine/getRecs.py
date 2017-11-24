import MySQLdb

def testConn():
    conn = MySQLdb.connect(
        host="kenkosqlinstance.cxgcdmduizhx.us-east-1.rds.amazonaws.com", 
        user="", 
        passwd="", 
        db="KenkoDB"
    )
    cursor = conn.cursor()

    cursor.execute('show tables')
    row = cursor.fetchone()

    conn.close()

    print(row)


if __name__=="__main__":
    testConn()