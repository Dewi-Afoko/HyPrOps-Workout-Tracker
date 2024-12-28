class Workout_Exercise_Info:

    def __init__(self, workout, exercise):
        self.workout_id = workout.id
        self.exercise_dict = {exercise.name : 
                                {"Reps" : [],
                                "Loading" : [],
                                "Rest" : [],
                                "Performance Notes" : []}
                                }
        
        
    def add_exercise(self, exercise):
        self.exercise_dict[exercise.name] = {
                                "Reps" : [],
                                "Loading" : [],
                                "Rest" : [],
                                "Performance Notes" : []
                                }
        
    def add_set(self, exercise, reps):
        self.exercise_dict[exercise.name]["Reps"].append(reps)

    def set_loading(self, exercise, loading):
        self.exercise_dict[exercise.name]["Loading"].append(loading)

    def set_rest_period(self, exercise, rest):
        self.exercise_dict[exercise.name]["Rest"].append(rest)
    
    def add_performance_notes(self, exercise, notes):
        self.exercise_dict[exercise.name]["Performance Notes"].append(notes)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Workout Exercise Info({self.workout_id}, {self.exercise_dict})"