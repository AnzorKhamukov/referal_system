import time

import requests
import secrets
import string
from datetime import datetime, timedelta
import jose
from jose import jwe, jwt
from rest_framework.exceptions import ValidationError
from referalsystem.settings import JWE_SECRET, SMS_SENDER_NUMBER, SMS_API_KEY, SMS_API_URL


def create_sms_jwe_token(credentials: dict) -> tuple[str, str]:
    """
    Создание зашифрованного JSON токена - JWE
    Возвращает кортеж (JWE-token, sms_code)
    """
    # Создание смс кода
    sms_code = create_sms_code()
    # Отправка смс
    send_sms(sms_code, credentials.get('phone'))
    # Задержка для имитации отправки смс
    time.sleep(2)
    now = datetime.utcnow()
    payload = {
        'iat': now,
        'nbf': now,
        'exp': now + timedelta(seconds=60 * 3),
        'credentials': dict(credentials),
        'sms_code': sms_code,
    }
    jwt_token = jwt.encode(claims=payload, key='')
    encrypted_token = jwe.encrypt(
        plaintext=jwt_token,
        key=JWE_SECRET
    ).decode('utf-8')

    return encrypted_token, sms_code


def create_sms_code() -> str:
    return ''.join(secrets.choice(string.digits) for _ in range(4))


def send_sms(sms_code: str, phone: str) -> None:
    text = f"{sms_code} - код для подтверждения номера телефона"
    headers = {'Authorization': f"Bearer {SMS_API_KEY}"}
    requests.post(
        url=SMS_API_URL,
        headers=headers,
        json={
            "number": SMS_SENDER_NUMBER,
            "destination": phone,
            "text": text
        }
    )


def decode_sms_token(token: str) -> dict:
    try:
        jwt_token = jwe.decrypt(jwe_str=token, key=JWE_SECRET)
    except (jose.exceptions.JWEError, jose.exceptions.JWEParseError):
        raise ValidationError('Invalid token')
    # Декодирование JWT
    try:
        return jwt.decode(token=jwt_token, key='')
    except jose.exceptions.JWTError:
        raise ValidationError(
            'Token lifetime is expired or invalid token is sent'
        )
