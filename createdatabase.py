from pymodm import connect
from pymodm import MongoModel, fields

connect("mongodb://bme590:hello12345@ds037768.mlab.com:37768/bme590")

# use list field
class User(MongoModel):

    patient_id = fields.IntegerField()
    attending_email = fields.EmailField()
    age = fields.IntegerField()
    heart_rate = fields.IntegerField()
    time_stamp = fields.DateTimeField()


u = User(patient = "1", attending_email = "nkm12@duke.edu", age = "60")

u.save()

for user in User.objects.raw({}):
    print(u.attending_email)
    print(u.age)
    del(u.attending_email)
    del(u.age)
    u.save()
    print(User)








