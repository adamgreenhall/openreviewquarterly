import os
from glob import glob
from bs4 import BeautifulSoup
from ipdb import set_trace
from codecs import open


junk_styles = [
    'height:11pt',
    'line-height:1.0',
    'line-height:1.1500000000000001',
    'color:#000000',
    'color:#222222',
    'margin-bottom:0',
    'margin-top:0',
    'margin-left:0',
    'margin-right:0',
    'padding-left:0',
    'padding-right:0',
    'padding-top:0',
    'padding-bottom:0',
    'direction:ltr',
    'font-size:11pt',
    'font-size:12pt',
    'font-size:10pt',
    'font-family:"Arial"',
    'font-family:"Calibri"',
    'font-family:"Cambria"',
    'font-family:"Times New Roman"',
    'font-family:"Segoe UI"',
    'padding:0',
    'margin:0',
    'color:inherit',
    'text-decoration:inherit',
    'background-color:#ffffff',
    'color:#1155cc;text-decoration:underline', #default link styling
]

# flatten the directory structure
for fnm in glob('*/*.html'):
    if not 'cleaned/' in fnm:
        os.system('mv "{}" "{}"'.format(fnm, fnm.split('/')[1]))
for fnm in glob('*/'):
    os.system('rm -r "{}"'.format(fnm))
    
# clean each html file
def attrOK(key, val):
     if key == 'style': return False
     return True
def tagOK(tag):
    if tag.name == 'sup' or ('href' in tag.attrs and 'cmnt_ref' in tag.attrs['href']):
        return False
    return True
def clean_style(key, val):
    if key != 'style': return val
    for st in junk_styles:
        val = val.replace(st, '')
    return val
    
os.system('mkdir -p cleaned')
for fnm in glob('*.html'):
    with open(fnm, 'r') as f: 
        body = BeautifulSoup(f).body
    
    body.attrs = {}
    for tag in body.findAll(): 
        tag.attrs = {key: clean_style(key, val) for key, val in tag.attrs.iteritems()}
        if not tagOK(tag):
            tag.extract()
            
    # remove the comments
    for div in body.findAll('div', {'style': 'margin:5px;border:1px solid black'}):
        div.extract()
    
    with open('cleaned/{}'.format(fnm), 'w+', encoding='utf-8') as f:
        out = unicode(
            ''.join([str(tag) for tag in body.contents]),
            encoding='utf-8')
        header = "" #"<meta charset='UTF-8'>"
        f.write(header+out)