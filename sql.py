import mysql.connector as ms

def establish_connection():
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '@Candiceland1234',
        'database': 'parking_info',
    }

    try:
        con = ms.connect(**config)
        if con.is_connected():
            cur = con.cursor()
            return con, cur  # Return the connection and cursor
    except ms.Error as e:
        print(f"Connection not established: {e}")
        return None, None  # Return None if connection is not established
    

################################################################################################################

def add_user(username, password, email, full_name):
    con, cur = establish_connection()
    if con and cur:
        try:
            query = "INSERT INTO signup_info (username, password, email, full_name) VALUES (%s, %s, %s, %s)"
            values = (username, password, email, full_name)
            cur.execute(query, values)
            con.commit()
            return True
        except ms.Error as e:
            print(f"Failed to insert record into MySQL table: {e}")
            return False
        finally:
            cur.close()
            con.close()
    return False

####################################################################################################################

def check_login(username, password):
    con, cur = establish_connection()
    if con and cur:
        try:
            username = username.strip()
            password = password.strip()

            query = "SELECT * FROM signup_info WHERE username = %s AND password = %s"
            values = (username, password)

            cur.execute(query, values)
            result = cur.fetchone()
            return result
        
        
        except ms.Error as e:
            print(f"Error fetching user from database: {e}")
        finally:
            cur.close()
            con.close()
    return False  # Return False if connection or cursor is not established

###########################################################################################################

