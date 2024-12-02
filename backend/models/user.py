from mongoengine import Document, StringField, ListField, EmbeddedDocumentField
from werkzeug.security import generate_password_hash, check_password_hash

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)  # Stores hashed password
    workout_list = ListField()
    personal_data = EmbeddedDocumentField()

    #TODO: Create personal_data for weight, height, age/dob, potentially name, location, etc.

    def save(self, *args, **kwargs):
        # Check if the password is already hashed
        if not self.password.startswith('scrypt:'):
            self.password = generate_password_hash(self.password)
        super().save(*args, **kwargs)


    def update_password(self, password):
        # Hash the new password before updating
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        # Verify the given password against the stored hashed password
        return check_password_hash(self.password, password)

    def add_workout(self, workout):
        self.workout_list.append(workout)

    def __repr__(self):
        return f"User(username={self.username}, workout_list={self.workout_list})"

    def to_dict(self):
        return {
            "username": self.username,
            "workout_list": self.workout_list
        }

    def __eq__(self, other):
        if isinstance(other, User):
            return self.__dict__ == other.__dict__
        return False
