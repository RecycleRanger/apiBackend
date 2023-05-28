import secrets
import string


def get_passwords(
        num: int,
        pwd_length: int = 21,
) -> list[str]:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return [''.join([secrets.choice(alphabet) for _ in range(pwd_length)]) for _ in range(num)]
