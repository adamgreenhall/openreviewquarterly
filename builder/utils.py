import csv,re,unicodedata
from BeautifulSoup import Comment
#from soupselect import select as cssselect

#def urlify(str): return str.replace(' ','_').replace("'","").lower()


indent='    '
_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')

_nbspstart_re = re.compile(r'>(&nbsp;){2,}')


_drop_chars_list=['&#39;','?',"'"]
def urlify(value,replace_char='-'):
    value = replace_funny_charachters(value)
    for char in _drop_chars_list: value=value.replace(char,'')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub(replace_char, value).lower()
    
def replace_funny_charachters(value):
    try: 
        if not isinstance(value, unicode): value = unicode(value)
    except UnicodeDecodeError:
        value= unicode(value.decode('utf-8'))
    #value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value=value.encode('ascii', 'xmlcharrefreplace')
    if u"\u2019" in value: 
        print value
        raise ValueError
    return value
def add_layout_title(layout,title=""):
    return '---\nlayout: "{}"\ntitle: "{}"\n---'.format(layout,title)
def escape_quotes(str): return str.replace('"',r'\"')

def striplatex(txt):
    txt=re.sub(r"\\section\*{(\w+)}",r'<div class="subsection">\1</div>',txt)
    txt=txt.replace(r"\\",'')
    return txt

def is_blank_para(node):
    #for those double spaced paragraphs
    try: 
        str=''.join(node.findAll(text=True))
        return str=='&nbsp;'
    except AttributeError: #b.s. NavigableString not Node
        return True
def remove_nbsp_parastart(html):
    return re.sub(_nbspstart_re,r'>',html)

def readCSV(filenm):
    '''read csv data in a csv file into a list of lists'''
    def transpose(listoflists): return map(None,*listoflists)
    csvfile = open(filenm,'r')
    dialect = csv.Sniffer().sniff(csvfile.read(4048)) 
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    data=zip(*reader)
    csvfile.close()
    
    data=transpose(data) #return data in r,c index order 
    fields=data.pop(0) #fields are the first row of csv
    return fields,data


def drop_comments(soup):
    #get rid of html comments
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    
    #get rid of google docs comments
    gdocs_comment_links = soup.findAll('a',attrs={'name':re.compile('cmnt(_ref)?\d+')})
    
    for gc in gdocs_comment_links:
        if '<a href="#cmnt_ref' in str(gc):
            #print 'endnote',gc
            #print gc.parent.parent
            gc.parent.parent.extract()
        else:
            #print 'link',gc
            gc.parent.extract()
    sups=soup.findAll('sup')
    if sups: 
        print sups
        riaasds
    return soup


def partial(partialname,**kwargs):
    def escape_ruby_chars(str):
        badchars=['#','"']
        for c in badchars:
            try: str=str.replace(c,'\{}'.format(c))
            except AttributeError: break #don't need to do this for integers, bools,...
        return str
        
    #partial('contributor_bio', :locals => {:name => name, :description=>description, :img => person_image(name,noquotes=true)})
    outargs=[]
    for k,v in kwargs.iteritems():
        if v==True and isinstance(v,bool): outargs.append(':{}=>true'.format(k))
        else:       outargs.append(':{}=>"{}"'.format(k,escape_ruby_chars(v)))
    else: outargs=','.join(outargs)
    return '=partial("{nm}",:locals=> {{{args}}})\n'.format(nm=partialname,args=outargs)


def make_toc(pieces,style='issue'):
    toc=[]
    toc.append('#tableofcontents')
    toc.append(indent+'.toc_head {headtitle}'.format(headtitle = 'Contents' if style=='issue' else 'Pieces'))
    toc.append(indent+'.tocpieces')
    for piece in pieces:
        toc.append(indent*2+piece.toc_enrty(style))
    return '\n'.join(toc)

def strip_classes(html):
    rep={'<span class="c4">':'',
        '<span class="c3">':'',
        '<span class="c5">':'',
        '<span class="c6 c5">':'',
        '<span class="c6">':'',
        '<span class="c6 c4">':'',
        '<span class="c4 c6">':'',
        '<span>':'',
        '</span>':'',    
        'class="c1"':'',
        '&nbsp;':' ',
        '&rsquo;':"'",
        '&#39;':"'",
        
        }
    for old,new in rep.iteritems():
        html=html.replace(old,new)
    return html

def escape_quotes(s): 
    try: return s.replace("'","\\'").replace('"','\\"')
    except AttributeError: return s
# def convert_google_text_styling(soup):
#     for style in ['bold','italic','underline']:
#         classy=howdoigetthis_outofcss
#         for e in cssselect(soup, classy):
#             e['class']=''
#             e['style']="text-weight: {}".format(style) if style!='underline' else "text-decoration:underline"
#     return soup