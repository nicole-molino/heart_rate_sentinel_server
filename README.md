# heart_rate_sentinel_server
BME 590 Homework Assignment
Nicole Molino
Due: Friday, November 16 

This README details the information for the heart rate sentinel assignment for BME 590.
This can help physicians store data about patients including id, email, age, heart rate.
It can also notify the physician if the patient is tachycardic or not. 


## Files Description
* **server.py** This module should be run as a flask application. The VM address
that can be used is: "vcm-7309.vm.duke.edu:5000". 

    Example get request:
    r=requests.get("http://vcm-7309.vm.duke.edu:5000/api/heart_rate/average/<patient_id>")

    This file contains multiple RESTful APIs specifications such as: 

    `POST /api/new_patient`
    `POST /api/heart_rate`
    `GET /api/status/<patient_id>`
    `GET /api/heart_rate/<patient_id>`
    `GET /api/heart_rate/average/<patient_id>`
    `POST /api/heart_rate/interval_average`

* **determine_if_tachy.py** Determines if the patient is tachycardic. 

* **determine_if_tachy.py** Determines if the patient is tachycardic. 

* **HR_sent_Logging.txt** activity log 

* **requirements.txt** 

* **send_grid.py** Service that sends an email to the doctor if the patient is 
tachycardic. NOTE: Change the e-mail to which you want to recieve, currently 
set to: nkm12@duke.edu 

## Tests 

* **validate_get_new_heart_rate.py** Checks if heart rate data exists 

* **validate_new_patient** Check if the patient exists already 

* **test_create_server.py**

* **test_determine_if_tachy.py**

* **test_get_heart_rate.py**

* **test_new_p.py**



