from flask import Flask, request, jsonify
import mysql.connector


app = Flask(__name__)


def getDBConnection():
    connection = mysql.connector.connect(
        host="localhost",
        user="veekus",
        password="QwertY!1606",
        database="dev",
    )
    return connection


def checkIfNumberExists(cursor,number):
    cursor.execute("SELECT * FROM numbers WHERE number = %s", (number,))
    result = cursor.fetchone()
    return result

@app.route("/", methods=["POST"])
def sendNumberRequest():
    connec = getDBConnection()
    cursor = connec.cursor()
    try:
        number = request.json["number"]
    except ValueError:
        return jsonify({"error": "Пожалуйста, введите корректный номер."})
    result = checkIfNumberExists(cursor,number)
    result2 = checkIfNumberExists(cursor,int(number+1))
    if result:
        return jsonify({"error": "Номер уже был введен."})
    if result2:
            return jsonify({"error": "Номер до введен уже был введен."})

    connec.cursor().execute("INSERT INTO numbers (number) VALUES (%s)", (number,))
    connec.commit()

    next_number = number + 1
    return jsonify({"result": next_number})



if __name__ == "__main__":
    app.run(port=5000)