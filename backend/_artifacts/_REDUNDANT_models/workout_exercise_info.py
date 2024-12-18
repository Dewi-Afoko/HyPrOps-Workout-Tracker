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

    def edit_details(self, reps_index=None, reps_value=None,
                loading_index=None, loading_value=None,
                rest_index=None, rest_value=None,
                performance_notes_index=None, performance_notes_value=None):
        response = {}

    # Update specific reps entry if index and value are provided
        if reps_index is not None and reps_value is not None:
            if 0 <= reps_index < len(self.reps):
                self.reps[reps_index] = reps_value
                response['updated_reps'] = f'reps[{reps_index}] = {reps_value}'
            else:
                response['reps_error'] = f'Index {reps_index} out of range for reps'

    # Update specific loading entry if index and value are provided
        if loading_index is not None and loading_value is not None:
            if 0 <= loading_index < len(self.loading):
                self.loading[loading_index] = loading_value
                response['updated_loading'] = f'loading[{loading_index}] = {loading_value}'
            else:
                response['loading_error'] = f'Index {loading_index} out of range for loading'

    # Update specific rest entry if index and value are provided
        if rest_index is not None and rest_value is not None:
            if 0 <= rest_index < len(self.rest):
                self.rest[rest_index] = rest_value
                response['updated_rest'] = f'rest[{rest_index}] = {rest_value}'
            else:
                response['rest_error'] = f'Index {rest_index} out of range for rest'

    # Update specific performance notes entry if index and value are provided
        if performance_notes_index is not None and performance_notes_value is not None:
            if 0 <= performance_notes_index < len(self.performance_notes):
                self.performance_notes[performance_notes_index] = performance_notes_value
                response['updated_performance_notes'] = f'performance_notes[{performance_notes_index}] = {performance_notes_value}'
            else:
                response['performance_notes_error'] = f'Index {performance_notes_index} out of range for performance notes'

    # If no fields were updated, return a default message
        if not response:
            response['message'] = 'No details to update provided or indices out of range'

        return response
        
    
    def mark_complete(self):
        if self.complete == False:
            self.complete = True
 
        elif self.complete == True:
            self.complete = False


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
    
    def delete_details(self, reps_index=None,
                    loading_index=None,
                    rest_index=None,
                    performance_notes_index=None):
        response = {}

        # Delete entries from reps
        if reps_index is not None:
            for index in sorted(reps_index, reverse=True):  # Sort indices in reverse to avoid shifting issues
                if 0 <= index < len(self.reps):
                    del self.reps[index]
                else:
                    response['reps_error'] = f"Index {index} out of range for reps"
            if 'reps_error' not in response:
                response['updated_reps'] = f"Indices {reps_index} deleted from reps"

        # Delete entries from loading
        if loading_index is not None:
            for index in sorted(loading_index, reverse=True):
                if 0 <= index < len(self.loading):
                    del self.loading[index]
                else:
                    response['loading_error'] = f"Index {index} out of range for loading"
            if 'loading_error' not in response:
                response['updated_loading'] = f"Indices {loading_index} deleted from loading"

        # Delete entries from rest
        if rest_index is not None:
            for index in sorted(rest_index, reverse=True):
                if 0 <= index < len(self.rest):
                    del self.rest[index]
                else:
                    response['rest_error'] = f"Index {index} out of range for rest"
            if 'rest_error' not in response:
                response['updated_rest'] = f"Indices {rest_index} deleted from rest"

        # Delete entries from performance_notes
        if performance_notes_index is not None:
            for index in sorted(performance_notes_index, reverse=True):
                if 0 <= index < len(self.performance_notes):
                    del self.performance_notes[index]
                else:
                    response['performance_notes_error'] = f"Index {index} out of range for performance notes"
            if 'performance_notes_error' not in response:
                response['updated_performance_notes'] = f"Indices {performance_notes_index} deleted from performance notes"

        # If no updates were made
        if not response:
            response['message'] = 'No valid details to delete or indices out of range'

        return response
