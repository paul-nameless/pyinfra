from pyinfra.modules import pacman

SUDO = True

pacman.packages(
    {'Install Vim and a plugin'},
    ['vim-fugitive', 'vim'],
    update=True,
)
