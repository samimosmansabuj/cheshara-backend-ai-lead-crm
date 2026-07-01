from django.db import models

class DeviceType(models.TextChoices):
    ANDROID = "ANDROID", "Android"
    IOS = "IOS", "iOS"
    WEB = "WEB", "Web"

class OTPPurpose(models.TextChoices):
    LOGIN = "LOGIN", "Login"
    REGISTER = "REGISTER", "Register"
    PASSWORD_RESET = "PASSWORD_RESET", "Password Reset"
    PHONE_VERIFY = "PHONE_VERIFY", "Phone Verification"
    EMAIL_VERIFY = "EMAIL_VERIFY", "Email Verification"

class LoginMethod(models.TextChoices):
    PASSWORD = "PASSWORD", "Password"
    OTP = "OTP", "OTP"
    EMAIL_OTP = "EMAIL_OTP", "Email OTP"
    GOOGLE = "GOOGLE", "Google"
    APPLE = "APPLE", "Apple"
    FACEBOOK = "FACEBOOK", "Facebook"
    BIOMETRIC = "BIOMETRIC", "Biometric"


class LoginStatus(models.TextChoices):
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"
    BLOCKED = "BLOCKED", "Blocked"
    LOCKED = "LOCKED", "Locked"
    EXPIRED = "EXPIRED", "Expired"
    INVALID_OTP = "INVALID_OTP", "Invalid OTP"
    INVALID_PASSWORD = "INVALID_PASSWORD", "Invalid Password"

