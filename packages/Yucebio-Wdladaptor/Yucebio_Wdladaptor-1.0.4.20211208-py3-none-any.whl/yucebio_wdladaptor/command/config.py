import sys
import click
from .base import AliasedGroup
from yucebio_wdladaptor.util.config import Config
from yucebio_wdladaptor.backend import SUPPORTTED_BACKENDS, create_adaptor, PLACEHOLDER_SIMG_PATH, PLACEHOLDER_GLOBAL_PATH, BaseAdaptor
from yucebio_wdladaptor.util.api import WDLAPI


@click.group('config', cls=AliasedGroup)
def cli():
    """查看或管理配置"""
    pass


@cli.command()
@click.option("--platform", "-p", type=click.Choice(list(SUPPORTTED_BACKENDS)), required=True, help="platform")
@click.option("--alias", "-a", help="配置别名，支持同一平台下的多个cromwell服务", default=None)
@click.option('--host', '-h', help="cromwell server 地址", required=True)
@click.option('--global_path', '-g', help=f"公共文件路径，用于自动替换json中的[{PLACEHOLDER_GLOBAL_PATH}]", type=str, required=True)
@click.option('--simg_path', '-s', help=f"singulartiy镜像路径，用于自动替换json中的[{PLACEHOLDER_SIMG_PATH}]", type=str, required=True)
@click.option('--runtimes', '-r', help=f"配置当前服务支持的自定义RUNTIME属性，多个属性之间使用逗号分隔", type=str)
def add_cromwell(**kw):
    """新增或更新更新Cromwell Server平台配置
    {host, global_path, simg_path, backend: platform}
    """
    config = Config()

    platform = kw['platform']
    if kw['runtimes']:
        kw['runtimes'] = kw['runtimes'].split(',')
    if kw['host']:
        kw['host'] = kw['host'].strip('/')
    cfg = {k: kw[k] for k in kw if kw[k]}
    cfg['backend'] = platform
    alias = kw['alias']
    if not kw['alias']:
        alias = platform

    pre_service = config.servers.get(alias, {})
    if cfg:
        config.add_server(alias, cfg)
    config.pp(config.servers)

    # 新增成功后，同步新增到API
    if not config.api:
        return

    api = WDLAPI()
    # 若platform和alias变更，则需要先删除
    if pre_service and pre_service.get("platform") != kw['platform']:
        api.delete_backend(pre_service)
    print("更新配置到API服务器：", api.add_update_backend(kw))

@cli.command()
def list_cromwell(**kw):
    """查看Cromwell Server平台配置"""
    config = Config()
    config.pp(config.servers)

@cli.command()
@click.option("--alias", "-a", help="配置别名", required=True)
def delete_cromwell(alias: str):
    """删除Cromwell Server平台配置"""
    config = Config()
    pre_service = config.servers.get(alias, {})
    if not alias:
        click.secho("删除出错，没有当前名称的配置项", fg='red', file=sys.stderr)
        return 

    config.del_server(alias)
    config.pp(config.servers)

    if not config.api:
        return

    api = WDLAPI()
    if pre_service:
        api.delete_backend(pre_service)

@cli.command()
# @click.option("--username", '-u', help="用户名", type=str)
# @click.password_option("--password", '-p', help="密码", required=False)
@click.argument('api', type=str)
def api_service(api):
    """配置适配器专用的API服务器地址

    使用适配器投递作业后, 适配器会自动将作业信息上传到API服务器, 由API服务器负责完成后续的作业同步等处理
    """
    config = Config()
    try:
        welcome_info = config.set_api_service(api)
    except Exception as e:
        click.secho("配置失败：" + str(e), fg='red')

    print("配置成功：", config.api)
    print(welcome_info)


@cli.command()
@click.option('--upload/--download', '-u/-d', is_flag=True, default=False, help="设置同步模式（上传或下载）", show_default=True)
def sync(upload: str):
    """主动同步配置

    1. 上传个人配置到gitlab
    2. 从gitlab下载个人配置
    """
    config = Config()
    if not upload:
        try:
            url = config.download_config()
            click.secho(f"download success from {url}", fg='green')
        except Exception as e:
            click.secho(f"下载配置异常: {e}", fg='red')
            raise e
    else:
        click.secho("upload config to gist", fg='yellow')
        url = config.upload_config()
        click.secho(f"upload success: {url}", fg='green')