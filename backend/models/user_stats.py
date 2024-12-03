from mongoengine import EmbeddedDocument, IntField

class UserStats(EmbeddedDocument):
    weight = IntField()