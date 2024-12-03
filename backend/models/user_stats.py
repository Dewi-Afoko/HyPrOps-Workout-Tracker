from mongoengine import EmbeddedDocument, IntField, ReferenceField, StringField

class UserStats(EmbeddedDocument): # Embed in workout
    weight = ReferenceField('PersonalData') # Pull from PersonalData
    sleep_score = IntField() # From an app, Fitbit, Oura, Ringconn, etc.
    sleep_quality = StringField() # Subjective rating
    notes = StringField() # General notes about condition, illness, injury, etc.