from mongoengine import EmbeddedDocument, StringField

class PersonalData(EmbeddedeDocument):
    name = StringField()