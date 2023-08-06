import click
import datetime
from click.types import DateTime

from .base import AliasedGroup
from yucebio_wdladaptor.util.monitor_v2 import Monitor

@click.group('monitor', cls=AliasedGroup)
def cli():
    """作业监控"""
    pass


@cli.command()
@click.option('--page', '-p', help="分页页码", type=int, default=1, show_default=True)
@click.option('--page_size', '-ps', help="每页查询的数据量", type=int, default=10, show_default=True)
@click.option('--backend_name', '-b', help="按Cromwell配置过滤")
@click.option('--prefix', help="按prefix（分析任务编号）模糊查询")
@click.option('--sample_ids', '-sa', help="按样本编号模糊查询")
@click.option('--status', '-s', help="按作业状态查询", type=click.Choice(['Submitted', 'Running', 'Aborting', 'Failed', 'Succeeded', 'Aborted']))
@click.option('--detail', '-d', is_flag=True, default=False, help="显示详细信息（错误信息和当前运行中的步骤）", show_default=True)
def ls(**kw):
    """查看本人提交的任务最新状态"""
    monitor = Monitor(backend_name=kw['backend_name'])
    show_detail = kw.pop('detail')
    monitor.list_jobs(kw, show_detail=bool(show_detail))

@cli.command()
@click.option('--backend_name', '-b', help="cromwell server 配置名称", required=True)
@click.option('--id', '-j', help="cromwell 作业编号")
@click.option('--name', '-n', help="cromwell 流程名称")
@click.option('--status', '-s', help="cromwell 作业状态", type=click.Choice(['Submitted', 'Running', 'Aborting', 'Failed', 'Succeeded', 'Aborted']))
@click.option('--start', '-st', help="cromwell 开始时间", type=DateTime())
@click.option('--submission', '-su', help="cromwell 提交时间", type=DateTime())
@click.option('--page', '-p', help="分页页码", type=int)
@click.option('--pageSize', '-ps', help="每页查询的数据量", type=int)
@click.option('--save', help="是否保存到API服务器", is_flag=True, default=False)
def query(**kw):
    """基于Cromwell API接口查询所有任务基本信息

    参考: https://cromwell.readthedocs.io/en/stable/api/RESTAPI/#workflowqueryparameter
    """
    server = kw.pop('backend_name')
    params = {k:v for k,v in kw.items() if v and k != 'save'}
    for k in ['start', 'submission']:
        if not kw[k]:
            continue
        t: datetime.datetime = kw[k]
        params[k] = t.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    if not params:
        ctx = click.get_current_context()
        click.secho('请至少指定一种参数', fg='red')
        print(ctx.get_help())
        return

    monitor = Monitor(backend_name=server)
    data = monitor.query(params, server)

    total, results = data['totalResultsCount'], data['results']
    click.secho(f"总数据量：{total}", fg="green")

    save = kw['save']
    for job in results:
        try:
            cromwell_job = monitor.get(job['id'], server)
        except Exception as e:
            click.secho(f"{job['id']}\t{server}\t获取metadata失败：{e}")
            continue
        cromwell_job.format()

        if save:
            monitor.save(cromwell_job)
