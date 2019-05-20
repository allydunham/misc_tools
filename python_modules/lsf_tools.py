#!/usr/bin/env python3
"""
Module containing tools for interacting and genrating jobs with the LSF job system
Only contains options for things I have needed to use in my work
"""

DEFAULT_LOGDIR = '/nfs/research1/beltrao/ally/logs'#
DEFAULT_QUEUE = 'research-rh74'

def bsub(command, stdout=None, stderr=None, ram=None, group=None,
         name=None, dep=None, cwd=None, gpu=0, gpu_exclusive=False,
         queue=None, project=None):
    """Generate LSF submission command string"""

    # Construct resource usage string
    rusage = {}
    if ram:
        rusage['mem'] = ram

    rusage_str = ', '.join([f'{key}={value}' for key, value in rusage.items()])

    # Construct gpu string
    if gpu == 1 and not gpu_exclusive:
        gpu = '-'
    elif gpu > 0:
        gpu = f'"num={gpu}{":j_exclusive=yes" if gpu_exclusive else ""}"'

    # Construct command
    command = ['bsub',
               f'-J "{name}"' if name else '',
               f'-g "{group}"' if group else '',
               f'-q "{queue}"' if queue else '',
               f'-P "{project}"' if project else '',
               f'-w "{dep}"' if dep else '',
               f'-gpu {gpu}' if gpu else '',
               f'-M {ram}' if ram else '',
               f'-R "rusage[{rusage_str}]"' if rusage else '',
               f'-o {stdout}' if stdout else '',
               f'-e {stderr}' if stderr else '',
               f'-cwd "{cwd}"' if cwd else '',
               f'"{command}"']

    command = [x for x in command if x]

    return ' '.join(command)

def easy_bsub(command, name, ram=None, gpu=0, logdir=DEFAULT_LOGDIR,
              group=None, dep=None, queue=DEFAULT_QUEUE, project=None,
              gpu_exclusive=False, cwd=None):
    """
    Quickly construct bsub commands with my usual formatting
    """
    if gpu and project is None:
        project = 'gpu'
    elif gpu and project != 'gpu':
        print('Warning: GPU requested but project is not gpu')

    if gpu and 'rh74' not in queue:
        print('Warning: GPU requested but selected queue might not support GPUs')

    return bsub(command, name=name, stdout=f'{logdir}/{name}.%J',
                stderr=f'{logdir}/{name}.%J.err', ram=ram, gpu=gpu,
                project=project, queue=queue, gpu_exclusive=gpu_exclusive,
                group=group, dep=dep, cwd=cwd)