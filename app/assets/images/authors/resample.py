from glob import glob
from os import system

for fnm in glob('new/*.png'):
    newfnm = fnm.split('/')[1].replace('.png', '.jpg')
    system('convert {} {}'.format(fnm, newfnm))

for fnm in glob('*.jpg'):
    # resize pictures to a resonable max area
    # imagemagick.org/Usage/resize/#pixel
    max_size = 240
    system('convert {f} -resize {ms}@ {f}'.format(f=fnm, ms=max_size**2))
