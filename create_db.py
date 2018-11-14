from pymodm import connect
from pymodm import MongoModel, fields

connect("mongodb://bme590:hello12345@ds157818.mlab.com:57818/hr")


# use list field
class User(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.IntegerField()
    heart_rate = fields.IntegerField()
    time_stamp = fields.DateTimeField()
