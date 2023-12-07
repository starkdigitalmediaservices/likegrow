OTP_EXPIRE_MINUTE_TIME = 15

STATUS_ACTIVE = 1
STATUS_INACTIVE = 2
STATUS_DELETED = 3

SUPER_ADMIN_ROLE = 1

FEMALE = 2
MALE = 1
OTHER = 3

SUPERUSER_ROLE = 1
STAFF = 2

BASE_URL = 'http://127.0.0.1:8000/api/v1/'
ACCESS_KEY = "AE698wLwHGPLvtuzF46V4P2h4yh3ru2MmkBKpsEA7bzQSHjQ3F"

MESSAGES = {
    "username_password_required": "Username and password are required. ",
    "invalid_username_and_password": "Invalid username or password. Please try again.",
    "email_not_provided": "Email not provided.",
    "forget_password_email_subject": "Stark Employee Portal reset Password",
    "send_email_otp_email_subject": "OTP for email verification",
    "password_confirm_password_invalid": "Password and confirm password does not match.",
    "created": " created successfully.",
    "updated": " updated successfully.",
    "deleted": " deleted successfully.",
    "not_found": " not found.",
    "email_not_exist":"Email not exists.",
    "username_not_exist":"Username not exists.",
    "user_inactive":"User is inactive.",
    "user_deleted":"User is deleted."
}

FORGET_PASSWORD_TOKEN_EXPIRY_IN_SEC = 24 * 60 * 60
