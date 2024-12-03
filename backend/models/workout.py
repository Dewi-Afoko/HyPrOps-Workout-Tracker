from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, BooleanField, EmbeddedDocumentField, EmbeddedDocumentListField, EmbeddedDocument
from datetime import datetime
from models.set_dicts import SetDicts
from models.user_stats import UserStats


class Workout(EmbeddedDocument):
    user_id = ReferenceField('User', required=True)
    workout_name = StringField()
    date = DateTimeField(default=datetime.now)
    complete = BooleanField(default=False)
    set_dicts_list = EmbeddedDocumentListField(SetDicts)
    user_stats = EmbeddedDocumentField(UserStats)
    notes = ListField(StringField(), default=list)
    

    