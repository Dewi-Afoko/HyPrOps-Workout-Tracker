from mongoengine import EmbeddedDocument, IntField, ReferenceField, StringField, EmbeddedDocumentField
from models.personal_data import PersonalData

class UserStats(EmbeddedDocument): # Embed in workout
    weight = EmbeddedDocumentField(PersonalData, required=False)
    sleep_score = IntField() # From an app, Fitbit, Oura, Ringconn, etc.
    sleep_quality = StringField() # Subjective rating
    notes = StringField() # General notes about condition, illness, injury, etc.

    def set_weight(self): # Consider updating so method takes argument to pull latest weight from PersonalData
        self.weight = self.weight['weight']
