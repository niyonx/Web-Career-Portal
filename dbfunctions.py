import sshtunnel
import pymysql
import config

sshtunnel.SSH_TIMEOUT = 30000

# Connecting to database

server = sshtunnel.SSHTunnelForwarder(
    'login.encs.concordia.ca',
    ssh_username=config.SSH_USERNAME,
    ssh_password=config.SSH_PASSWORD,
    remote_bind_address=('qxc353.encs.concordia.ca', 3306)
)

server.start()
print(server.local_bind_port)

print("Connected to server")

db = pymysql.connect(
    host="localhost",
    port=server.local_bind_port,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_DATABASE,
    connect_timeout=3100)

cursor = db.cursor()

print("Connected to database")

# sql = "SELECT * FROM admin;"

# try:
#     # Execute the SQL command
#     cursor.execute(sql)
#     # Fetch all the rows in a list of lists.
#     results = cursor.fetchall()
#     # for item in results:
#     #     print(item)
# except:
#     print("Error: unable to fetch data")

# db.close()

def getUsers():
    sql = "SELECT * FROM user ;"

    results = []
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        # for item in results:
        #     print(item)
    except:
        print("Error: unable to fetch data")

    # Table headers
    field_names = [i[0] for i in cursor.description]

    return field_names, results
    
def getJobs():
    sql = "SELECT * FROM jobs ;"

    results = []
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        # for item in results:
        #     print(item)
    except:
        print("Error: unable to fetch data")

    # Table headers
    field_names = [i[0] for i in cursor.description]

    return field_names, results

def postJob(job_title):
    sql = "INSERT INTO jobs(job_title) VALUES(\'"+job_title+"\');"

    # print(sql)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit SQL command
        db.commit()
        return True
    except Exception as e:
        print("Problem inserting into db: " + str(e))
        return False

def verifyAccount(email, password):
    email.replace(" ", "")
    password.replace(" ", "")
    sqlUser= "SELECT EXISTS (SELECT * FROM user WHERE login_email=\'"+email+"\' AND password=\'"+password+"\')"
    sqlAdmin = "SELECT EXISTS (SELECT * FROM admin WHERE login_email=\'"+email+"\' AND password=\'"+password+"\')"

    # print(sqlUser)
    try:
        cursor.execute(sqlUser)
        result = cursor.fetchall()
        if result[0][0] == 0:
            cursor.execute(sqlAdmin)
            result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print("Problem verifying user info: " + str(e))
        return False


def getUserID(email, password):
    sql = "SELECT ID FROM user WHERE login_email=\'"+email+"\' AND password=\'"+password+"\'"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            return result[0][0]
        else:
            sqlAdmin ="SELECT ID FROM admin WHERE login_email=\'"+email+"\' AND password=\'"+password+"\'"
            cursor.execute(sqlAdmin)
            result = cursor.fetchall()
            for item in results:
                print(item)
        return result[0][0]
    except Exception as e:
        print("Problem getting user ID: " + str(e))
        return False

def applyJob(jobSeekerID, jobID, appliedDate, coverLetter, resume):
    # sql = "INSERT INTO applyTo VALUES(\'1231221\',\'1232112\',\'2020-02-02\',\'pending\',\'coverletter\',\'resume\');"
    sql = "INSERT INTO applyTo VALUES(\'"+jobSeekerID+"\',\'"+jobID+"\',\'"+appliedDate+"\',\'pending\',\'"+coverLetter+"\',\'"+resume+"\');"

    print(sql)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit SQL command
        db.commit()
        return True
    except Exception as e:
        print("Problem inserting into db: " + str(e))
        return False
