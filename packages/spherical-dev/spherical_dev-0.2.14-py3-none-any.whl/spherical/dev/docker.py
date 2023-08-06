import functools
import inspect
import pathlib
from collections import Mapping

import docker
import invoke

from .invoke import ConfigurableTask
from .utils import flatten_options, named_args


DEFAULT_BASE = 'alpine:v3.14'


class DockerTask(ConfigurableTask):
    def task_module_config(self, ctx):
        module_config = dict(super().task_module_config(ctx))
        try:
            docker_id = docker.from_env().info()['ID']
            docker_config = module_config.get(docker_id, {})
            for task, config in docker_config.items():
                task_config = module_config.setdefault(task, {})
                for name, value in config.items():
                    # even if option exists in task config
                    # overload it with docker specific option by id
                    # see apt-cacher for usage example
                    task_config[name] = value
        except Exception:
            pass
        return module_config


task = functools.partial(invoke.task, klass=DockerTask)


def build_cmd(*args):
    return ' '.join(args)


def name(path=None):
    if path is None:
        frame = inspect.currentframe()
        while frame is not None:
            path = pathlib.Path(frame.f_code.co_filename).resolve()
            if path.name == 'tasks.py':
                break
            path = None
            frame = frame.f_back
        if path is None:
            raise RuntimeError('tasks path not found')
    return pathlib.Path(path).resolve().parent.name


@task
def kill(ctx, container=None):
    if not container:
        raise ValueError('please specify container to kill')
    if ctx.config['run']['dry']:
        ctx.run(f'docker stop {container}')
        ctx.run(f'docker rm {container}')
    else:
        engine = docker.from_env()
        containers = {x.name: x for x in engine.containers.list()}
        if container in containers:
            containers[container].stop()
            containers[container].remove()


@task
def install(
    ctx,
    image=name(),
    proxy=None,
    base=DEFAULT_BASE,
    network=None,
    args=None,
    context='.',
    file=None,
    platform=None,
):
    build_args = {
        'BASE_IMAGE': base,
        **(args if args is not None else {}),
    }
    if proxy is not None:
        build_args['http_proxy'] = proxy
        build_args['https_proxy'] = proxy
    build_args = named_args('--build-arg ', build_args)

    image, *tags = image.split(',')
    ctx.run(build_cmd(
        'docker',
        'buildx' if platform else '',
        'build',
        f'--platform {platform}' if platform else '',
        f'--network {network}' if network else '',
        f'-f {file}' if file else '',
        f'{build_args}',
        f'-t {image} {context}',
    ))
    for tag in tags:
        ctx.run(f'docker tag {image} {tag}')


@task
def run(
    ctx,
    volumes=[],
    container=None,
    image=name(),
    network=None,
    daemon='-d --restart unless-stopped',
    options=[],
    command=[],
    env='',
    labels=[],
    entrypoint=None,
):
    networks = None
    if isinstance(network, list):
        network, *networks = network
    if container is None:
        container = image
    env = named_args('-e ', env) if env else env

    if not isinstance(labels, Mapping):
        labels = {k: v for k, _, v in (x.partition('=') for x in labels)}

    kill(ctx, container=container)
    ctx.run(build_cmd(
        'docker run',
        daemon,
        ' '.join(options),
        f'--name {container}',
        f'--network {network}' if network else '',
        *(f'--volume {x}' for x in volumes),
        *((f'--entrypoint {entrypoint}',) if entrypoint is not None else ()),
        f'{env}',
        named_args('--label ', flatten_options(labels)),
        image,
        ' '.join(command),
    ), pty=True)

    if networks:
        for net in networks:
            ctx.run(f'docker network connect {net} {container}')


@task
def shell(
    ctx,
    container=name(),
    command='sh',
):
    ctx.run(build_cmd(
        f'docker exec -ti {container} {command}',
    ), pty=True)
