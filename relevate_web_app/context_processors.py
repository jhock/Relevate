def reset_url(request):
    from django.contrib.auth.views import password_reset
    return {'relevate_web_app.apps.profiles.templates.password_reset': password_reset}


def confirm_url(request):
    from django.contrib.auth.views import password_reset_confirm
    return {'relevate_web_app.apps.profiles.templates.password_reset_confirm': password_reset_confirm}


def done_url(request):
    from django.contrib.auth.views import password_reset_done
    return {'relevate_web_app.apps.profiles.templates.password_reset_done': password_reset_done}
