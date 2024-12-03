from mongoengine import EmbeddedDocument, StringField, DateField, FloatField

class PersonalData(EmbeddedeDocument):
    name = StringField()
    dob = DateField()
    height = FloatField()
    weight = FloatField()