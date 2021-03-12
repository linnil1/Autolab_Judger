import mysql.connector 
from passlib.hash import bcrypt as hashalgo
from collections import defaultdict
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

mydb = mysql.connector.connect(
        host="172.17.0.2",
        user="autolab",
        database="autolab",
        password="autolab")

"""
SELECT a.email, MAX(d.total)
FROM users as a
LEFT JOIN course_user_data as b on a.id = b.user_id
LEFT JOIN submissions as c on b.id = c.course_user_datum_id
JOIN(
    SELECT submission_id as submission_id, SUM(score) as total
    FROM scores as d
    GROUP BY submission_id
) d on c.id = d.submission_id
WHERE c.assessment_id = 24
GROUP BY a.id
INTO OUTFILE '/var/lib/mysql/hw11.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
"""

# Print all User
cur = mydb.cursor()
cur.execute("SELECT id, name, due_at FROM assessments;")
course = list(cur.fetchall())
print(course)

def handinTimes():
    for p_num, c in enumerate(course[1:10]):
        cur = mydb.cursor()
        cur.execute(f"""
        SELECT a.email, c.settings FROM users as a
        LEFT JOIN course_user_data as b on a.id = b.user_id
        LEFT JOIN submissions as c on b.id = c.course_user_datum_id
        WHERE c.assessment_id = {c[0]} """)

        tool = defaultdict(list)
        for i in cur.fetchall():
            tool[i[0]].append(i[1])

        plt.subplot(3, 3, p_num + 1)
        plt.hist([len(tool[i]) for i in tool], bins=20)
        pprint(tool)
        plt.title(c[1])

    plt.suptitle("Handin Times")
    plt.show()


def countLanguage():
    hw = []
    hw_name = []
    labels = ["Python", "Java", "Multi"]

    for p_num, c in enumerate(course[1:-1]):
        cur = mydb.cursor()
        cur.execute(f"""
        SELECT a.email, c.settings FROM users as a
        LEFT JOIN course_user_data as b on a.id = b.user_id
        LEFT JOIN submissions as c on b.id = c.course_user_datum_id
        WHERE c.assessment_id = {c[0]}
        """)

        def getLang(arr):
            if all(["Python" in i for i in arr]):
                return "Python"
            if all(["Java" in i for i in arr]):
                return "Java"
            return "Multi"

        tool = defaultdict(list)

        for i in cur.fetchall():
            tool[i[0]].append(i[1])

        tool = [getLang(tool[i]) for i in tool]
        size = [sum(i == l for i in tool) for l in labels]
        hw.append(size)
        hw_name.append(c[1])
        """
        plt.subplot(3, 3, p_num + 1)
        plt.pie(size, labels=labels, autopct='%1.1f%%', counterclock=False, startangle=90)
        # pprint(tool)
        plt.title(c[1] + f" N={sum(size)}")
        """

    """
    plt.suptitle("Language")
    """
    hw = np.array(hw)
    print(hw)
    ind = np.arange(len(hw))
    bottom = np.zeros(shape=hw.shape[0])
    for i in range(len(labels)):
        plt.bar(ind, hw[:, i], label=labels[i], bottom=bottom)
        for j in range(len(hw)):
            perc = round(hw[j,i] / hw[j, :].sum() * 100)
            plt.text(x=j-0.2, y=bottom[j] + hw[j, i] // 2 - 2, s=f"{perc}%" , fontdict=dict(fontsize=20))
        bottom += hw[:, i]
    plt.xticks(np.arange(len(hw)), hw_name)
    plt.legend()

    plt.title("Language Submissions")
    plt.tight_layout()
    plt.show()


def tryVSscore():
    for p_num, c in enumerate(course[1:10]):
        cur = mydb.cursor()
        cur.execute(f"""
        SELECT a.email, d.total FROM users as a
        LEFT JOIN course_user_data as b on a.id = b.user_id
        LEFT JOIN submissions as c on b.id = c.course_user_datum_id
        JOIN(
            SELECT submission_id as submission_id, SUM(score) as total
            FROM scores as d
            GROUP BY submission_id
        ) d on c.id = d.submission_id
        WHERE c.assessment_id = {c[0]}
        """)
        score = defaultdict(list)
        for i in cur.fetchall():
            score[i[0]].append(i[1])

        # plt.subplot(3, 3, p_num + 1)
        plt.subplot(3, 3, p_num + 1)
        for _, arr in score.items():
            m = 0
            marr = []
            for i in arr:
                m = max(m, i)
                marr.append(m)
            plt.plot(marr)
        plt.title(c[1] + f" N={len(score)}")


    plt.suptitle("Max score vs Times of Try")
    plt.show()


# handinTimes()
# countLanguage()
# tryVSscore()
