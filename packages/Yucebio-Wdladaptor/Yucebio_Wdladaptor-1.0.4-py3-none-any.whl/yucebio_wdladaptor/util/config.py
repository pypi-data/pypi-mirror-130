import json
import requests
from typing import Any, TypedDict
from yucebio_config import Config as BaseConfig

from yucebio_wdladaptor.util.gist import Gist


class ServerConfig(TypedDict):
    platform: str
    host: str
    global_path: str
    simg_path: str
    runtimes: str
    backend: str    # == platform

class WorkflowJob(TypedDict):
    cromwell_id: str
    server: str

# 配置文件的版本
LATEST_CONFIG_VERSION = 4

class Config(BaseConfig):
    SNIPPET_TITLE = "Yucebio Wdladaptor Config"
    SNIPPET_FILE_NAME = "yucebio_wdladaptor_config.json"

    def __init__(self, name: str = "wdladaptor", path: str = None, check_login = True) -> None:
        super().__init__(name=name, path=path)
        self.load()
        self.check_version()

        self.sync_config = BaseConfig("sync_credentials")
        if check_login:
            self.validate_login()

    @property
    def servers(self) -> dict[str, ServerConfig]:
        """管理Cromwell Server配置项"""
        return self.config.get('server', {})

    def add_server(self, platform_alias: str = None, new_config: dict = None) -> dict:
        return self.add_cromwell_backend(platform_alias, new_config)

    def add_cromwell_backend(self, platform_alias: str = None, new_config: dict = None) -> dict:
        """查询或更新服务器配置:  cromwell api地址， 公共目录以及simg目录必须配置
        1. 查询              c = adaptor.config()
        2. 查询指定配置      c  = adaptor.config('aws')
        3. 更新指定配置       adaptor.config('aws', {...})
        """
        server_config = self.servers

        if platform_alias:
            platform_alias = platform_alias.lower()
            if new_config:
                server_config[platform_alias] = new_config
                self.set('server', server_config)
            return server_config.get(platform_alias, {})
        return self.servers

    def get_server(self, server_alias: str) -> ServerConfig:
        return self.get_cromwell_backend(server_alias)
    
    def get_cromwell_backend(self, server_alias: str = None) -> ServerConfig:
        if not self.servers:
            raise RuntimeError("未配置Backend")

        if not server_alias:
            all_alias = list(self.servers.keys())
            if len(all_alias) != 1:
                raise RuntimeError(f"请指定backend别名: {all_alias}")
            server_alias = all_alias[0]
        return self.servers.get(server_alias, {})

    def del_server(self, server_alias: str):
        return self.del_cromwell_backend(server_alias)

    def del_cromwell_backend(self, server_alias: str):
        servers = self.servers
        if server_alias in servers:
            del servers[server_alias]
        self.set('server', servers)

    @property
    def jobs(self) -> list[WorkflowJob]:
        """管理已投递的所有作业"""
        return self._config.get("workflows", [])

    def add_job(self, jobid: str, server_alias: str):
        jobs = self.jobs
        jobs.append({
            "cromwell_id": jobid, "server": server_alias
        })
        self.set('workflows', jobs)
        return jobs

    def set(self, key: str, value: Any, quiet=True):
        self._config[key] = value
        self.reload()
        self.upload_config()

    def get(self, key: str, default = None):
        return self.config.get(key, default)

    def check_version(self):
        """检查配置版本信息。并根据需要自动完成配置升级

        Version 1: 支持多个cromwell server配置
        Version 2: 将cromwell backend配置合并到service字段内
        Version 3: 修改cromwell backend配置，增加一个冗余的backend子字段
        """
        if not self._config:
            return
        config_version = self.get("version", 1)
        if config_version >= LATEST_CONFIG_VERSION:
            return config_version

        # 避免循环引入，直接在函数内导入所需模块
        from yucebio_wdladaptor.backend import SUPPORTTED_BACKENDS

        server_config = self.servers
        # Version 1时，backend直接保存在跟配置项中，需要将cromwell配置收集到二级字段内，从而允许相同backend存在多个cromwell配置
        for backend_name in SUPPORTTED_BACKENDS:
            # Version 2->3: 使用backend替代platform
            # Version 3->4: 新增cromwell配置时，忘记设置backend, 修改配置逻辑，并在这里强制转换下
            # item = dict(server_config.pop(backend_name))
            # item.update({
            #     "backend": backend_name
            # })
            if backend_name in self._config:
                backend_config = self._config.pop(backend_name)
                backend_config['platform'] = backend_name
                backend_config['backend'] = backend_name
                server_config[backend_name] = backend_config
        new_config = {}
        # Version 3->4: 新增cromwell配置时，忘记设置backend, 修改配置逻辑，并在这里强制转换下
        for alias, backend_config in server_config.items():
            # elif backend_name in server_config:
            # server_config[backend_name]['backend'] = backend_name
            item = {k:v for k,v in backend_config.items() if k not in ['platform']}
            if not item.get('backend'):
                item['backend'] = backend_config['platform']
            new_config[alias] = item

        self._config['server'] = new_config
        self._config['version'] = LATEST_CONFIG_VERSION
        self.reload()
        return LATEST_CONFIG_VERSION

    def pp(self, obj: Any = None):
        if obj == None:
            obj = self._config
        print(json.dumps(obj, indent=2, default=str))

    def set_sync_config(self, username: str, password: str, api: str, grant_type: str="password"):
        current_config = self.sync_config.config

        current_config.update({
            "username": username,
            "password": password,
            "api": api,
            "grant_type": grant_type
        })
        self.sync_config.init(current_config)

    def validate_login(self):
        """为了准确识别使用者身份，强制要求使用之提供认证信息
        """
        current_config = self.sync_config.config
        if not current_config:
            raise RuntimeError("未登录")
        self.get_gist(False)

    def get_gist(self, silent: bool = True) -> Gist:
        username = self.sync_config('username')
        password = self.sync_config('password')
        grant_type = self.sync_config('grant_type')
        api = self.sync_config('api')
        if not all([username, password, grant_type, api]):
            if not silent:
                raise RuntimeError("缺少Gitlab必要配置内容")
            return
        gist = Gist(username, password, api)
        if grant_type != 'password':
            if not silent:
                raise RuntimeError("仅支持通过用户名和密码的方式使用Gitlab")
            return

        gist.validate_api()
        return gist

    def get_exist_snippet(self, gist: Gist):
        title, file_name = self.SNIPPET_TITLE, self.SNIPPET_FILE_NAME
        # gist没有去重的逻辑，需要自己处理查重
        snippets = gist.query({"title": title, "file_name": file_name})
        if not snippets:
            return
        return snippets[0]

    def upload_config(self) -> str:
        """上传配置, 成功时返回配置链接
        """
        gist = self.get_gist()
        if not gist:
            return
        content = json.dumps(self._config, indent=2)
        exist = self.get_exist_snippet(gist)
        if exist:
            gist.update(exist, content)
        else:
            exist = gist.create(self.SNIPPET_TITLE, self.SNIPPET_FILE_NAME, content)
        return f"{gist.api}/snippets/{exist['id']}"

    def download_config(self, silent = False):
        """下载配置，成功时，返回下载地址
        """
        gist = self.get_gist(silent=False)
        exist = self.get_exist_snippet(gist) 
        if not exist:
            if not silent:
                raise RuntimeError("没有找到可用的配置")
            return
        content: dict = json.loads(gist.get_content(exist['id']))
        self.init(content)
        return f"{gist.api}/snippets/{exist['id']}"

    @property
    def api(self):
        return self.get('api_service', '').strip('/')

    def set_api_service(self, api: str):
        rsp = requests.get(api)
        self.set('api_service', api)
        return rsp.json()

    def validate_api(self, host: str, port: int):
        # TODO: 验证api地址是否有效
        return True