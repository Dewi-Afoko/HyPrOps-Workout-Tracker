from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, BooleanField, EmbeddedDocumentField
from datetime import datetime
from .workout_exercise_info import WorkoutExerciseInfo

class Workout(Document): #TODO: Add notes for workout, add to __repr__ and to_dict, add edit routes, testing and documentation
    user_id = ReferenceField('User', required=True) 
    date = DateTimeField(default=datetime.now)
    complete = BooleanField(default=False)
    exercise_list = ListField(EmbeddedDocumentField(WorkoutExerciseInfo), default=list)
    

    def add_exercise(self, exercise_info):
        self.exercise_list.append(exercise_info)
        self.save()

    def mark_complete(self):
        self.complete = True
        self.save()

    def __repr__(self): #TODO: Add complete, id and date to this function - fix tests for those criteria
        return f"Workout(user_id={self.user_id}, exercise_list={self.exercise_list})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def to_dict(self):
        return {
            "id": str(self.id), 
            "user_id": str(self.user_id), 
            "exercise_list": [exercise.to_dict() for exercise in self.exercise_list],
            "complete": self.complete,
            "date": self.date,
        }
