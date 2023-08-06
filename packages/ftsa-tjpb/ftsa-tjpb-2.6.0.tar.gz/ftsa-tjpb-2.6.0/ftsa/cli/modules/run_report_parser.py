import os
import socket
import docker
import platform
from datetime import datetime
from ftsa.cli.utils import execute
from ftsa.cli.utils.files import delete_path, delete_file, is_project_ftsa, get_project_properties
from ftsa.cli.modules.properties import IMAGE_NAME, IMAGE_VERSION


RESULTS_DIRECTORIES = [
    'results',
    'output',
    'pabot_results',
    'report',
    'dist',
    'videos'
]

FILES = [
    '.pabotsuitenames',
    'log.html',
    'report.html',
    'output.xml'
]


def add_tags(args, tipo):
    if hasattr(args, tipo) and getattr(args, tipo) is not None:
        return ' '.join(['--' + tipo + ' ' + i for i in getattr(args, tipo)])
    return ''


def docker_report(args):
    is_project_ftsa()
    clear(args)
    include = add_tags(args, 'include')
    exclude = add_tags(args, 'exclude')
    docker_client = docker.from_env()

    # Setting no-docker execution option
    if hasattr(args, 'nodocker') and getattr(args, 'nodocker'):
        os.environ['NO_DOCKER_EXECUTION'] = 'nodocker'
        report(args)
    else:
        os.environ['NO_DOCKER_EXECUTION'] = 'dockerallowed'
        if hasattr(args, 'pull') and getattr(args, 'pull'):
            os.system(f'docker pull {IMAGE_NAME}:{IMAGE_VERSION}')
        else:
            os.system(f'docker build -t {IMAGE_NAME}:{IMAGE_VERSION} ./')

        # Use NET param OR, if none, [timestamp]_grid will be set
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        network_name = f'{now}_grid'
        if hasattr(args, 'net') and getattr(args, 'net') is not None:
            network_name = getattr(args, 'net')
        os.system(f'docker network create {network_name}')

        # Use CONTAINER param OR, if none, [network_name]_execution_robot
        user_exec_container = f'{network_name}_execution_robot'
        if hasattr(args, 'container') and getattr(args, 'container') is not None:
            user_exec_container = getattr(args, 'container')

        # Use DOCKERHOST param OR, if none, use current machine IP
        host = socket.gethostbyname(socket.gethostname())
        if hasattr(args, 'dockerhost') and getattr(args, 'dockerhost') is not None:
            host = getattr(args, 'dockerhost')

        # Creating path to save video files
        project_cwd = os.getcwd()
        videos_path = os.path.join(project_cwd, 'videos')
        if not os.path.isdir(videos_path):
            os.makedirs(videos_path)
        # Insert quotation marks if Windows dir
        print(f'Platform detected: {platform.system()}')
        if platform.system() == 'Windows':
            project_cwd = f'"{project_cwd}"'

        # Initializing volume to save video files
        video_recording_volume_name = 'video_recording_volume'
        videos_recorded_container = 'videos_recorded_container'
        try:
            videos_recorded = docker_client.containers.get(videos_recorded_container)
            videos_recorded.logs()
            videos_recorded.stop()
            videos_recorded.remove()
            print('Existing (old) videos recorded container removed.')
        except BaseException:
            print(f'Videos recorder container does not exist.')
        try:
            volume = docker_client.volumes.get(video_recording_volume_name)
            volume.remove()
            print('Existing (old) video recording volume removed.')
        except BaseException:
            print(f'Video recording volume does not exist.')
        cmd = f'docker volume create {video_recording_volume_name}'
        execute(cmd, 5)
        print(f'{video_recording_volume_name} volume created to save test executions.')

        # Initializing User Execution Independent container
        cmd = f'docker run --name {user_exec_container} --net {network_name} ' \
              f'-v /var/run/docker.sock:/var/run/docker.sock:rw ' \
              f'-v {project_cwd}:/opt/robotframework/tests:rw ' \
              f'-e SELENIUM_EXEC_HOST={host} ' \
              f'-e SELENIUM_CONTAINER_NAME={now}_selenium ' \
              f'-e VIDEOS_RECORDER_CONTAINER_NAME={now}_videos ' \
              f'-e USER_NETWORK_NAME={network_name} ' \
              f'-e USER_EXEC_CONTAINER_NAME={user_exec_container} ' \
              f'-e VOLUME_VIDEO_RECORDING_NAME={video_recording_volume_name} ' \
              f'{IMAGE_NAME}:{IMAGE_VERSION} ' \
              f'/bin/bash -c "ftsa report {include}{exclude}"'
        execute(cmd, 5)

        # os.system(f'docker stop {user_exec_container} && docker rm {user_exec_container}')
        # Finalize securely independent execution container
        try:
            exec_container = docker_client.containers.get(user_exec_container)
            exec_container.logs()
            exec_container.stop()
            exec_container.remove()
            print(f'{user_exec_container} container stopped and removed.')
        except BaseException:
            print(f'There is no {user_exec_container} container available OR already stopped and removed.')

        # os.system(f'docker network rm {network_name}')
        # Finalize securely grid network
        try:
            network = docker_client.networks.get(network_name)
            network.remove()
            print(f'{network} network removed.')
        except BaseException:
            print(f'There is no {network_name} network available OR already removed.')

        # Copy video files recorded to project videos path and exclude volume
        # os.system(f'docker volume rm video_recording_volume')
        try:
            cmd = f'docker run -it -d --name {videos_recorded_container} ' \
                  f'-v {video_recording_volume_name}:/videos fedora '
            execute(cmd, 5)
            videos_recorded = docker_client.containers.get(videos_recorded_container)
            videos_recorded.logs()
            cmd = f'docker cp {videos_recorded.id}:/videos {project_cwd}'
            print(f'Saving videos recorded to "{videos_path}" project path directory.')
            execute(cmd, 5)
            videos_recorded.stop()
            videos_recorded.remove()
            print(f'{videos_recorded_container} container removed.')
            volume = docker_client.volumes.get(video_recording_volume_name)
            volume.remove()
            execute('docker volume prune -f', 5)
            print(f'{video_recording_volume_name} volume removed.')
        except BaseException:
            print(f'There is no videos recorded available OR already removed.')


