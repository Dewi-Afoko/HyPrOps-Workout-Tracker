class Exercise:

    def __init__(self, name, id=0):
        self.name = name
        self.type = []
        self.muscles = []
        self.equipment = []
        self.id = id

    def add_lift_type(self, type):
        self.type.append(type)

    def add_muscle(self, muscle):
        self.muscles.append(muscle)

    def add_equipment(self, equipment):
        self.equipment.append(equipment)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Exercise({self.name}, {self.type}, {self.muscles}, {self.equipment})"