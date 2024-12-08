from mongoengine import Document, StringField, ListField, ReferenceField, BooleanField, EmbeddedDocument, IntField, FloatField

class SetDicts(EmbeddedDocument):
    set_order = IntField() # Total sets of all exercises in performance order
    exercise_name = StringField(required=True)
    set_number = IntField() # This should be a count of how many sets for each exercise
    set_type = StringField() # Warm up, working/normal, dropset, superset, partials, 21s, finisher, etc.
    reps = IntField()
    loading = FloatField()
    focus = StringField() # Max load, form, ROM, patterning movement
    rest = FloatField()
    notes = StringField()
    complete = BooleanField(default=False) # Has the set been performed

    def toggle_complete(self):
        if self.complete == False:
            self.complete = True
        elif self.complete == True:
            self.complete = False

    def add_notes(self, notes):
        self.notes = notes

    def delete_notes(self):
        self.notes = None

    def to_dict(self):
        return {
                'set_order' : self.set_order,
            'exercise_name' : self.exercise_name,
            'set_number' : self.set_number,
            'set_type' : self.set_type,
            'reps' : self.reps,
            'loading' : self.loading,
            'focus' : self.focus,
            'rest' : self.rest,
            'notes' : self.notes,
            'complete' : self.complete
        }