def report(args):
    is_project_ftsa()
    clear(args)
    include = add_tags(args, 'include')
    exclude = add_tags(args, 'exclude')

    # Setting no-docker execution option
    if hasattr(args, 'nodocker') and getattr(args, 'nodocker'):
        os.environ['NO_DOCKER_EXECUTION'] = 'nodocker'
    else:
        os.environ['NO_DOCKER_EXECUTION'] = 'dockerallowed'

    parallel = 1
    if hasattr(args, 'parallel') and getattr(args, 'parallel') is not None and int(getattr(args, 'parallel')) > 1:
        parallel = int(args.parallel)
    project = get_project_properties()
    try:
        quantity = project.get('prop', 'PARALLEL')
        if quantity is not None and int(quantity) > 1:
            parallel = int(project.get('prop', 'PARALLEL'))
            print(f'A propriedade PARALLEL foi definida no arquivo de propriedades: {parallel}')
    finally:
        print('A propriedade PARALLEL não existe no arquivo de propriedades do projeto')

    options = f'--verbose --testlevelsplit'
    if hasattr(args, 'allure') and getattr(args, 'allure') is not None and getattr(args, 'allure'):
        os.system(f'pabot {options} --processes {parallel} --listener allure_robotframework '
                  f'--outputdir ./output {include}{exclude} --timestampoutputs ./features')
        os.system(f'allure serve ./output/allure')
    elif parallel == 1:
        os.system(f'robot -L TRACE -d ./output {include}{exclude} --timestampoutputs ./features')
    else:
        os.system(f'pabot {options} --processes {parallel} --outputdir ./output {include}{exclude} --timestampoutputs ./features')


def clear(args):
    is_project_ftsa()
    for directory in RESULTS_DIRECTORIES:
        try:
            delete_path(os.path.join(os.getcwd(), directory))
        except BaseException:
            print(f'Path/Directory "{directory}" can NOT be deleted...')
    for file in FILES:
        try:
            delete_file(os.path.join(os.getcwd(), file))
        except BaseException:
            print(f'File "{file}" can NOT be deleted...')


def run(args):
    report(args)
    clear(args)
