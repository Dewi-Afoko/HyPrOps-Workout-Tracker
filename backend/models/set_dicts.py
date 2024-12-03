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
    complete = BooleanField() # Has the set been performed