"""
@Author：WangYuXiang
@E-mile：Hill@3io.cc
@CreateTime：2021/4/22 9:53
@DependencyLibrary：无
@MainFunction：无
@FileDoc：
    app_helper.py
    文件说明
@ChangeHistory:
    datetime action why
    example:
    2021/4/22 9:53 change 'Fix bug'

"""
import logging
from functools import partial
from importlib import import_module
from pathlib import Path
from sanic_plugin_toolkit import SanicPlugin

ALL_METHOD = {'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'}


def get_module_urls(module_path) -> list:
    """
    得到app中的urls
    :param module_path:
    :return:
    """
    module_path = '%s.urls' % module_path
    try:
        module = import_module(module_path)
    except ModuleNotFoundError:
        return False, None
    return True, getattr(module, 'urls')


def get_module_models(module_path):
    """
    得到app中的models
    :param module_path:
    :return:
    """
    module_path = '%s.models' % module_path
    try:
        import_module(module_path)
    except ModuleNotFoundError:
        return False, None
    return True, module_path


def get_module_blueprint(module_path, module_name):
    """
    得到app的蓝图
    :param module_path:
    :param module_name:
    :return:
    """
    return getattr(import_module(module_path, module_name), module_name)


def set_route(endpoint, route):
    """为urls中的methods提供缺省参数"""
    if 'methods' not in route:
        route['methods'] = ALL_METHOD
    endpoint.add_route(**route)


def load_route(app, bp, routes):
    """
    循环添加路由到指定端点

    :param app: app实例
    :param bp: 蓝图实例
    :param routes: 路由列表
    """
    for route in routes:
        is_base = route.pop('is_base', False)
        if is_base:
            set_route(app, route)
        else:
            set_route(bp, route)


class AppStructureError(Exception):
    pass


class AppsHelper(SanicPlugin):
    """
    一个app应用加载器
    可以方便快捷的加载和管理apps程序

    :param SanicPlugin: sanic插件管理框架
    """

    def __init__(self):
        self.apps = {}
        self.routers = []
        self.models = {}
        super(AppsHelper, self).__init__()

    def on_registered(self, context, reg, *args, **kwargs):
        """
        插件注册时调用的事件

        :param context: 插件上下文，可以用来存储内容
        :param reg: 已注册的内容
        :raises AppStructureError: APP结构错误异常
        """
        info = partial(context.log, logging.INFO)
        warn = partial(context.log, logging.WARN)
        info('Start load app.')
        app = context.app
        config = app.config
        app_modules = self.get_app_modules(config)

        for module_name, module_path in app_modules.items():
            # 检查app结构
            info('{}Start loading [{}] application.{}'.format('-' * 15, module_name, '-' * 15))
            try:
                blueprint = get_module_blueprint(module_path, module_name)
            except ModuleNotFoundError as exc:
                raise AppStructureError('未找到 %s 程序' % module_path)
            except AttributeError as exc:
                raise AppStructureError('app程序必须包含 __init__.py 模块。')
            self.apps[module_name] = {
                'bp': blueprint,
                'path': Path(import_module(module_path).__file__).parent
            }
            models_exists, models = get_module_models(module_path)
            urls_exists, urls = get_module_urls(module_path)
            if models_exists:
                self.models[module_name] = [models]
                info('\t\tModels finish.')
            else:
                warn('\t\tNot find models.')
            if urls_exists:
                self.routers.extend(urls)
                load_route(app, blueprint, urls)
                info('\t\tRegistered route finish.')
            else:
                warn('\t\tNot find urls.')
            app.blueprint(blueprint)
            info('\t\ttRegistered Blueprint finish.')
        info('The {} applications are loaded.'.format(len(app_modules)))

    def get_app_modules(self, config):
        app_modules = config.get('APP_MODULES', {})
        if not config.AUTO_LOAD_APPS:
            return app_modules
        apps_path = config.APPS_FOLDER_PATH
        folder_paths = Path(apps_path).iterdir()
        for folder_path in folder_paths:
            if (folder_path / '__init__.py').exists():
                app_modules[folder_path.name] = '%s.%s' % (config.APPS_FOLDER_NAME, folder_path.name)
        return app_modules

apps_helper = AppsHelper()
__all__ = ['apps_helper', 'AppsHelper']
