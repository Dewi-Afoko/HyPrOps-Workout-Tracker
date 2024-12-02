from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, BooleanField, EmbeddedDocumentField
from datetime import datetime


class Workout(Document):
    user_id = ReferenceField('User', required=True)
    workout_name = StringField()
    date = DateTimeField(default=datetime.now)
    complete = BooleanField(default=False)
    set_list = ListField(EmbeddedDocumentField(), default=list)
    
#TODO: Create the logic for this blueprint to follow

    def toggle_complete(self):
        if self.complete == False:
            self.complete = True
            self.save()
        elif self.complete == True:
            self.complete = False
            self.save()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    