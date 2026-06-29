from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not value.startswith("+"):
        raise ValidationError(
            "Phone number must start with country code."
        )


def validate_country_code(value):
    if not value.startswith("+"):
        raise ValidationError(
            "Invalid country code."
        )


