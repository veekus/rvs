from flask import Flask, request, jsonify
import mysql.connector
import logging


app = Flask(__name__)


def getDBConnection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="QwertY!1606",
        database="dev",
    )
    return connection


def checkIfNumberExists(cursor,number):
    cursor.execute("SELECT * FROM numbers WHERE number = %s", (number,))
    result = cursor.fetchone()
    return result

@app.route('/', methods=['POST', 'GET'])
def sendNumberRequest():
    #logging.basicConfig(filename=f'/home/veekus/rvs/log.log', encoding='utf-8', level=logging.DEBUG)
    #logging.info(f'The container was run at {datetime.now()}')
    connec = getDBConnection()
    cursor = connec.cursor()
    try:
        if request.method == 'POST':
            number = int(request.form['number'])
            #request.json["number"]
            result = checkIfNumberExists(cursor,number)
            result2 = checkIfNumberExists(cursor,int(number+1))
            if result:
                #logging.info(f'Номер уже был введен')
                return jsonify({"error": "Номер уже был введен."})
            if result2:
                #logging.info(f'Номер до введен уже был введен')
                return jsonify({"error": "Номер до введен уже был введен."})

            connec.cursor().execute("INSERT INTO numbers (number) VALUES (%s)", (number,))
            connec.commit()

            next_number = number + 1
            return jsonify({"result": next_number})
        else:
            return """
            <form method="post">
                <label for="number">Введите число:</label>
                <input type="number" id="number" name="number">
                <input type="submit" value="Сохранить">
            </form>
            """
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(port=5000)
