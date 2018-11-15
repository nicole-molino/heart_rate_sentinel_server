from builtins import int

from flask import Flask, jsonify, request
from pymodm import connect
from create_db import User
import datetime
import logging
from validate_get_heart_rate import validate_get_heart_rate, ValidationError
#from validate_patient_id import validate_patient_id

logging.basicConfig(filename="HR_sent_Logging.txt",
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def get_new_p():
    connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")
    a = request.get_json()
    print(a)

    # validate

    patient = User(patient_id=a["patient_id"],
                   attending_email=a["attending_email"],
                   user_age=a["user_age"])

    patient.save()
    logging.info("Added a new patient, %s", a["patient_id"])

    result = {"message": "Successfully added new patient"}

    return jsonify(result)


@app.route("/api/heart_rate", methods=["POST"])
def add_HR():
    a = request.get_json()
    print(a)

    user_id = User.objects.raw({"_id": a["patient_id"]})

    # need to throw an error if the id doesn't exist already

    user_id.update({"$push": {"heart_rate": a["heart_rate"]}})


    now = datetime.datetime.now()

    user_id.update({"$push": {"time_stamp": now}})

    logging.info("Added HR (%s BPM), patient: %s,  time: %s", a["heart_rate"], a["patient_id"], now)

    result = {"message": "Successfully added heart rate data"}


    return jsonify(result)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rate(patient_id):
    connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")

    a = int(patient_id)

    try:
        for user in User.objects.raw({"_id": a}):
            try:
                validate_get_heart_rate(user.heart_rate)
                logging.info("Add heart rate data %s", user.heart_rate)
            except ValidationError:
                return jsonify("User exists but no heart rate data")

        return jsonify(user.heart_rate)
    except UnboundLocalError:
        raise ValidationError("User does not exist")
        logging.warning("Tried to access user that does not exist")

if __name__ == "__main__":
    app.run(host="127.0.0.1")
