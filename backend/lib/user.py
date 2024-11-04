class User:

    def __init__(self, username, id=0):
        self.username = username
        self.workout_list = []
        self.id = id

    def update_password(self, password):
        self.password = password

    def add_workout(self, exercise):
        self.workout_list.append(exercise)

    def __repr__(self):
        return f"User({self.username}, {self.workout_list})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__