from mongoengine import Document, StringField, ListField, EmbeddedDocumentField, EmbeddedDocumentListField, ReferenceField, DateField, FloatField, DictField, EmbeddedDocument
from datetime import datetime

class WeightData(EmbeddedDocument):
    weight = ListField(FloatField())
    date = ListField(DateField(default=datetime.now().replace(second=0, microsecond=0)))
    
