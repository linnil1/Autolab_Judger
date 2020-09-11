import mysql.connector 
from passlib.hash import bcrypt as hashalgo

mydb = mysql.connector.connect(
        host="172.17.0.2",
        user="autolab",
        database="autolab",
        password="password")

# Print all User
cur = mydb.cursor()
cur.execute("SELECT * FROM users")
for i in cur.fetchall():
    print(i)


# Add user
cur = mydb.cursor()
cur.execute("INSERT INTO users" \
            "(email,first_name)" \
            "VALUES(%s,%s)", 
            ("linnil123@ntu.edu.tw", "linnil1"))
for i in cur.fetchall():
    print(i)
mydb.commit()

# Update User Password
cur = mydb.cursor()
a = cur.execute("UPDATE users " \
                "SET encrypted_password = %s " \
                "WHERE email = %s", 
                (hashalgo.hash("yourpassword"), "linnil1@ntu.edu.tw"))
mydb.commit()

# Add to coure but fail
# INSERT INTO course_user_data (user_id, course_id) VALUES(57, 2);
