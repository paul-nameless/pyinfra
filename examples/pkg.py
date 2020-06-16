from pyinfra import host
from pyinfra.modules import pkg

SUDO = True

if host.fact.os == 'OpenBSD':

    pkg.packages(
        {'Install Vim and Vim Addon Manager'},
        ['vim-addon-manager', 'vim'],
    )
