import os
from glob import glob
from bs4 import BeautifulSoup
from codecs import open


junk_styles = [
    'height:11pt',
    'line-height:1.0',
    'line-height:1.1500000000000001',
    'line-height:1.428571',
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
    'padding-bottom:10pt',
    'direction:ltr',
    'font-size:9pt',
    'font-size:10pt',
    'font-size:11pt',
    'font-size:12pt',
    'font-family:"Arial"',
    'font-family:"Calibri"',
    'font-family:"Cambria"',
    'font-family:"Times New Roman"',
    'font-family:"Segoe UI"',
    'padding:0',
    'margin:0',
    'color:inherit',
    'text-decoration:inherit',
    'text-indent:36pt',
    'background-color:#ffffff',
    'color:#1155cc;text-decoration:underline', #default link styling
]

# flatten the directory structure

# clean each html file
def attrOK(key, val):
     if key == 'style': return False
     return True
def tagOK(tag):
    if tag.name == 'sup' or \
        ('href' in tag.attrs and 'cmnt_ref' in tag.attrs['href']):
        return False
    return True

def is_comment_ref(tag):
    return tag.attrs.get('href', '').startswith('#cmnt') and \
        tag.attrs.get('name', '').startswith('cmnt_ref')

def is_comment_body(tag):
    return tag.attrs.get('href', '').startswith('#cmnt_ref') and \
        tag.attrs.get('name', '').startswith('cmnt')

def clean_style(key, val):
    if key != 'style': return val
    for st in junk_styles:
        val = val.replace(st + ';', '')
        val = val.replace(st, '')
    return val
    
os.system('mkdir -p cleaned')
for fnm in glob('*/*/*.html'):
    if fnm.startswith('old'): continue
    with open(fnm, 'r') as f: 
        body = BeautifulSoup(f).body
    
    body.attrs = {}
    for tag in body.findAll(): 
        tag.attrs = {key: clean_style(key, val) for key, val in tag.attrs.iteritems()}
        if is_comment_ref(tag):
            # extract the super tag around the footnote link
            tag.parent.extract()
        elif is_comment_body(tag):
            # extract the paragraph tag around the footnote body
            tag.parent.extract()
            
    # remove the comments
    for div in body.findAll('div', {'style': 'margin:5px;border:1px solid black'}):
        div.extract()
    
    with open('cleaned/{}'.format(fnm.split('/')[-1]), 'w+', encoding='utf-8') as f:
        out = unicode(
            ''.join(
                [str(tag) for tag in body.contents]
            ).replace(' style=""','').replace('\t', ''),
            encoding='utf-8')
        header = "" #"<meta charset='UTF-8'>"
        f.write(header+out)