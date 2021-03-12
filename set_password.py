import mysql.connector 
from passlib.hash import bcrypt as hashalgo

mydb = mysql.connector.connect(
        host="172.17.0.2",
        user="autolab",
        database="autolab",
        password="autolab")

# Print all User
cur = mydb.cursor()
cur.execute("SELECT * FROM users")
for i in cur.fetchall():
    print(i)


# Update User Password
stus = """
linnil1@ntu.edu.tw
"""

stus = stus.split()

print(stus)

for stu in stus:
    name = stu.split("@")[0]
    cur = mydb.cursor()
    a = cur.execute("UPDATE users " \
                    "SET encrypted_password = %s " \
                    "WHERE email = %s", 
                    (hashalgo.hash(name + "@password"), stu))
    mydb.commit()

# Add to coure but fail
# INSERT INTO course_user_data (user_id, course_id) VALUES(57, 2);
