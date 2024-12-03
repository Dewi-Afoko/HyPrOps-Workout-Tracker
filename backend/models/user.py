from mongoengine import Document, StringField, ListField, EmbeddedDocumentField, EmbeddedDocumentListField
from werkzeug.security import generate_password_hash, check_password_hash
from models.personal_data import PersonalData
from models.workout import Workout

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)  # Hash this
    workout_list = EmbeddedDocumentListField(Workout)
    personal_data = EmbeddedDocumentField(PersonalData)

