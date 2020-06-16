from pyinfra import host
from pyinfra.modules import dnf

SUDO = True

# Note: This "if" below is not really required.
# For instance, if you run this deploy on an
# Ubuntu instance (which does not use dnf)
# the dnf.packages() will simply be skipped
if host.fact.linux_name in ['CentOS', 'RedHat']:

    dnf.packages(
        {'Install some packages'},
        ['vim-enhanced', 'vim', 'wget'],
        update=True,
    )

linux_id = host.fact.linux_distribution['release_meta'].get('ID')
print(linux_id)

if host.fact.linux_name == 'CentOS':
    dnf.key(
        {'Add the Docker CentOS gpg key'},
        'https://download.docker.com/linux/{}/gpg'.format(linux_id),
    )

dnf.rpm(
    {'Ensure an rpm is not installed'},
    'snappy',
    present=False,
)

if host.fact.linux_name in ['CentOS', 'RedHat']:

    packages = host.fact.rpm_packages
    epel_installed = False
    for p in packages.keys():
        if p.startswith('epel-release'):
            epel_installed = True

    if not epel_installed:
        dnf.rpm(
            {'Install EPEL rpm to enable EPEL repo'},
            'https://dl.fedoraproject.org/pub/epel/epel-release-latest-'
            '{{  host.fact.linux_distribution.major }}.noarch.rpm',
        )

    dnf.packages(
        {'Install Zabbix and htop'},
        ['zabbix', 'htop'],
        update=True,
    )
