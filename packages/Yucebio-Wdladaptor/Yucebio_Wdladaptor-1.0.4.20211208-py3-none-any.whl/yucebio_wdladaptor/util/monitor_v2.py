"""获取作业状态
"""
import sys
from typing import OrderedDict
import requests
from yucebio_wdladaptor.util.config import Config
from yucebio_wdladaptor.util.api import WDLAPI
import click
from . import types

config = Config(check_login=False)

class Monitor:

    def __init__(self, backend_name: str = None) -> None:
        self.api = WDLAPI()
        self.backend_config : types.CromwellBackendType = None
        if backend_name:
            self.init_backend_config(backend_name)

    def init_backend_config(self, backend_name: str):
        if self.backend_config and self.backend_config["alias"] == backend_name:
            return

        self.backend_config = config.get_cromwell_backend(backend_name)

    @property
    def owner(self):
        return config.get('owner', '')

    def get(self, jobid: str, server_alias: str, auto_update: bool = True):
        """从cromwell api中获取作业最新状态

        Args:
            jobid (str): cromwell 作业id
            server_alias (str): cromwell server地址
            auto_update (bool): 检测到任务完成时，是否自动更新到数据库
        """
        cromwell_job = CromwellJob(jobid, server_alias)
        cromwell_job.get_metadata()
        return cromwell_job

    def query(self, params: dict, backend_name: str):
        """基于Cromwell API接口查询数据，Refer to https://cromwell.readthedocs.io/en/stable/api/RESTAPI/#workflowqueryparameter
        """
        api = config.get_cromwell_backend(backend_name)["host"]
        url = f"{api}/api/workflows/v1/query"
        try:
            rsp = requests.get(url, params=params)
            if not rsp.ok:
                print(url, params)
                raise RuntimeError(rsp.reason)
            return rsp.json()
        except Exception as e:
            raise e

    def save(self, cromwell_job: "CromwellJob"):
        # if not self.persistable:
        #     return

        # coll = self.get_collection()
        # cromwell_job.get_metadata()     # 再次处理下metadata

        # item = {
        #     "id": cromwell_job.cromwell_id,
        #     "host": cromwell_job.host,
        #     "server_alias": cromwell_job.server_alias,
        #     "owner": cromwell_job.owner,
        #     "samples": cromwell_job.samples,
        #     "prefix": cromwell_job.prefix
        # }
        # # record = coll.find_one({"id": item['id']})
        
        # # calls的key里面有不符合格式的字段，需要转换下
        # metadata = cromwell_job.metadata
        # self.encode_metadata(metadata)
        # item.update(metadata)

        # coll.find_one_and_replace({"id": item['id']}, item, upsert=True)
        pass

    def list_jobs(self, params: dict={}, show_detail: bool = False):
        """查看本人所有任务
        """
        page = params.get('page', 1)
        pageSize = params.get('page_size', 10)
        skip = (page - 1) * pageSize
        if skip <= 0:
            skip = 0

        api_params = {k:v for k,v in params.items() if k not in ['page', 'page_size', 'backend_name']}
        api_params['owner'] = self.owner
        if params.get('backend_name'):
            self.init_backend_config(params['backend_name'])
            backend = self.backend_config.get('platform', self.backend_config.get('backend'))

            api_params['backend.backend'] = backend

        workflows = self.api.get_workflows(api_params, paginations={"offset": skip, "limit": pageSize})
        if not workflows:
            return

        # 打印表头
        self.format_api_workflow_header()
        for job in workflows:
            self.format_api_workflow(job, show_detail=show_detail)

    def format_api_workflow_header(self):
        """打印表头
        """
        header = {
            "status": "状态",                   # Succeeded
            "prefix": "Prefix/分析项目编号",    # 20211116.ClinicRapid.2103062.MT1011.104406
            "sample_ids": "样本编号",           # DN2003922SLZDA26
            "workflow_name": "流程名称",
            "url": "Cromwell链接"
        }
        msg = '{status:10s}\t{prefix:40s}\t{sample_ids:32s}\t{workflow_name:15s}\t{url}'.format(**header)
        print(msg)

    def format_api_workflow(self, workflow: types.WorkflowType, show_detail: bool = False):
        backend_host = workflow["backend"]["host"]
        url = "-"
        if workflow.get('cromwell_id'):
            url = f"{backend_host}/api/workflows/v1/{workflow['cromwell_id']}/metadata"
        msg = f'{workflow["status"]:10s}\t{workflow.get("prefix", "-"):40s}\t{workflow.get("sample_ids", "-"):32s}\t{workflow.get("workflow_name", "-"):15s}\t{url}'

        if workflow["status"] == 'Running' and show_detail:
            for running_task in workflow.get("running_tasks", []):
                msg += click.style(f"\nRUNNING:\t{running_task}", fg="yellow")
        print(msg)

        if show_detail:
            for r in workflow.get("failures", []):
                print(click.style(f"\nFAIL_REASON:\t{r}", fg="red"), file=sys.stderr)

