from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, BooleanField, EmbeddedDocumentField, EmbeddedDocumentListField, EmbeddedDocument, ObjectIdField, FloatField, IntField
from datetime import datetime
from models.set_dicts import SetDicts
from bson import ObjectId
from copy import deepcopy


class Workout(Document):
    user_id = ReferenceField('User', required=True)
    workout_name = StringField(require=True)
    date = DateTimeField(default=datetime.now().replace(second=0, microsecond=0))
    complete = BooleanField(default=False)
    set_dicts_list = EmbeddedDocumentListField(SetDicts)
    user_weight = FloatField()
    sleep_score = IntField()
    sleep_quality = StringField()
    notes = ListField(StringField(), default=list)


    def add_set_dict(self, set_dict): # SetDict object
        set_dict_copy = deepcopy(set_dict)
        set_order = len(self.set_dicts_list) + 1
        set_number = 1
        for set in self.set_dicts_list:
            if set.exercise_name == set_dict_copy.exercise_name:
                set_number += 1
        set_dict_copy.set_order = set_order
        set_dict_copy.set_number = set_number
        self.set_dicts_list.append(set_dict_copy)
        self.save()

    def delete_set_dict(self, set_number):
        del self.set_dicts_list[set_number]
        self.save()

    def toggle_complete(self):
        if self.complete == False:
            self.complete = True
        elif self.complete == True:
            self.complete = False
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
            "user_weight": float(self.user_weight) if self.user_weight else None,
            "sleep_score": self.sleep_score,
            "sleep_quality": self.sleep_quality,
            "notes": self.notes,
        }
        return workout_dict
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def format_workout(self):
        set_order = 1
        exercise_count = {}
        for set in self.set_dicts_list:
            set.set_order = set_order
            set_order += 1
            exercise_name = set.exercise_name
            if exercise_name in exercise_count:
                exercise_count[exercise_name] += 1
            else:
                exercise_count[exercise_name] = 1
            set.set_number = exercise_count[exercise_name]
        self.save()

    def edit_details(self, name=None, date=None, user_weight=None, sleep_score=None, sleep_quality=None):
        if name is not None:
            self.workout_name = name  # Ensure you update the correct field
        if date is not None:
            self.date = date
        if user_weight is not None:
            try:
                self.user_weight = float(user_weight)  # Cast to float for weight
            except ValueError:
                raise ValueError("user_weight must be a number")
        if sleep_score is not None:
            try:
                self.sleep_score = float(sleep_score)  # Cast to float for sleep_score
            except ValueError:
                raise ValueError("sleep_score must be a number")
        if sleep_quality is not None:
            self.sleep_quality = sleep_quality
        self.save()
