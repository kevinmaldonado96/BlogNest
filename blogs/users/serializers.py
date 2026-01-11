import re
from rest_framework import serializers
from .models import IdentityType, User, PersonalInformation
from validate_email_address import validate_email
from rest_framework import serializers


class UserRegistrationSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    identity_type = serializers.CharField(max_length=50)
    identity_number = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    
    def validate_identity_type(self, value: str):
        identity_type_exist = IdentityType.objects.filter(code=value).exists()
        if not identity_type_exist:
            raise serializers.ValidationError("Identity type invalid, please try with other option")
        return value
    
    def validate_identity_number(self, value: str):
        if not value.isnumeric():
            raise serializers.ValidationError("Identity number has to be a number, please fix it")
        return value
    
    def validate_email(self, value: str):
        if not validate_email(value):
            raise serializers.ValidationError("Email is not valid, please fix it")
        return value
    
    def validate_password(self, value: str):
        """
        Field-level validation for password.
        Enforce at least one uppercase, one lowercase, one special char, and one number.
        """
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r"[@$!%*?&]", value):
            raise serializers.ValidationError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
        
        return value

    def validate_username(self, value: str):
        user_exist = User.objects.filter(username=value).exists()
        if user_exist:
            raise serializers.ValidationError("User exist, please try with another username")
        return value
    
    def validate(self, data):
        
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        
        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        
        return data
        
    
    def create(self, data):
        
        identity_type = IdentityType.objects.filter(code = data.get("identity_type")).first()
        
        personal_information_user = PersonalInformation.objects.create(
            name = data.get("name"),
            lastname = data.get("lastname"),
            identity_type = identity_type,
            identity_number = data.get("identity_number"),
            email = data.get("email")
        ) 
                
        user = User.objects.create_user(
           username = data.get("username"),
           email = data.get("email"),
           password = data.get("password"),
           personal_information = personal_information_user
        )
        
        return {"user_id": user.id, "username: ": user.username}

        