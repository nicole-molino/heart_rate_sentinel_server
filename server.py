from builtins import int, type, float, ValueError, KeyError, UnboundLocalError
from statistics import mean
from flask import Flask, jsonify, request
from pymodm import connect
from create_db import User
import datetime
import logging
from determine_if_tachy import determine_if_tachy
from send_grid import send_email
from validate_get_heart_rate import validate_get_heart_rate, ValidationError
from validate_new_patient import check_if_new
from statistics import StatisticsError

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
    """
     Determine if correct keys given when making new patient

     Args:
         a (json) : keys input by user

     Raises:
         Validation Error: If missing key
    """

    for key in REQ_KEYS():
        if key not in req.keys():
            raise ValidationError("Key '{0}' "
                                  "not present in request".format(key))


@app.route("/api/new_patient", methods=["POST"])
def add_new_p():
    """Add new patient to data base

    Args:
        patient_id (key): numerical id of patient
        user_age (key) : age of patient
        attending_email (key) : patient email

    Returns:
        result: prints if patient was saved

    Returns: if patient added to database """
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
    # try:
    #    validate_new_patient(a)
    # except ValidationError as inst:
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
    """
    Store HR data with time stamp and sends email if tachycardic

    Args:
        patient_id (key): id of patient
        heart_rate (key): HR data want to enter

    Returns:
        result (string): says data was added

    Raises:
        ValidationError: Wrong keys given
        ValidationError: Patient doesn't exist

    """
    a = request.get_json()

    # validate correct keys

    # check if patient exists
    my_id = a["patient_id"]
    all_id = []
    all_pat = User.objects.raw({})
    for user in all_pat:
        all_id.append(user.patient_id)

    try:
        aa = check_if_new(all_id, my_id)
        if aa == 1:
            raise ValidationError("Patient doesn't exist")
            logging.error("Tried to add HR to non-existent patient")
    except ValueError:
        pass

    # add the heart rate data
    user_id = User.objects.raw({"_id": a["patient_id"]})
    try:
        user_id.update({"$push": {"heart_rate": a["heart_rate"]}})
    except KeyError:
        logging.warning("Provided wrong keys")
        raise ValidationError("Provide keys: ID and HR only")

    now = datetime.datetime.now()
    user_id.update({"$push": {"time_stamp": now}})
    logging.info("Added HR (%s BPM), patient: %s,"
                 "  time: %s", a["heart_rate"], a["patient_id"],
                 now)
    result = {"message": "Successfully added heart rate data"}

    # send email if tachycardic

    HR = float(a["heart_rate"])
    age = User.objects.raw({"_id": a["patient_id"]}).first().user_age

    try:
        if determine_if_tachy(age, HR):
            send_email()
            logging.info("Patient %s is tachycardic, HR: %s", my_id, HR)
    except UnboundLocalError:
        raise ValidationError("User does not exist")

    return jsonify(result)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rate(patient_id):
    """
    Return all previous HR data

    Args:
        patient_id: ID of patient you want data for

    Returns:
        HRdata (json): json of all HR data

    Raises:
        ValidationError: User doesn't exist
        ValidationError: No HR data for user
    """
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
    """
    Average of HR data for all measurements

    Args:
        patient_id (int): id of specified patient

    Returns:
        ave (json): json with value of average HR

    Raises:
        ValidationError: user doesn't exist
    """
    connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")

    a = int(patient_id)

    try:
        for user in User.objects.raw({"_id": a}):
            try:
                validate_get_heart_rate(user.heart_rate)
                logging.info("Average heart rate data")
            except ValidationError:
                pass
                mes = jsonify("User exists but no heart rate data")

        ave = mean(user.heart_rate)
        mes = jsonify(ave)
    except UnboundLocalError:
        mes = "User does not exist"
        # raise ValidationError("User does not exist")
        logging.warning("Tried to access user that does not exist")

    return mes


@app.route("/api/heart_rate/status/<patient_id>", methods=["GET"])
def determine_tachy(patient_id):
    """
    Return if patient is tachy from most
    recent measurement and time stamp, send email if tachy

    Args:
        patient_id (str):

    Returns:
        ans_str (str):  if tachy or not
        time (str): time stamp

    Raises:
        ValidationError: User doesn't exist
    """
    connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")

    a = int(patient_id)

    try:
        for user in User.objects.raw({"_id": a}):
            try:
                validate_get_heart_rate(user.heart_rate)
            except ValidationError:
                pass

        time = user.time_stamp[-1]
        answer = determine_if_tachy(float(user.user_age),
                                    int(user.heart_rate[-1]))

        # send email if tahycardic
        if answer:
            logging.warning("User is tachycardic")
            send_email()
            ans_str = 'Tachycardic'

        else:
            ans_str = 'Not tachycardic'
            logging.info("User is not tachycardic")

        mes = jsonify(ans_str, time)

    except UnboundLocalError:
        mes = "User does not exist"
        mes = jsonify(mes)
        logging.warning("Tried to test if "
                        "tachycardia for user that does not exist")

    return mes


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def calc_int_avg():
    """
    Calculate average HR over an interval

    Returns:
        int_avg (json) : average over the interval

    """
    connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")

    r = request.get_json()

    # check if user exists

    my_id = r["patient_id"]
    all_id = []
    all_pat = User.objects.raw({})

    for user in all_pat:
        all_id.append(user.patient_id)

    # check if patient exists
    try:
        b = check_if_new(all_id, my_id)
        if b == 1:
            raise ValidationError("Patient doesn't exist")
    except ValueError:
        pass

    time_requested = \
        datetime.datetime.strptime(r["heart_rate_average_since"],
                                   "%Y-%m-%d %H:%M:%S.%f")

    # pidstr = r["patient_id"]
    # pi = int(pidstr)
    pat = User.objects.raw({"_id": r["patient_id"]}).first()
    alltime = pat.time_stamp
    allHR = pat.heart_rate
    HRint = []

    for item in alltime:
        if item > time_requested:
            index = alltime.index(item)
            HRint.append(allHR[index])
    try:
        int_avg = mean(HRint)
        mes = jsonify(int_avg)
    except StatisticsError:
        mes = "No HR data for patient"
    return mes


if __name__ == "__main__":
    app.run(host="0.0.0.0")
