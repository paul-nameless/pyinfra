from pyinfra import host
from pyinfra.modules import apt, init, python

# Standalone example to show how to install Docker CE using
# https://docs.docker.com/install/linux/docker-ce/ubuntu/

# This script just shows how some pieces might fit together.
# Please see https://github.com/Fizzadar/pyinfra-docker
# for a more complete pyinfra docker installation.

SUDO = True


def check_docker_works(state, host):
    command = 'docker run hello-world'
    status, stdout, stderr = host.run_shell_command(state, command=command, sudo=SUDO)
    if not status or 'Hello from Docker!' not in stdout:
        raise Exception('`{}` did not work as expected'.format(command))


if host.fact.linux_name == 'Ubuntu':

    apt.packages(
        {'Ensure old docker packages are not present'},
        [
            'docker',
            'docker-engine',
            'docker.io',
            'containerd runc',
        ],
        present=False,
    )

    apt.packages(
        {'Ensure Docker CE prerequisites are present'},
        [
            'apt-transport-https',
            'ca-certificates',
            'curl',
            'gnupg-agent',
            'software-properties-common',
        ],
        update=True,
    )

    docker_key_exists = False
    stdout = host.fact.command('apt-key list')
    if 'Docker' in stdout:
        docker_key_exists = True

    if not docker_key_exists:
        apt.key(
            {'Add the Docker apt gpg key if we need to'},
            key='https://download.docker.com/linux/ubuntu/gpg',
        )

    linux_id = host.fact.linux_distribution['release_meta'].get('ID')
    code_name = host.fact.linux_distribution['release_meta'].get('DISTRIB_CODENAME')
    print(linux_id, code_name)
    apt.repo(
        {'Add the Docker CE apt repo'},
        (
            'deb [arch=amd64] https://download.docker.com/linux/'
            '{} '
            '{} stable'.format(linux_id, code_name)
        ),
        filename='docker-ce-stable',
    )

    apt.packages(
        {'Ensure Docker CE is installed'},
        [
            'docker-ce',
            'docker-ce-cli',
            'containerd.io',
        ],
        update=True,
    )

    init.service(
        {'Ensure docker service is running'},
        'docker',
        running=True,
        enabled=True,
    )

    python.call(check_docker_works)
