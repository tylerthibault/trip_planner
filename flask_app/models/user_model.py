from flask_app.models import base_model
from flask import flash, session

class User(base_model.Base):
    table_name = "users"
    attributes = ['first_name', 'last_name', 'username', 'password']
    required_attributes = ['first_name', 'last_name', 'username', 'password']
    
    def __init__(self, data):
        super().__init__(data)

        # TODO: create attributes
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.password = data['password']

    @classmethod
    def validator(cls, **data):
        is_valid = super().validator(**data)

        if (data['password'] != data['confirm_password']):
            flash("Passwords do not match", "err_users_confirm_password")
            
        return is_valid