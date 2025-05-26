# Заглушки без настоящей базы данных
_fake_db = {
    "+79998887766": {"role": "admin"},
    "+71112223344": {"role": "user"}
}

def check_user(phone_number):
    user = _fake_db.get(phone_number)
    if user:
        return user["role"]
    return None

def register_user(data):
    _fake_db[data['phone']] = {
        "role": "user",
        "name": data["name"],
        "surname": data["surname"],
        "email": data["email"],
        "age": data["age"],
        "city": data["city"]
    }

def user_exists(phone_number: str) -> bool:
    return phone_number in _fake_db

def set_role(phone_number: str, new_role: str):
    if user_exists(phone_number):
        _fake_db[phone_number]["role"] = new_role
