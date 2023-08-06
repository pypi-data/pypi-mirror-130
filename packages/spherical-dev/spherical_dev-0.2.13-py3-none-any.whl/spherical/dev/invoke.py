import functools
import inspect

import invoke.executor
import invoke.main


class Executor(invoke.executor.Executor):
    def normalize(self, tasks):
        calls = super().normalize(tasks)
        for call, task in zip(calls, tasks):
            call._task = task
        return calls


config = getattr(invoke.main.program, 'config', None)
if config is not None:
    executor_class = f'{Executor.__module__}.{Executor.__name__}'
    config['tasks']['executor_class'] = executor_class


class ConfigurableTask(invoke.Task):
    def __call__(self, *args, **kwargs):
        kwargs = dict(kwargs)
        frame = inspect.currentframe()
        call = frame.f_back.f_locals.get('call', None)

        if call is not None:
            task = getattr(call, '_task', None)
            if task is not None:
                task_arguments = task.args.values()
            else:
                task_arguments = call.task.get_arguments()
        else:
            task_arguments = self.get_arguments()

        ctx, *_ = args
        config = self.get_config(ctx)

        def strip(value):
            return value.rstrip() if isinstance(value, str) else value

        kwargs.update({
            arg.name: strip(config[arg.name])
            for arg in task_arguments
            if (
                arg.name in config
                and kwargs.get(arg.name, arg.default) == arg.default
                and not arg.got_value
            )
        })

        return super().__call__(*args, **kwargs)

    def task_module_config(self, ctx):
        config = ctx.config
        for part in self.body.__module__.split('.'):
            config = config.get(part)
            if config is None:
                break
        return {} if config is None else config

    def get_config(self, ctx):
        return self.task_module_config(ctx).get(self.name, {})


task = functools.partial(invoke.task, klass=ConfigurableTask)
