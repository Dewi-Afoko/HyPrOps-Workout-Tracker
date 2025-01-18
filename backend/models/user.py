from mongoengine import Document, StringField, ListField, EmbeddedDocumentField, EmbeddedDocumentListField, ReferenceField, DateField, FloatField, DictField
from werkzeug.security import generate_password_hash, check_password_hash
from models.workout import Workout
from datetime import datetime

date_format = "%Y/%m/%d"

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(required=False)
    height = FloatField(required=False)
    weight = DictField()
    dob = DateField(required=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password)
        self.save()

    def update_password(self, password):
        self.password = generate_password_hash(password)
        self.save()

    def update_personal_details(self, name=None, dob=None, height=None, weight=None):
        if name is not None:
            try:
                self.name = self._validate_name(name)
            except AttributeError:
                raise AttributeError("Name must be a string")
        if dob is not None:
            self.dob = self._validate_dob(dob)  
        if height is not None:
            self.height = self._validate_is_number(height, "height") 
        if weight is not None:
            weight = self._validate_is_number(weight, "weight")
            self.weight[datetime.now().strftime(date_format)] = weight
        self.save()

    def to_dict(self):
        payload = {
            'id' : str(self.id),
            'username' : self.username,
            'name': self.name,
            'height': self.height,
            }
        if self.dob != None:
            payload['dob'] = self.dob.strftime(date_format)
        if len(self.weight )> 0 :
            latest_weigh_in = max(self.weight, key=lambda date: datetime.strptime(date, date_format))
            payload['weight'] = self.weight[latest_weigh_in]
            payload['last_weighed_on'] = latest_weigh_in

        return payload

    def _validate_name(self, name):
        if isinstance(name, str) and len(name.strip()) > 0:
            return name
        raise ValueError(f"Name must be a string, got {type(name).__name__}")

    def _validate_dob(self, dob):
        if isinstance(dob, str):
            try:
                return datetime.strptime(dob, date_format)
            except ValueError:
                raise ValueError(f"Date of birth must be in YYYY/MM/DD format, got {dob}")
        raise ValueError(f"Date of birth must be a string, got {type(dob).__name__}")

    def _validate_is_number(self, value, field_name):
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"{field_name} must be a number, got {value}")


        

