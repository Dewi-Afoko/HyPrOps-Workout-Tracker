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
    
    def update_personal_details(self, name=None, dob=None, height=None, weight=None):
        if name != None:
            self.name = name
        if dob != None:
            self.dob = dob
        if height != None:
            self.height = height
        if weight != None: 
            self.weight = weight
        
