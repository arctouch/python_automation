from os import path
import argparse
import multiprocessing
import os
import shlex
import shutil
import subprocess
from os.path import join

from paver.setuputils import setup

# -n \'Checking form subimission validation\'
# ./features/Services.feature
def run_behave_test(device, task_id=0, is_web=False, tags=None):
    # Verifying if reports and logs folder exist
    if not path.exists('reports'):
        os.makedirs('reports')
    if not path.exists('logs'):
        os.makedirs('logs')
    folder = './reports'
    # Creating a folder to each device
    device_log_folder = join(folder, device)
    try:
        os.makedirs(device_log_folder)
    except OSError as e:
        print("Error: %s : %s" % (folder, e.strerror))
    formatter_args = f'--junit --junit-directory {device_log_folder}'
    my_env = os.environ.copy()
    my_env["TASK_ID"] = str(task_id)

    tag_expression = ''
    if tags is not None:
        tag_expression = make_tag_expression(tags)
    command = f'behave ./features -D device="{device}" {tag_expression} {formatter_args}'
    if is_web:
        command = f'{command} -D platform=web'

    print('Task {}: {}'.format(task_id, command))

    log_file = 'logs/{}.log'.format(device)
    with open(log_file, 'a+') as log:
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, env=my_env)

        while True:
            output = process.stdout.readline().decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            if output:
                log.write(output)
                log.flush()
                print('Task {} • {} • >> {}'.format(task_id, device, output.replace("\n", "")))

        rc = process.poll()
        log.write('Task {} • {} • >> Completed  OK  '.format(task_id, device))
        print('Task {} • {} • >> Completed  OK  '.format(task_id, device))

    return rc


def make_tag_expression(tags):
    tags_list = tags.split(',')
    tag_expression = ''

    for tag in tags_list:
        tag_expression += '--tags ' + tag + ' '

    return tag_expression


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--d', help='Example: $ runner.py --d deviceName1,deviceName2 | Insert the devices.', required=True)
    parser.add_argument('--web', action='store_true', help='Example: True | Add this option IF it`s web automation. The code will run mobile native automation as default.')
    parser.add_argument('--tag', help='Example: $ runner.py --d deviceName --tag android,web | Insert tags to run the code accordingly to the tags added on test scenarios. If you want to not run the code on a specific tag, please add \'~\' before the tag.')
    args = parser.parse_args()
    devices = args.d
    devices = devices.split(',')
    web = args.web
    tags = args.tag
    for i in range(len(devices)):
        p = multiprocessing.Process(target=run_behave_test, args=(devices[i], i, web, tags))
        p.start()


if __name__ == '__main__':
    run()
