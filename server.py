from builtins import int, type, float
from statistics import mean
from flask import Flask, jsonify, request
from pymodm import connect
from create_db import User
import datetime
import logging
from validate_new_patient import  check_if_new

from determine_if_tachy import determine_if_tachy
from send_grid import send_email
from validate_get_heart_rate import validate_get_heart_rate, ValidationError

# from validate_patient_id import validate_patient_id

logging.basicConfig(filename="HR_sent_Logging.txt",
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

app = Flask(__name__)




REQ_KEYS = [
    "patient_id",
    "attending_email",
    "user_age"
    ]

class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

def validate_new_patient(req):
    for key in REQ_KEYS():
        if key not in req.keys():
            raise ValidationError("Key '{0}' not present in request".format(key))

@app.route("/api/new_patient", methods=["POST"])
def add_new_p():
    connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")
    a = request.get_json()
    my_id = a["patient_id"]
    all_id = []
    all_pat = User.objects.raw({})
    for user in all_pat:
        all_id.append(user.patient_id)

    # check if patient exists
    check_if_new(all_id, my_id)

    # validate correct keys
    #try:
    #    validate_new_patient(a)
    #except ValidationError as inst:
    #    return jsonify({"message": inst.message}),500

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

    HR = float(a["heart_rate"])

    for user in User.objects.raw({"_id": a["patient_id"]}):
        age = int(user.user_age)
        return age
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

        age = float(user.user_age)
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
        logging.warning("Tried to test if "
                        "tachycardia for user that does not exist")


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def calc_int_avg():
    connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")

    r = request.get_json()
    time_requested = datetime.datetime. \
        strptime(r["heart_rate_average_since"], "%Y-%m-%d %H:%M:%S.%f")

    pat = User.objects.raw({"_id": r["patient_id"]}).first()
    alltime = pat.time_stamp
    allHR = pat.heart_rate
    HRint = []

    for item in alltime:
        if item > time_requested:
            index = alltime.index(item)
            HRint.append(allHR[index])
    int_avg = mean(HRint)
    return jsonify(int_avg)


if __name__ == "__main__":
    app.run(host="127.0.0.1")
