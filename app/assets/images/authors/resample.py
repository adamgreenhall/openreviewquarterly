from glob import glob
from os import system

for fnm in glob('new/*.png'):
    newfnm = fnm.split('/')[1].replace('.png', '.jpg')
    system('convert {} {}'.format(fnm, newfnm))
