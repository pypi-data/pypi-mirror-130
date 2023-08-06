"""支持WDL API"""
import requests
from .config import Config
from .types import CromwellBackendType, RestfulResponseType, WorkflowType

class WDLAPI(object):
    API_PREFIXS = {
        "backend": "/api/v1/backend/",       # 管理backend
        "workflow": "/api/v1/workflow/",     # crowmell作业管理
    }

    def __init__(self) -> None:
        super().__init__()
        self.config = Config()
        self.api = self.config.api
        self.owner = self.config.get('owner')

    def submit(self, backend_name: str, jsonpath: str):
        url = self.api + self.API_PREFIXS['workflow']
        data = {
            "owner": self.owner,
            "backend_name": backend_name,
        }
        files = {"input": open(jsonpath, 'rb')}
        rsp = requests.post(url, data=data, files=files)
        return self.parse_restful_response(rsp.json())

    def parse_restful_response(self, response: RestfulResponseType):
        if response['code'] != 0:
            raise RuntimeError(response['message'])
        return response['message']

    def submit_action(self, action: str, data: dict, backend_name: str = None, primary_value: str = 'action', expect_response_type: str="json"):
        """提交自定义操作：中止、重投
        """
        backend = self.config.get_cromwell_backend(backend_name)

        # /{prefix}/{资源编号}/{操作名称}  或 /{prefix}/action/{操作名称}
        url = self.api + self.API_PREFIXS['workflow'] + primary_value + "/" + action
        item = {
            "owner": self.owner,
            "backend": backend['backend'],
            "alias": backend_name,
            **data
        }
        rsp = requests.post(url, data=item)

        if expect_response_type != 'json':
            return rsp

        rsp_data = rsp.json()   # type: RestfulResponseType

        if rsp_data['code'] != 0:
            raise RuntimeError(rsp_data['message'])
        return rsp_data['message']

    def get_workflows(self, filters: dict = None, paginations: dict = None):

        url = self.api + self.API_PREFIXS['workflow']
        params = dict(filters)

        if paginations:
            params.update(paginations)

        rsp = requests.get(url, params=params)

        response: RestfulResponseType = rsp.json()
        if response['code'] != 0:
            raise RuntimeError(response['message'])

        workflows: list[WorkflowType] = response['data'] # type: list[WorkflowType]
        return workflows

    def get_backends(self, alias: str = None):
        url = self.api + self.API_PREFIXS['backend']
        query = {"owner": self.owner}
        if alias:
            query['alias'] = alias

        rsp = requests.get(url, params=query)
        d = rsp.json()  # type: RestfulResponseType

        if d.get('code') != 0:
            raise RuntimeError(d.get("message", "未知错误"))
        backends = d.get('data')    # type: list[CromwellBackendType]
        if alias and backends:
            backends = [backends] 
        return backends

    def sync_backend(self, upload: bool = True):
        """同步本地和服务器上的backend配置
        
        upload (bool): 指定上传 或 下载配置
        """
        url = self.api + self.API_PREFIXS['backend']
        if upload:
            for alias, item in self.config.servers.items():
                item['alias'] = alias
                msg = f"{item['alias']}\t{item.get('backend', item['platform'])}\t{item['host']}\t"
                try:
                    self.add_update_backend(item)
                except Exception as e:
                    print(f"上传失败：{msg} {e}")
                else:
                    print(f"上传成功: {msg}")
            return

        rsp = requests.get(url, params={"owner": self.owner})
        rsp_data = rsp.json() # type: RestfulResponseType
        if rsp_data['code'] != 0:
            raise RuntimeError(f"查询服务器Cromwell Backend配置失败: {rsp_data['message']}")
        backends = rsp_data['data'] # type: list[CromwellBackendType]
        for backend in backends:
            self.config.add_cromwell_backend(backend['backend'], {k: v for k,v in backend.items() if k not in ['_id', 'name', 'owner']})
        print("下载配置成功")
        self.config.pp(self.config.servers)

    def add_update_backend(self, item: dict):
        """添加或更新backend

        Args:
            item (dict): 待添加或更新的backend

        根据 平台 + alias 检查是否存在。若存在则更新，否则新增

        若需要修改平台或alias，则需要先删除原backend在新增
        """
        url = self.api + self.API_PREFIXS['backend']
        data = dict(item)
        data['owner'] = self.owner
        if not data.get('backend') and data.get('platform'):
            data['backend'] = data['platform']
            del data['platform']
        rsp = requests.put(url, data=data)
        d = rsp.json()   # type: RestfulResponseType
        if d['code'] != 0:
            raise RuntimeError(d['message'])
        return d['message']

    def delete_backend(self, item: dict):
        if not item.get('backend') and item.get('platform'):
            item['backend'] = item['platform']
            del item['platform']

        name = ":".join([self.owner, item['backend'], item['alias']])
        url = self.api + self.API_PREFIXS['backend'] + name
        requests.delete(url)

    def validate_cromwell_id(self, cromwell_id: str, alias: str = None):
        backend = self.config.get_cromwell_backend(alias)

        # rsp = requests.post(f"{host}/api/workflows/v1", files=files)
        try:
            rsp = requests.get(f"{backend['host']}/api/workflows/v1/{cromwell_id}/status")
            d = rsp.json()
            # 成功时 d = {id, status}
            # 失败时 d = {status, message}
            if not d.get('id'):
                raise RuntimeError(f"Cromwell校验失败：{d.get('message')}")
        except Exception as e:
            raise RuntimeError(f"Cromwell 编号校验失败: {e}")
        return True