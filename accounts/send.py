from django.core.mail.message import EmailMessage


def send_email():
    subject = "메시지"
    to = ['aaa@bbb.com']
    from_email = 'dune2011@naver.com'
    message = "메시지를 성공적으로 전송"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()

def send_mail(subject, message, recipient_list=None):
	from django.conf import settings
	default_recipient_list = ['shoark7@gmail.com']
	send_mail(
		subject=subject,
		message=message,
		from_email=settings.EMAIL_HOST_USER, #!
		recipient_list=recipient_list if recipient_list else default_recipient_list
)