class CromwellJob:
    def __init__(self, cromwell_id: str, server_alias: str, host: str=None) -> None:
        self.cromwell_id = cromwell_id
        self.server_alias = server_alias
        self.host = host            # 某些情况下需要直接提供host地址
        self.api = self._api()
        self.metadata = {}
        self.call_details = []

        # 需要从inputs中提取的额外内容
        self.owner = ""
        self.prefix = ""
        self.samples = ""

    def _api(self):
        if not self.host:
            server_config = config.servers.get(self.server_alias)
            if not server_config:
                raise RuntimeError(f"无法找到[{self.server_alias}]对应的配置")
            if  not server_config.get('host'):
                raise RuntimeError(f"[{self.server_alias}]对应的配置中缺少host配置项")
            self.host = server_config['host']
        return self.host

    def get_metadata(self):
        """从cromwell api中获取作业最新状态
        """
        if self.metadata:
            return

        url = f"{self.api}/api/workflows/v1/{self.cromwell_id}/metadata"
        rsp = requests.get(url)
        if not rsp.ok:
            raise RuntimeError(f"{url}\t{rsp.reason}")

        metadata: dict = rsp.json()
        self.parse_metadata(metadata)

    def parse_metadata(self, metadata: dict):
        """解析metadata数据
        """
        self.metadata = metadata
        if not self.metadata:
            return
        self.status = self.metadata.get('status')
        for k in ["workflowName", "id", "status", "submission", "start", "end"]:
            self.__dict__[k] = self.metadata.get(k, "")

        # 解析calls
        calls = self.metadata.get('calls')
        if isinstance(calls, dict):
            for task_name, task_items in calls.items():
                idx = -1
                for task_item in task_items:
                    idx += 1
                    info = {
                        k: task_item.get(k, '-') for k in [
                            "executionStatus", "jobId", "backend", "start", "end", "callRoot",
                        ]
                    }
                    failures = task_item.get('failures')
                    if failures:
                        failures = self.parse_failures(failures)
                    self.call_details.append((task_name, idx, info, failures))

        self.parse_inputs()

    def parse_inputs(self):
        """解析inputs，提取一些必要信息"""
        inputs = self.metadata.get('inputs', {})
        if inputs:
            self.prefix = inputs.get('prefix', 'NA')

            tumor_id = inputs.get('tumor_id', None)
            normal_id = inputs.get('normal_id', None)
            rna_id = inputs.get('rna_id', None)
            sample = "-VS-".join([v for v in [tumor_id, normal_id] if v])
            sample = ",".join([v for v in [sample, rna_id] if v])
            self.samples = sample

            self.owner = inputs.get('owner', "")

    def parse_failures(self, failures: list):
        reasons = []
        for failure in failures:
            casedBy = failure.get('causedBy')
            if casedBy:
                reasons += self.parse_failures(failure['causedBy'])
            else:
                if failure.get('message'):
                    reasons.append(failure['message'])

        return reasons

    def format(self):
        key_lables = OrderedDict([
            ("workflowName", "流程名称"),
            ("id", "Workflow Id"),
            ("status", "状态"),
            ("submission", "提交时间"),
            ("start", "开始时间"),
            ("end", "结束时间"),
            # ("prefix", "分析项目号"),
            # ("samples", "样本")
        ])
        basic_infos = {k: self.metadata.get(k, "-") for k in key_lables}


        url = f"{self.api}/api/workflows/v1/{self.cromwell_id}/metadata"
        basic_infos["id"] = url
        msg = f"{basic_infos['status']}\t{self.prefix:15s}\t{self.samples:20s}\t{basic_infos['workflowName']:15s}\t{url}\t{basic_infos['submission']}"

        if self.status == 'Running':
            for running_task in self.current_running_tasks():
                msg += click.style(f"\nRUNNING:\t{running_task}", fg="yellow")
        print(msg)

        for r in self.fail_reason():
            print(click.style(f"\nFAIL_REASON:\t{r}", fg="red"), file=sys.stderr)

    def current_running_tasks(self):
        tasks = []
        for call in self.call_details:
            task_name, idx, info, failures = call
            if info.get('executionStatus') == 'Running':
                tasks.append(f"{task_name}[{idx}]\t{info['jobId']}\t{info['start']}")
            
        return tasks

    def fail_reason(self):
        if not self.call_details:
            # 直接从顶级的failures中提取错误信息
            return self.parse_failures(self.metadata.get('failures', []))
        reasons = []
        for call in self.call_details:
            task_name, idx, info, failures = call
            if not failures:
                continue
            reasons += [f"{task_name}[{idx}]\t{f}" for f in failures]
        return reasons