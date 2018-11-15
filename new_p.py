from builtins import int, type
from statistics import mean
from flask import Flask, jsonify, request
from pymodm import connect
from create_db import User
import datetime
import logging

from determine_if_tachy import determine_if_tachy
from send_grid import send_email
from validate_get_heart_rate import validate_get_heart_rate, ValidationError

# from validate_patient_id import validate_patient_id

logging.basicConfig(filename="HR_sent_Logging.txt",
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

app = Flask(__name__)

required_keys_to_add = [
    "patient_id",
    "attending_email",
    "user_age"
]


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


def validate_new_patient(req):
    for b in required_keys_to_add():
        if b not in req.keys():
            raise ValidationError("Missing a key")


@app.route("/api/new_patient", methods=["POST"])
def add_new_p():
    connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")
    a = request.get_json()

    try:
        validate_new_patient(a)
    except ValidationError as inst:
        return jsonify({"message": inst.message}), 500

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

    logging.info("Added HR (%s BPM), patient: %s,"
                 "  time: %s", a["heart_rate"], a["patient_id"], now)

    result = {"message": "Successfully added heart rate data"}

    HR = int(a["heart_rate"])

    for user in User.objects.raw({"_id": a["patient_id"]}):
        age = int(user.user_age)

    try:
        answer = determine_if_tachy(age, HR)
        if answer:
            send_email()
    except UnboundLocalError:
        raise ValidationError("User does not exist")
        logging.warning("Tried to access user that does not exist")

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


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def calculate_avg_HR(patient_id):
    connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")

    a = int(patient_id)

    try:
        for user in User.objects.raw({"_id": a}):
            try:
                validate_get_heart_rate(user.heart_rate)
                logging.info("Average heart rate data")
            except ValidationError:
                return jsonify("User exists but no heart rate data")

        ave = mean(user.heart_rate)
        return jsonify(ave)
    except UnboundLocalError:
        raise ValidationError("User does not exist")
        logging.warning("Tried to access user that does not exist")


@app.route("/api/heart_rate/status/<patient_id>", methods=["GET"])
def determine_tachy(patient_id):
    connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")

    a = int(patient_id)

    try:
        for user in User.objects.raw({"_id": a}):
            try:
                validate_get_heart_rate(user.heart_rate)
            except ValidationError:
                return jsonify("User exists"
                               " but no heart rate, can't determine")

        age = int(user.user_age)
        HR = int(user.heart_rate[-1])
        time = user.time_stamp[-1]
        answer = determine_if_tachy(age, HR)

        if answer:
            send_email()
            ans_str = 'Tachycardic'
        else:
            ans_str = 'Not tachycardic'

        return jsonify(ans_str, time)

    except UnboundLocalError:
        raise \
            ValidationError("User does "
                            "not exist")
        logging.wrarning("Tried to test if "
                         "tachycardia for user that does not exist")


if __name__ == "__main__":
    app.run(host="127.0.0.1")
