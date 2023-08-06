"""获取作业状态
"""
import sys
import json
from typing import OrderedDict
import pymongo, pymongo.collection, requests
# from yucebio_config import Config
from yucebio_wdladaptor.util.config import Config
import click

config = Config(check_login=False)

class Monitor:

    def __init__(self) -> None:
        self.persistable = self.test_persist_able(_raise=False)
        self._coll = None

    @property
    def persist_config(self) -> dict:
        return config.get("persist", {})

    def test_persist_able(self, _raise = True):
        """检查是否支持持久化：若不支持"""
        try:
            self.get_collection()
        except Exception as e:
            if _raise or True:
                raise e
            return False
        return True

    def get_mongo_client(self) -> pymongo.MongoClient:
        if not self.persist_config and self.persist_config.get('uri'):
            raise RuntimeError("未配置数据库")

        uri = self.persist_config.get('uri')
        client = pymongo.MongoClient(host=uri)
        return client

    @property
    def owner(self):
        return config.get('owner', '')
    
    def get_collection(self) -> pymongo.collection.Collection:
        if not getattr(self, '_coll', None):
            self._coll = self.get_mongo_client().get_database(self.persist_config.get('dbname', 'yucebio_wdl')).get_collection(self.persist_config.get('collection_name', "wdl_metadata"))
        return self._coll

    def get_server_api(self, server_alias: str) -> str:
        server_config = config.servers.get(server_alias)
        if not server_config:
            raise RuntimeError(f"无法找到[{server_alias}]对应的配置")
        if  not server_config.get('host'):
            raise RuntimeError(f"[{server_alias}]对应的配置中缺少host配置项")
        return server_config['host']

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

    def query(self, params: dict, server_alias: str):
        """基于Cromwell API接口查询数据，Refer to https://cromwell.readthedocs.io/en/stable/api/RESTAPI/#workflowqueryparameter
        """
        api = self.get_server_api(server_alias)
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
        if not self.persistable:
            return

        coll = self.get_collection()
        cromwell_job.get_metadata()     # 再次处理下metadata

        item = {
            "id": cromwell_job.cromwell_id,
            "host": cromwell_job.host,
            "server_alias": cromwell_job.server_alias,
            "owner": cromwell_job.owner,
            "samples": cromwell_job.samples,
            "prefix": cromwell_job.prefix
        }
        # record = coll.find_one({"id": item['id']})
        
        # calls的key里面有不符合格式的字段，需要转换下
        metadata = cromwell_job.metadata
        self.encode_metadata(metadata)
        item.update(metadata)

        coll.find_one_and_replace({"id": item['id']}, item, upsert=True)


    def abort(self, jobid: str, server_alias: str):
        api = self.get_server_api(server_alias)
        url = f"{api}/api/workflows/v1/{jobid}/abort"
        try:
            rsp = requests.post(url)
            if not rsp.ok:
                raise RuntimeError(rsp.reason)
            return rsp.json()
        except Exception as e:
            raise e

    def list_jobs(self, params: dict={}):
        """查看本人所有任务
        """
        # 1. 检测是否配置了持久化数据库
        try:
            coll = self.get_collection()
        except Exception:
            return self.list_local_jobs()

        # 将本地任务更新到数据库
        self.merge_local_jobs(coll)

        page = params.get('page', 1)
        pageSize = params.get('pagesize', 10)
        skip = (page - 1) * pageSize
        if skip <= 0:
            skip = 0

        # 查询本人所有任务
        cursor = coll.find({"owner": self.owner}, sort=[("id", pymongo.DESCENDING)]).limit(pageSize).skip(skip)
        click.secho(f"总数据量： {cursor.count()}", fg="green")
        for record in cursor:
            cromwell_id, host, server = record['id'], record['host'], record['server_alias']
            cromwell_job = CromwellJob(cromwell_id, server, host=host)
            # 判断是否需要获取最新数据
            if record.get('status') not in ['Succeeded', 'Failed', 'Aborted']:
                cromwell_job.get_metadata()
                # calls的key里面有不符合格式的字段，需要转换下
                metadata = cromwell_job.metadata
                self.encode_metadata(metadata)
                coll.update_one({"_id": record['_id']}, {"$set": metadata})
            else:
                self.decode_metadata(record)
                cromwell_job.parse_metadata(record)
            cromwell_job.format()

    def encode_metadata(self, metadata: dict):
        """cromwell metadata数据中存在不符合mongo数据格式的嵌套字典，在存入前需要对字段做下处理"""
        for k, d in zip(['inputs', 'outputs', 'calls'], [{}, {}, []]):
            metadata[k] = json.dumps(metadata.get(k, d))
    def decode_metadata(self, metadata: dict):
        for k, d in zip(['inputs', 'outputs', 'calls'], ['{}', '{}', '[]']):
            metadata[k] = json.loads(metadata.get(k, d))

    def merge_local_jobs(self, coll: pymongo.collection.Collection):
        workflows = config.get('workflows', [])
        if not isinstance(workflows, list):
            return

        invalid_workflows = []
        for job in workflows:
            cromwell_id, server = job['cromwell_id'], job['server']
            query = {
                "id": job['cromwell_id'],
                # "server_alias": job['server'],
                "host": self.get_server_api(job['server'])
            }

            record = coll.find_one(query)
            # 检查是否一致
            if record:
                if record.get('owner') != self.owner:
                    click.secho(f"任务所属人不一致！任务编号【{cromwell_id}】当前所属人为[{record['owner']}]，与您【{self.owner}】不一致", fg='red')
                    invalid_workflows.append(job)
                continue

            # 插入数据到服务器
            new_job = dict(query)
            new_job.update({
                "owner": self.owner,
                "server_alias": server
            })
            coll.insert_one(new_job)
        config.set("workflows", invalid_workflows)


    def list_local_jobs(self):
        """查看本地记录的所有任务"""
        workflows = config.get('workflows', [])
        if not isinstance(workflows, list):
            return

        for job in workflows:
            cromwell_id, server = job['cromwell_id'], job['server']
            try:
                cromwell_job = self.get(cromwell_id, server)
            except Exception as e:
                click.secho(f"{cromwell_id}\t{server}\t获取metadata失败：{e}")
                continue
            cromwell_job.format()

    def get_local_job(self, filter: dict) -> "CromwellJob":
        coll = self.get_collection()

        record = coll.find_one(filter)  # type: dict
        if not record:
            return None

        # '_id', 'id', 'host', 'server_alias', 'owner', 'samples', 'prefix', 'workflowName', 
        # 'workflowProcessingEvents', 'actualWorkflowLanguageVersion', 'submittedFiles', 'calls', 'outputs', 
        # 'actualWorkflowLanguage', 'inputs', 'labels', 'submission', 'status', 'end', 'start'
        cromwell_job = CromwellJob(record['id'], record['server_alias'], host=record['host'])
        self.decode_metadata(record)
        cromwell_job.parse_metadata(record)

        return cromwell_job

    def get_job(self, prefix: str = None, server: str = None, cromwell_id: str = None):
        if prefix:
            job = self.get_local_job({"prefix": prefix})
        elif cromwell_id:
            job = self.get_local_job({"id": cromwell_id})
        else:
            raise RuntimeError("prefix或cromwell_id必须提供一种")

        if not job:
            if  not all([cromwell_id, server]):
                raise RuntimeError("必须同时指定Cromwell作业编号和服务器")
            job = CromwellJob(cromwell_id, server)
            job.get_metadata()

        return job


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