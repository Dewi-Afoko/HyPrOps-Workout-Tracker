from mongoengine import EmbeddedDocument, StringField, DateField, FloatField
from datetime import datetime

class PersonalData(EmbeddedDocument):
    name = StringField()
    dob = DateField()
    height = FloatField()
    weight = FloatField()

    def to_dict(self):
        return {
            'name': self.name,
            'dob': self.dob.strftime('%Y/%m/%d'),
            'height': self.height,
            'weight': self.weight,
        }