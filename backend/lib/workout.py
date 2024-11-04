from datetime import datetime

class Workout:

    def __init__(self, user):
        self.exercise_list = []
        self.user_id = user.id
        self.date = datetime.now().strftime("%Y/%m/%d")
        self.complete = False

    def add_exercise(self, exercise):
        self.exercise_list.append(exercise)

    def mark_complete(self):
        self.complete  = True

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Workout({self.exercise_list}, {self.user_id}, {self.date}, {self.complete})"