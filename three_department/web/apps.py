from django.apps import AppConfig


# 定义一个WebConfig类，继承自AppConfig
class WebConfig(AppConfig):
    # 设置默认的自动字段类型为BigAutoField
    default_auto_field = 'django.db.models.BigAutoField'
    # 设置应用的名称为web
    name = 'web'
