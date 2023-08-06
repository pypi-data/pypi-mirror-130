import os
import sys
import click
from .base import AliasedGroup, show_error
from yucebio_wdladaptor.util.api import WDLAPI


@click.group('api', cls=AliasedGroup)
def cli():
    """通过适配器服务的形式管理Cromwell作业、Backend等
    """
    pass

@cli.command()
@click.option('--backend_name', '-b', help="Cromwell backend别名")
@click.option('--cromwell_id', '-j', help = "Cromwell作业编号")
@click.option('--prefix', '-p', help = "自定义分析任务编号")
@click.option('--file_type', '-t', help="指定导出类型。json或wdl", default="json")
def export_workflow(backend_name, cromwell_id, prefix, file_type):
    """导出已有作业的原始内容，如input.json
    """
    if prefix and cromwell_id:
        return show_error("只能使用一种编号")

    if not prefix and not cromwell_id:
        return show_error("至少指定一种编号")

    do_action('export_workflow', {"type": file_type}, backend_name=backend_name, primary_value=cromwell_id if cromwell_id else prefix)


@cli.command()
@click.option('--backend_name', '-b', help="Cromwell backend别名")
# @click.option('--cromwell_ids', '-j', help = "待关联作业的Cromwell编号", required=True, nargs=-1)
@click.argument('cromwell_ids', nargs=-1)
def link_job(backend_name, cromwell_ids):
    """关联一个已存在的作业
    
    CROMWELL_IDS: 一个或多个待关联的Crowmell作业编号
    """
    api = WDLAPI()
    for cromwell_id in cromwell_ids:

        # do_action('link', {"cromwell_id": cromwell_id}, backend_name=backend_name)
        try:
            api.validate_cromwell_id(cromwell_id, backend_name)
            msg = api.submit_action('link', {"cromwell_id": cromwell_id}, backend_name=backend_name)
        except Exception as e:
            click.secho(f"关联失败：{cromwell_id} {e}", fg='red', file=sys.stderr)
        else:
            click.secho(f"关联成功: {cromwell_id} {msg}", fg="green")

def do_action(action: str, data: dict, backend_name: str, primary_value: str = 'action', expect_response_type: str='json'):
    """基于Restful接口执行自定义操作

    当primary_value=='action'时，表示操作的是整个资源
    """
    api = WDLAPI()
    try:
        msg = api.submit_action(action, data, backend_name=backend_name, primary_value=primary_value, expect_response_type=expect_response_type)
        if expect_response_type != 'json':
            return msg
    except Exception as e:
        click.secho(f"操作失败：{e}", fg='red', file=sys.stderr)
    else:
        click.secho(f"操作成功: {msg}", fg="green")

@cli.command()
@click.option('--backend_name', '-b', help="按别名过滤", type=str, default=None)
def list_backends(backend_name):
    """获取服务器支持的所有Cromwell Backend

    按照 host backend owner alias 列出所有已存在的cromwell backends。
    """
    print("\t".join(["HOST", "Backend", "Owner", "Alias"]))
    api = WDLAPI()
    backends = api.get_backends(backend_name)
    for backend in backends:
        print("\t".join([backend.get(k, '-') for k in ['host', 'backend', 'owner', 'alias']]))


@cli.command()
@click.option('-u/-d', '--upload/--download', is_flag=True, default=True, help="同步本地与WDLAPI上的Cromwell配置信息")
def sync_backends(**kw):
    """将本地backend配置上传到服务器 或 从服务器下载backend配置"""
    api = WDLAPI()
    api.sync_backend(upload = kw['upload'])