import base64
import hashlib
import datetime
import calendar
import jwt
from flask import current_app
from flask_restx import abort


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )

def generate_password_hash(password):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),   # кодирование пароля в бинарное представление, т.к. pbkdf2_hmac работает именно с ними
        current_app.config["PWD_HASH_SALT"],
        current_app.config["PWD_HASH_ITERATIONS"]
    ).decode("utf-8", "ignore")     # декодирование бинарного представления в сроковое
    # return bace64.b64encode(hash_digest) # перевод цифрового шифра в строку, где hash_digest то что возвращает hashlib.pbkdf2_hmac

# def generate_password_hash(password: str) -> str:
#     return base64.b64encode(__generate_password_digest(password)).decode('utf-8')

# TODO: [security] Описать функцию compose_passwords(password_hash: Union[str, bytes], password: str)

# Пример compare_passwords - сравнения паролей:
# def compare_passwords(hash_user: Union[str, bytes], input_password: str):
#     """ Проверка пароля из request, пароля в БД """
#     return hmac.compare_digest(
#         base64.b64decode(hash_user),
#         hashlib.pbkdf2_hmac(
#             'sha256',
#             input_password.encode('utf-8'),
#             salt=current_app.config["PWD_HASH_SALT"],
#             iterations=current_app.config["PWD_HASH_ITERATIONS"]
#         )
#     )

def compare_passwords(password_hash, other_password):
    """

    :param password_hash: - Пароль из БД.
    :param other_password: - Пароль, который прислал пользователь.
    :return:
    """
    return password_hash == generate_password_hash(other_password)

def generate_tokens(user_data, ):

    # # Вариан (добавить: password_hash, refresh=False), тереноса проверки из check_user сюда:
    # if not refresh:
    #     if not compare_passwords(password_hash=password_hash, other_password=user_data['password']):
    #         return None

    #access_token на 30 минут.
    min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
    user_data['exp'] = calendar.timegm(min15.timetuple())
    access_token = jwt.encode(user_data, key=current_app.config['SECRET_KEY'],
                              algorithm=current_app.config['ALGORITHM'])

    # refresh_token на 130 дней.
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
    user_data['exp'] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(user_data, key=current_app.config['SECRET_KEY'],
                              algorithm=current_app.config['ALGORITHM'])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

## Варианты:
# def generate_tokens(self, user_data):
#     # access_token на 30 минут.
#     min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
#     user_data['exp'] = calendar.timegm(min15.timetuple())
#     access_token = jwt.encode(user_data, SECRET, algorithm=ALGO)
#
#     # refresh_token на 130 дней.
#     days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
#     user_data['exp'] = calendar.timegm(days130.timetuple())
#     refresh_token = jwt.encode(user_data, SECRET, algorithm=ALGO)
#
#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token
#     }

# def  refresh_tokens(refresh_token):
#     data = jwt.decode(refresh_token, key=current_app.config['SECRET_KEY'],
#               algorithms=current_app.config['ALGORITHM'])
#
#     email = data.get("email")
#     password = data.get("password")
#
#     return generate_tokens(email=email, password=password, password_hash=None, refresh=True)

def refresh_tokens(token):
    refresh_token = token.get("refresh_token", None)

    if refresh_token is None:
        abort(400)

    try:
        data = get_data_by_token(refresh_token)
    except Exception as e:
        print(f"Возникла ошибка: {e}")
        abort(401)

    user_data = {
        "email": data['email'],
        "password": data['password']
    }

    return user_data

def get_data_by_token(token):
    data = jwt.decode(token, key=current_app.config['SECRET_KEY'],
                      algorithms=current_app.config['ALGORITHM'])

    return data