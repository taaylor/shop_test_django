import uuid
from datetime import timedelta

from celery import shared_task

from django.utils.timezone import now

from users.models import User, EmailVerification

@shared_task
def send_email_verify(user_id):
    user = User.objects.get(id=user_id)
    experation = now() + timedelta(hours=48)
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, experation=experation)
    record.send_verification_email()