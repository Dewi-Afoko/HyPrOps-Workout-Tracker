from mongoengine import EmbeddedDocument, IntField, ReferenceField, StringField, EmbeddedDocumentField, FloatField

class UserStats(EmbeddedDocument): # Embed in workout
    weight = FloatField()
    sleep_score = IntField() # From an app, Fitbit, Oura, Ringconn, etc.
    sleep_quality = StringField() # Subjective rating
    notes = StringField() # General notes about condition, illness, injury, etc.

    def update_user_stats(self, weight=None, sleep_score=None, sleep_quality=None, notes=None):
        if weight != None: 
            self.weight = weight
        if sleep_score != None:
            self.sleep_score = sleep_score
        if sleep_quality != None:
            self.sleep_quality = sleep_quality
        if notes != None:
            self.notes = notes

    def to_dict(self):
        return {
            'weight': self.weight,
            'sleep_score': self.sleep_score,
            'sleep_quality': self.sleep_quality,
            'notes': self.notes
        }
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__