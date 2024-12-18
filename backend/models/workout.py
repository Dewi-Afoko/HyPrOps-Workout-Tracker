from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, BooleanField, EmbeddedDocumentField, EmbeddedDocumentListField, EmbeddedDocument, ObjectIdField
from datetime import datetime
from models.set_dicts import SetDicts
from models.user_stats import UserStats
from bson import ObjectId


class Workout(Document):
    user_id = ReferenceField('User', required=True)
    workout_name = StringField(require=True)
    date = DateTimeField(default=datetime.now().replace(second=0, microsecond=0))
    complete = BooleanField(default=False)
    set_dicts_list = EmbeddedDocumentListField(SetDicts)
    user_stats = EmbeddedDocumentField(UserStats)
    notes = ListField(StringField(), default=list)


    def add_set_dict(self, set_dict): # SetDict object
        self.set_dicts_list.append(set_dict)
        self.save()

    def delete_set_dict(self, set_dict):
        self.set_dicts_list.remove(set_dict)
        self.save()

    def toggle_complete(self):
        if self.complete == False:
            self.complete = True
        elif self.complete == True:
            self.complete = False
        self.save()

    def add_stats(self, user_stats): # UserStats object
        self.user_stats = user_stats
        self.save()

    def add_notes(self, notes): # notes is a string
        if not self.notes:
            self.notes = []
        self.notes.append(notes)
        self.save()

    def delete_note(self, note_index):
        del self.notes[int(note_index)]
        self.save()

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
    