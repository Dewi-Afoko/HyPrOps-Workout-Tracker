from mongoengine import Document, StringField, ListField, EmbeddedDocumentField, EmbeddedDocumentListField
from werkzeug.security import generate_password_hash, check_password_hash
from models.personal_data import PersonalData
from models.workout import Workout

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    workout_list = EmbeddedDocumentListField(Workout, required=False)
    personal_data = EmbeddedDocumentField(PersonalData, required=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password)
        self.save()

    def add_workout(self, workout): # Workout object
        self.workout_list.append(workout)
        self.save()

    def add_personal_data(self, personal_data): # PersonalData object
        self.personal_data = personal_data

    def to_dict(self):
        return {
            'id' : str(self.id),
            'username' : self.username,
            'workout_list' : self.workout_list,
            'personal_data' : str(self.personal_data),
        }



    

