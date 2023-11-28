import re
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import PBKDF2PasswordHasher

User = get_user_model()


def validate_email(email):
    # Regular expression pattern for email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"  # abc@gmail.com
    return re.match(pattern, email)


def authenticate_user(password, username=None, email=None):
    if not username and not email:
        return
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return
    else:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return
    hasher = PBKDF2PasswordHasher()
    return user if hasher.verify(password, user.password) else None
 