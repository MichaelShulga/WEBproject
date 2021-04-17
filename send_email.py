import smtplib
import ssl

port = 465  # For SSL
email = 'AuthorizationService@yandex.com'
password = 'AuthService2k'

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(email, password)
    # TODO: Send email here