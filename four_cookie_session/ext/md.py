from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 1. 如果是登陆界面，直接往后运行
        # 在其他框架可能会存在拦截/static目录下的情况，需要额外声明一下
        if request.path == '/login/' or request.path == '/static/':
            return

        # 2. 如果是需要进行登陆操作的页面，需要判断登陆条件：
        # 无返回值或返回None，继续往下走
        # return None
        # 有返回值 redirect render http...
        info_dict = request.session.get('info')
        if info_dict:
            # 继续往下走
            # 主动给request中赋值
            request.info_dict = info_dict
            return
        else:
            return redirect('/login/')
