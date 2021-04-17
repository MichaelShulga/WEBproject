from requests import post

EMAIL = 'AuthorizationService@yandex.com'
PASSWORD = 'AuthService2k'

print(post('https://api.sendpulse.com/smtp/domains',
           json={'email': EMAIL}).json())
