from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, BooleanField, EmbeddedDocumentField, EmbeddedDocumentListField, EmbeddedDocument, ObjectIdField
from datetime import datetime
from models.set_dicts import SetDicts
from models.user_stats import UserStats
from bson import ObjectId


class Workout(EmbeddedDocument):
    id = ObjectIdField(required=True, default=ObjectId, primary_key=True)
    user_id = ReferenceField('User', required=True)
    workout_name = StringField()
    date = DateTimeField(default=datetime.now)
    complete = BooleanField(default=False)
    set_dicts_list = EmbeddedDocumentListField(SetDicts)
    user_stats = EmbeddedDocumentField(UserStats)
    notes = ListField(StringField(), default=list)


    def add_set_dict(self, set_dict): # SetDict object
        self.set_dicts_list.append(set_dict)

    def delete_set_dict(self, set_dict):
        self.set_dicts_list.remove(set_dict)

    def toggle_complete(self):
        if self.complete == False:
            self.complete = True
        elif self.complete == True:
            self.complete = False

    def add_stats(self, user_stats): # UserStats object
        self.user_stats = user_stats

    def add_notes(self, notes): # notes is a string
        self.notes.append(notes)

    def delete_note(self, note_index):
        del self.notes[note_index]

    def to_dict(self):
        workout_id = str(self.id)
        user_id = str(self.user_id.id)
        workout_dict = {
            "id": workout_id,
            "user_id": user_id,
            "workout_name": self.workout_name,
            "date": self.date.isoformat() if self.date else None,  # Properly serialize date
            "complete": self.complete,
            "sets_dict_list": [set_dict.to_dict() for set_dict in self.set_dicts_list],
            "user_stats": self.user_stats.to_dict() if self.user_stats else None,
            "notes": self.notes,
        }
        return workout_dict
    

    def __eq__(self, other):
        return super().__eq__(other)