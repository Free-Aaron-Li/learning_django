from django.middleware.security import SecurityMiddleware
from django.shortcuts import redirect


class AuthMiddleware(SecurityMiddleware):
    def process_request(self, request):
        # 1. 不用登陆即可访问
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 2. 必须登陆才能访问的
        info_dict = request.session.get('info')
        if not info_dict:
            return redirect("/login/")

        request.info_dict = info_dict
