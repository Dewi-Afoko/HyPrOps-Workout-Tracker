from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, BooleanField, EmbeddedDocumentField, EmbeddedDocumentListField, EmbeddedDocument
from datetime import datetime
from models.set_dicts import SetDicts


class Workout(EmbeddedDocument):
    user_id = ReferenceField('User', required=True)
    workout_name = StringField()
    date = DateTimeField(default=datetime.now)
    complete = BooleanField(default=False)
    set_dicts_list = EmbeddedDocumentListField(SetDicts)
    user_stats = EmbeddedDocumentField()
    notes = ListField(StringField(), default=list)
    

    