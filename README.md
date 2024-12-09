Сервис реферальной системы с авторизацией по номеру телефона

Реализована логика и API для следующего функционала:

Авторизация по номеру телефона. Первый запрос на ввод номера телефона. Отправка 4х-значного кода авторизации. Второй запрос на ввод кода.
Если пользователь ранее не авторизовывался, то он записывается в бд.
Пользователю при первой авторизации присваивается рандомно сгенерированный 6-значный инвайт-код.
В профиле у пользователя имеется возможность ввести чужой инвайт-код, который отображается в виде номера телефона реферера.
В API профиля выводится список пользователей(номеров телефона), которые ввели инвайт код текущего пользователя.
Процесс Авторизации начинается на эндпойнте login/ и завершается выдачей JWT токена. Проект развернут на виртуальной машине http://158.160.123.22/

message auth API

[POST] /login/

Первый запрос на ввод номера телефона и отправку смс-сообщения. Возвращает sms-token для предоставления в хедере второго запроса. JWE токен зашифрован 256 битным ключом, lifetime=3m, в полезной нагрузке содержит отправленный смс-код.

Request:

{
    "phone": "+79123456789"
}
Response:

{
    "sms-token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..lBm8N4NQxiScPbe6eaBOag.lU04QuOInUbWA8JrfKh0pEnINGVePqarxy-gz-nUYP4rb0ANULa1bz35pi_DAUSYFSf4Xv3aLB3D1wC-OwC96P2cnzjBM3dT2sFNGr3s72BC-sulY2xz2bnfnOqXqg_H76QZNnQDRh_iACuH215jGlnEsLc6fdF-pgGz_i9AuL84psnVT88-usO5jo9T4ekZoEO-Fi1c-giwdADeZ2PbESHqVBnDxe-e0YTEpEiJbAstMxAp0hAfaNQ3nLRPTes6x7ns6BPt3MLaFnjQt_U4LaIgPkgGJfCw8W8BBaHqEC-H.6P_NAUqZst7fY9IzV5ym_A",
    "url_to_redirect": "/login/sms-confirm/",
    "fields_to_be_required": [
        "sms_code"
    ]
}
[POST] /login/sms-confirm/

Второй запрос на ввод смс-сообщения. В хедер запроса необходимо добавить JWE токен. Возвращает JWT bearer_token.

Request header:

{
    "sms-token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..lBm8N4NQxiScPbe6eaBOag.lU04QuOInUbWA8JrfKh0pEnINGVePqarxy-gz-nUYP4rb0ANULa1bz35pi_DAUSYFSf4Xv3aLB3D1wC-OwC96P2cnzjBM3dT2sFNGr3s72BC-sulY2xz2bnfnOqXqg_H76QZNnQDRh_iACuH215jGlnEsLc6fdF-pgGz_i9AuL84psnVT88-usO5jo9T4ekZoEO-Fi1c-giwdADeZ2PbESHqVBnDxe-e0YTEpEiJbAstMxAp0hAfaNQ3nLRPTes6x7ns6BPt3MLaFnjQt_U4LaIgPkgGJfCw8W8BBaHqEC-H.6P_NAUqZst7fY9IzV5ym_A",
}
Request body:

{
    "sms_code": "1234"
}
Response:

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEzMjI0NDczLCJpYXQiOjE3MTMyMTU0NzMsImp0aSI6ImQwODNjNzBjNzMzYTQ2NWZhOThhYjlhYmY4NjY2ODgzIiwidXNlcl9pZCI6Mn0.y-KioHdCS1W2KSfJFtDiogx4lwQOadbfMBgixBgXscI",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMzMwMTg3MywiaWF0IjoxNzEzMjE1NDczLCJqdGkiOiJjM2I3ZmEzZTM5MzQ0ZTYyOGU3MmY0M2NiOGY2ZGI0OCIsInVzZXJfaWQiOjJ9.1Rmq8K166wSTsRTj8A811bPr7h6TzwjOIz3b5hFmABU"
}
Profile API

[GET], [PUT], [PATCH], [DELETE] /profile/

Собственный профиль (защищен авторизацией - Authorization: Bearer token).

Response:

{
    "first_name": "Andrey",
    "last_name": "Potapov",
    "email": "potapov@mail.ru",
    "phone": "79123456789",
    "invitation_code": "QBX27C",
    "invited_by": "79012345678",
    "invited_users_phones": [
        "79999999999"
    ]
}
[POST] /profile/invitation/

Ввод реферального кода (защищен авторизацией - Authorization: Bearer token).

Request:

{
    "invitation_code": "QBX27C"
}
Response:

{
    "invited_by": "79123456789"
}