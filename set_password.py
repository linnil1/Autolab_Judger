import pymysql
from passlib.hash import bcrypt as hashalgo

mydb = pymysql.connect(
        host="db",
        user="user",
        database="autolab_development",
        password="password")

# Print all User
cur = mydb.cursor()
cur.execute("SELECT * FROM users")
for i in cur.fetchall():
    print(i)


# Update User Password
stus = """
hardness1020@gmail.com
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
