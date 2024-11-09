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

    def edit_details(self, reps="", loading="", rest="", perfomance_notes=""):
        edit_fields = {}
        response = {}
        if reps > 0:
            edit_fields['reps'] = reps
            response['updated_reps'] = f'{reps = }'
        if rest > 0:
            edit_fields['rest'] = rest
            response['updated_rest'] = f'{rest = }'
        if loading > 0:
            edit_fields['loading'] = loading
            response['updated_loading'] = f'{loading = }'
        if len(perfomance_notes) > 0:
            edit_fields['performance_notes'] = perfomance_notes
            response['updated_performance_notes'] = f'{perfomance_notes = }'
        if len(response) < 1:
            response['message'] = 'No details to update provided!'
        return response
        
    
    def mark_complete(self):
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