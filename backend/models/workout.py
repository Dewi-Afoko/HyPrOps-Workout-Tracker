from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, BooleanField, EmbeddedDocumentField, EmbeddedDocumentListField
from datetime import datetime
from models.set_dicts import SetDicts


class Workout(Document):
    user_id = ReferenceField('User', required=True)
    workout_name = StringField()
    date = DateTimeField(default=datetime.now)
    complete = BooleanField(default=False)
    set_dicts_list = EmbeddedDocumentListField(SetDicts)
    user_stats = EmbeddedDocumentField()
    notes = ListField(StringField(), default=list)
    

    