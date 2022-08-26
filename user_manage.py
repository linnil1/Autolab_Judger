"""
Author: linil1
Description: Directly connect to DB to create user and change password
"""
import sys
import datetime
import pymysql
from passlib.hash import bcrypt as hashalgo


mydb = pymysql.connect(
    host="db",
    user="autolab",
    database="autolab_development",
    password="autolab_password"
)


def listUser():
    # Print all User
    cur = mydb.cursor()
    cur.execute("SELECT * FROM users")
    for i in cur.fetchall():
        print(i)


def addUser(email: str, name: str):
    cur = mydb.cursor()
    cur.execute("INSERT INTO users "
                "(email, first_name, confirmed_at) "
                "VALUES(%s, %s, '%s')", 
                (email, name, datatime.datetime.now()))
    mydb.commit()


def changePassword(email: str, password: str):
    # Update User Password
    cur = mydb.cursor()
    cur.execute("UPDATE users "
                "SET encrypted_password = %s "
                "WHERE email = %s",
                (hashalgo.hash(password), email))
    mydb.commit()


if __name__ == "__main__":
    if sys.argv[1] == "list":
        listUser()
    elif sys.argv[1] == "add":
        if len(sys.argv) != 4:
            print("python user_manage.py add EMAIL NAME")
            exit()
        addUser(sys.argv[2].strip(), sys.argv[3].strip())
    elif sys.argv[1] == "passwd":
        if len(sys.argv) != 4:
            print("python user_manage.py passwd EMAIL PASSWORD")
            exit()
        changePassword(sys.argv[2].strip(), sys.argv[3].strip())
    else:
        print("python user_manage.py [list|add|passwd]")
