import string
from django.core.exceptions import ValidationError

class ModDrivePasswordValidator:
    def validate(self, password, user=None):
        errors = []
        if not any(char.isupper() for char in password):
            errors.append(
                "Password must contain at least one uppercase letter."
            )
        if not any(char in string.punctuation for char in password):
            errors.append(
                "Password must contain at least one special character."
            )
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return "Your password must contain at least one uppercase letter and one special character."
    
