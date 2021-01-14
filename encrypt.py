from werkzeug.security import generate_password_hash, check_password_hash

def encrypt_password(password):
    return generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

def check_password(password, hash):
    return check_password_hash(hash, password)

if __name__ == "__main__":
    choice = input("Encrypt password or check password? ")
    password = input("Password: ")
    if choice.lower() == "encrypt":
        print(encrypt_password(password))
    else:
        hash = input("password hash: ")
        print(check_password(password, hash))

