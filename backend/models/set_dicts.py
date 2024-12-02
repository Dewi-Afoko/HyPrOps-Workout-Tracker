from mongoengine import Document, StringField, ListField, ReferenceField, BooleanField, EmbeddedDocument, IntField, FloatField

class SetDicts(EmbeddedDocument):
    exercise_name = StringField(required=True)
    set_count = IntField() #TODO: Check how we can make this indicate the number of SetDicts with this exercise name - len(some_function(exercise_name))...?
    set_type = StringField()
    reps = IntField()
    loading = FloatField()
    focus = StringField()
    rest = FloatField()
    notes = StringField()
    complete = BooleanField()