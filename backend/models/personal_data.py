from mongoengine import EmbeddedDocument, StringField, DateField, FloatField

class PersonalData(EmbeddedDocument):
    name = StringField()
    dob = DateField()
    height = FloatField()
    weight = FloatField()