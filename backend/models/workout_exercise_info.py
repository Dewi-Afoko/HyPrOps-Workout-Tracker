from mongoengine import EmbeddedDocument, StringField, IntField, FloatField, ListField, BooleanField

class WorkoutExerciseInfo(EmbeddedDocument):
    exercise_name = StringField(required=True)
    reps = ListField(IntField(), default=list)
    loading = ListField(FloatField(), default=list)
    rest = ListField(IntField(), default=list)
    performance_notes = ListField(StringField(), default=list)
    complete = BooleanField(default=False)  # New field added with default value False

    def add_set(self, reps):
        self.reps.append(reps)

    def set_loading(self, loading):
        self.loading.append(loading)

    def set_rest_period(self, rest):
        self.rest.append(rest)

    def add_performance_notes(self, notes):
        self.performance_notes.append(notes)
    
    def mark_complete(self):
        """Method to set complete to True."""
        self.complete = True

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return (
            f"WorkoutExerciseInfo(exercise_name={self.exercise_name}, reps={self.reps}, loading={self.loading}, rest={self.rest}, performance_notes={self.performance_notes}, complete={self.complete})"
        )
    
    def to_dict(self):
        return {
            "exercise_name": self.exercise_name,
            "reps": self.reps,
            "loading": self.loading,
            "rest": self.rest,
            "performance_notes": self.performance_notes,
            "complete": self.complete
        }