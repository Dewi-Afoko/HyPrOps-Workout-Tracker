from mongoengine import EmbeddedDocument, IntField, ReferenceField, StringField, EmbeddedDocumentField
from models.personal_data import PersonalData

class UserStats(EmbeddedDocument): # Embed in workout
    weight = EmbeddedDocumentField(PersonalData, required=False)
    sleep_score = IntField() # From an app, Fitbit, Oura, Ringconn, etc.
    sleep_quality = StringField() # Subjective rating
    notes = StringField() # General notes about condition, illness, injury, etc.

    def set_weight(self): # Consider updating so method takes argument to pull latest weight from PersonalData
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

    def to_dict(self):
        weight = str(self.weight.weight)
        return {
            'weight': weight,
            'sleep_score': self.sleep_score,
            'sleep_quality': self.sleep_quality,
            'notes': self.notes
        }