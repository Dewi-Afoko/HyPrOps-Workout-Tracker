from mongoengine import EmbeddedDocument, IntField, ReferenceField, StringField, EmbeddedDocumentField
from models.personal_data import PersonalData

class UserStats(EmbeddedDocument): # Embed in workout
    weight = ReferenceField('PersonalData')
    sleep_score = IntField() # From an app, Fitbit, Oura, Ringconn, etc.
    sleep_quality = StringField() # Subjective rating
    notes = StringField() # General notes about condition, illness, injury, etc.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_weight()

    def set_weight(self):
        self.weight = self.weight['weight']

    def update_user_stats(self, weight=None, sleep_score=None, sleep_quality=None, notes=None):
        if weight != None: # If this is accessed, we need to update PersonalData
            self.weight = weight
        if sleep_score != None:
            self.sleep_score = sleep_score
        if sleep_quality != None:
            self.sleep_quality = sleep_quality
        if notes != None:
            self.notes = notes
        self.set_weight()

    def to_dict(self):
        weight = int(self.weight.weight)
        return {
            'weight': weight,
            'sleep_score': self.sleep_score,
            'sleep_quality': self.sleep_quality,
            'notes': self.notes
        }