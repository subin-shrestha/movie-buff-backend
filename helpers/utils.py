import string
from django.utils.crypto import get_random_string as get_random_str


def get_random_string(size=6, allowed_chars=string.ascii_uppercase + string.digits):
    return get_random_str(size, allowed_chars)

