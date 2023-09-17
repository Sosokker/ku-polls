import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

log = logging.getLogger("django")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# !https://stackoverflow.com/questions/37618473/how-can-i-log-both-successful-and-failed-login-and-logout-attempts-in-django
@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = get_client_ip(request)

    log.info('Login User: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = get_client_ip(request)

    log.info('Logout User: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    log.warning('Login Failed for: {credentials}'.format(
        credentials=credentials,
    ))
