import sys
import click
from .base import AliasedGroup
from yucebio_wdladaptor.util.config import Config
from yucebio_wdladaptor.util.api import WDLAPI
from yucebio_wdladaptor.backend_v2 import SUPPORTTED_BACKENDS, create_adaptor, PLACEHOLDER_SIMG_PATH, PLACEHOLDER_GLOBAL_PATH, BaseAdaptor


@click.group('adaptor', cls=AliasedGroup)
def cli():
    """WDL适配器 V2"""
    pass

def info(msg, file=sys.stderr, **secho_options):
    click.secho(msg, fg='red', file=file, **secho_options)

@cli.command()
@click.option('--backend_name', '-b', required=True, type=str, help="平台配置名称")
@click.argument('json', nargs=-1)
def submit(**kw):
    """提交通用流程到指定平台(适用于生产人员)

    JSON 一个或多个任意通用流程对应的JSON文件
    """
    api = WDLAPI()
    for jsonfile in kw["json"]:
        try:
            msg = api.submit(kw['backend_name'], jsonfile)
        except Exception as e:
            click.secho(f"任务信息上传失败：{e}，请手动将作业信息上传到服务器或联系开发人员", fg='red', file=sys.stderr)
        else:
            click.secho(f"上传成功: {msg}", fg="green")

@cli.command()
@click.option('--prefix', '-p', type=str, help="用户自定义的分析编号")
@click.option('--cromwell_id', '-c', type=str, help="Cromwell自动生成的编号")
@click.option("--backend_name", "-b", required=True, type=str, help="平台配置名称")
def restart(prefix, cromwell_id, backend_name):
    """重投作业。请至少提供prefix或cromwell_id参数(仅适用于生产人员)

    Tips: 使用非通用流程的研发人员请使用convert子命令投递或重新投递任务
    """
    if prefix and cromwell_id:
        return info("只能使用一种编号")

    if not prefix and not cromwell_id:
        return info("至少指定一种编号")

    api = WDLAPI()
    try:
        msg = api.submit_action('restart', {}, backend_name, prefix if prefix else cromwell_id)
    except Exception as e:
        info(e)
    else:
        click.secho(msg, fg="green")

@cli.command()
@click.option('--prefix', '-p', type=str, help="用户自定义的分析编号")
@click.option('--cromwell_id', '-c', type=str, help="Cromwell自动生成的编号")
@click.option("--backend_name", "-b", required=True, type=str, help="平台配置名称")
def abort(prefix, cromwell_id, backend_name):
    """根据cromwell_id或prefix终止作业

    Tips: 同一个prefix可能会存在多个作业, 此时会因找不到正确的作业而失败
    """
    if prefix and cromwell_id:
        return info("只能使用一种编号")

    if not prefix and not cromwell_id:
        return info("至少指定一种编号")

    api = WDLAPI()
    try:
        msg = api.submit_action('abort', {}, backend_name, prefix if prefix else cromwell_id)
    except Exception as e:
        info(e)
    else:
        click.secho(msg, fg="green")

@cli.command()
@click.option("--input", "-i", required=False, help="input json file")
@click.option("--backend_name", "-b", required=True, type=str, help="平台配置名称")
@click.option("--submit", "-s", is_flag=True, default=False, help="是否自动投递。（默认情况下会将适配后的内容保存到本地，由使用人员手动投递）")
@click.option('--runtimes', '-r', help=f"配置需要自动添加到task.runtime中的属性", type=str)
@click.argument("wdl")
def convert(**kw):
    """根据不同平台具有的基础设施转换通用WDL，并自动适配json和task。(适用于研发人员)
    """
    config = Config()

    backend = config.get_cromwell_backend(kw['backend_name'])
    if not backend:
        return info("平台配置无效，请选择其他平台或重新配置Backend")

    if not config.api:
        return info("未配置服务器地址")

    adaptor = create_adaptor(backend)
    adaptor.parse(wdl_path=kw['wdl'], input_path=kw['input'], runtimes=kw["runtimes"])

    adaptor.convert()

    if not kw['submit']:
        adaptor.generate_file(outdir='temp')
        return

    jobid = adaptor.submit()
    click.secho(f"submit success: {jobid}，准备将任务信息上传到到服务器", fg="green")

    # 若配置了API，则将任务发送到API服务器
    api = WDLAPI()
    try:
        msg = api.submit_action('link', {"cromwell_id": jobid}, backend_name=kw['backend_name'])
    except Exception as e:
        click.secho(f"任务信息上传失败：{e}，请手动将作业信息上传到服务器或联系开发人员", fg='red', file=sys.stderr)
    else:
        click.secho(f"上传成功: {msg}", fg="green")




@cli.command()
@click.option("--access_id", "-i", help="阿里云ACCESS KEY ID")
@click.option('--access_secrect', '-s', help="阿里云ACCESS KEY SECRECT")
def update_bcs_instance(access_id, access_secrect):
    """更新阿里云可用类型
    """
    import batchcompute, datetime
    bNeedUpdateAccess = True
    # adaptor = BaseAdaptor()
    config = Config()
    if not (access_id and access_secrect):
        # 从配置文件中获取
        # cfg = adaptor.config("bcs_access", {})
        cfg = config.get("bcs_access", {})
        if not cfg:
            click.secho("请提供ACCESS_KEY_ID和ACCESS_KEY_SECRECT", fg='yellow')
            return
        access_id, access_secrect = cfg.get("access_id", ""), cfg.get("access_secrect", "")
        bNeedUpdateAccess = True

    if not (access_id and access_secrect):
        return

    try:
        client = batchcompute.Client(batchcompute.CN_SHENZHEN, access_id, access_secrect)
        response = client.get_available_resource()
    except Exception as e:
        click.secho(f"Error: {e.code} 请检查ACCESS_KEY_ID[{repr(access_id)}]和ACCESS_KEY_SECRECT[{repr(access_secrect)}]是否正确", fg='red')
        return

    if bNeedUpdateAccess:
        config.set("bcs_access", {"access_id": access_id, "access_secrect": access_secrect})
    data = response.content
    data['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d")
    config.set("available_bcs_rescource", data)
    click.secho("阿里云可用实例类型更新完毕！")



if __name__ == "__main__":
    cli()
