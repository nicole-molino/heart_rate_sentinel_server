from flask import Flask, jsonify, request
from pymodm import connect
from create_db import User

app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def get_new_p():
    a = request.get_json()
    connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")
    print(a)

    # validate

    patient = User(patient_id=a["patient_id"],
                   attending_email=a["attending_email"],
                   user_age=a["user_age"])

    patient.save()

    result = {"message": "Successfully added new patient"}

    return jsonify(result)


@app.route("/api/heart_rate", methods=["POST"])
def add_HR():
    a = request.get_json()
    print(a)
    patient = User(patient_id=a["patient_id"],
                   attending_email=a["attending_email"],
                   user_age=r["user_age"])

    patient.save()

    result = {"message": "Successfully added heart rate data"}

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1")
