from passlib.hash import argon2


def hash_password(password: str) -> str:
    # argon2.encrypt is deprecated; use .hash
    return argon2.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return argon2.verify(password, hashed)
