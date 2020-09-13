chown 1005:1005 autograde -R
chmod 700 autograde -R
chmod 705 autograde autograde/py_grade.py autograde/java_grade.java autograde/*.jar
tar -cf autograde.tar autograde/
