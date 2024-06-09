from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("emp.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/emp", methods=["GET", "POST"])
def employees():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM employee")
        Employees = [
            dict(id=row[0], empID=row[1], deptID=row[2], locID=row[3], name=row[4], salary=row[5], email=row[6])
            for row in cursor.fetchall()
        ]
        if Employees is not None:
            return jsonify(Employees)

    if request.method == "POST":
        new_empID = request.form["empID"]
        new_name = request.form["name"]
        new_departmentID = request.form["deptID"]
        new_salary = request.form["salary"]
        new_email = request.form["email"]
        new_locationID = request.form["locID"]
        sql = """INSERT INTO employee (empID, deptID, locID,name,salary,email)
                         VALUES (?, ?,?,?,?,?)"""
        cursor = cursor.execute(sql, (new_empID, new_name, new_departmentID, new_salary, new_email, new_locationID))
        conn.commit()
        return f"Employee added successfully", 201

    @app.route("/emp/<int:id>", methods=["GET", "PUT", "DELETE"])
    def single_employee(id):
        connE = db_connection()
        cursorEMP = connE.cursor()
        employee = None
        if request.method == "GET":
            cursorEMP.execute("SELECT * FROM employee WHERE id=?", (id,))
            rows = cursorEMP.fetchall()
            for r in rows:
                employee = r
            if employee is not None:
                return jsonify(employee), 200
            else:
                return "Something wrong", 404

            if request.method == "PUT":
                sql_B = """UPDATE employee
                        SET  empID=?,
                            deptID=?,
                             locID=?,
                             name=?,
                             salary=?,
                             email=? 
                        WHERE id=? """

            emp_id = request.form["empID"]
            name = request.form["name"]
            deptID = request.form["deptID"]
            salary = request.form["salary"]
            locID = request.form["locID"]
            email = request.form["email"]

            updated_employee = {
                "id": id,
                "empID": emp_id,
                "name": name,
                "salary": salary,
                "deptID": deptID,