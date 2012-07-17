from utils import *
import os,re,glob,logging
from BeautifulSoup import BeautifulSoup
import config




def main():
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s', filename='conversion.log',filemode='w+')
    for n,issue in enumerate(config.issues):
        issuenum=len(config.issues)-n
        if issuenum>3: 
            logging.debug('dont translate any issues past #3')
            continue
        texdir='../orq{}/final/'.format(issuenum)
        outdir='info/issues/{}/updates_from_tex/'.format(urlify(issue))

        piecenames = glob.glob(texdir+'*.tex')
        
        for texfile in piecenames:
            if issue=='Unplugging': skip_authors=['mittelsteadt','meltzer','gupta']
            elif issue=='Adventure': skip_authors=['wolcott','sassman']
            elif issue=='Digital Presence': 
                skip_authors=[
                    'ahillen','bernstein','birks','buckley',
                    'blickenstaff','heffernan','meltzer','wolcott','wallace',
                    'greenhall']
            else: skip_authors=[]
            
            if any(a in texfile.lower() for a in skip_authors): continue
            
            logging.info('converting: {}'.format(texfile))
            outputfile=os.path.join(outdir,os.path.basename(texfile)+'.html')

            with open(texfile,'r') as file: latex=file.read()
            with open(outputfile,'w+') as file: file.write(latex2html(latex))
        
def test(
    texfile='../orq3/final/ORQ3_Blickenstaff.tex',
    outputfile='info/issues/digital-presence/updates_from_tex/ORQ3_Blickenstaff.tex.html'
    ):
    
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    with open(texfile,'r') as file: latex=file.read()
    with open(outputfile,'w+') as file: file.write(latex2html(latex))

    

tex2html_replacements={
    r'\&'   :'&amp;',
    r'\#'   :'&#35;',
    r'\%'   :'&#37;',
    r'\$'   :'&#36;',
    '---'   :'&mdash;',
    '--'   :'&ndash;',
    r'\ldots':'&hellip;', #elipsis
    r'\-':'', #ignore hypenation helpers,
    r'~':' ', #convert spacing helpers
    }

tex_command_re=re.compile(r'(\\[a-zA-Z]+\*?)((\{[^\{\}]+\})*)?')
tex_para_re=re.compile(r'(\\\\\*?\n+\s?([\w+&;]))')
tex_paperdigital_re= re.compile(r'(\\paperonly|\\digitalonly)(\{\\?\w+\})')#'\\paperonly\{(.)\}')

tex_verb_re = re.compile(r'=(\d+)=')
tex_accents_grave_re = re.compile("\\`\{([a-z])\}")
tex_accents_acute_re = re.compile("\\'\{([a-z])\}")

ignore_commands=[
    'indentpattern',   'noindent',   'hspace', 'vspace',    'lstset',
    'large',    'small',    'tiny',    'normalsize',
    'paper',    'digital',
    'restoregeometry',    'columnbreak',    'pagestyle',
    'flagverse',    'fill',    'fussy',    'sloppy',
    'addtotocimg',    'marginparwidth',    'newgeometry',
    ]
ignore_beginend_options=[
    'dialog',    'patverse',
    'dutchparagraphs',    'adjustwidth',    'minipage',
    'flushleft',
    ]
warn_beginend_options=[
    'multicols',
    ]
environment_class_map={
    'center':'center',
    'quote':'blockquote',
    'flushright':'right',
    'lstlisting':'div class="verbatim" style="font-family: courier;"',
    #'hspace':'span class="hspace" style="width:"',
    }
command_html_map ={
    'textit':'i',
    'textbf':'b',
    'emph':'em',
    'underline':'u',
    'attrib':'div class="attrib"',
    'sms':'span class="sms" style="font-family: sans-serif"',
    'datingstory':'div class="dating_story"',
    }

def convert_tex_command(tex,cmd,custom_commands):
    def check_command_ignore(command): return any(ignore in command.lower() for ignore in ignore_commands)
    def check_options(options,command): return command in [r'\begin', r'\end'] and any(ignore in options.lower() for ignore in ignore_beginend_options)
    def check_options_warn(options,command): 
        return command in [r'\begin', r'\end'] and any(warn in options.lower() for warn in warn_beginend_options)


    def equiv_env_html(options,command): return command in [r'\begin',r'\end'] and options in environment_class_map.keys()
    def replace_environment(tex,env,begin_end,cmd_str):
        divclass=environment_class_map[env]
        if not begin_end==r'\begin' and divclass.startswith('div'): divclass='div' #end div tag with div
        out= tex.replace(cmd_str,'<{}{}>'.format('' if begin_end==r'\begin' else '/' , divclass))
        return out

    def equiv_command_html(command): return any(c in command for c in command_html_map)
    def replace_command(tex,command, apply_to_text,cmd_str):
        cmd_txt=command.strip(r'\\')
        start_tag=command_html_map[cmd_txt]
        if start_tag.startswith('div'):
            end_tag = 'div'
        elif start_tag.startswith('span'):
            end_tag = 'span'
        else: 
            end_tag = start_tag
        out='<{starter}>{txt}</{ender}>'.format(starter=start_tag, ender=end_tag,txt=apply_to_text)
        
        return tex.replace(cmd_str,out)
        #return tex.replace(cmd_str,'<{html}>{txt}</{html}>'.format(html=command_html_map[command.strip(r'\\')],txt=apply_to_text))
    def replace_link(cmd_str,tex):
        try: href,link,name= cmd_str.replace('}','').split('{')
        except ValueError: 
            logging.error('could not process link name: {}'.format(cmd_str))
            href,link= cmd_str.replace('}','').split('{')
            name='??'
        if not link.startswith('http:'): link=r'http://'+link
        html_link='<a rel="external" href="{}">{}</a>'.format(link,name.strip())
        return tex.replace(cmd_str,html_link)

    command,options,lastopt=cmd
    cmd_str=''.join([command,options])
    options=options.replace('{','').replace('}','')

    #print cmd_str
    unknown,custom_command='',''
    if command==r'\href': tex=replace_link(cmd_str,tex)
    elif command.lower()==r'\sectiondivider':
        tex=tex.replace(cmd_str,'<div class="sectiondivider"><center>&diams;</center></div>')
    elif command.startswith(r'\subsection'):
        tex=tex.replace(cmd_str,'<div class="subsection">{}</div>'.format(options))
    elif command==r'\footnote':
        if options:
            replacement='<span class="parenthesis" title="{}">()</span>'.format(options)
            tex=tex.replace(cmd_str,replacement)
        else:
            logging.warning('blank footnote found')
            tex=tex.replace(cmd_str,'')
    
    elif equiv_env_html(options,command): tex=replace_environment(tex,options,command,cmd_str)
    elif equiv_command_html(command): tex=replace_command(tex,command, options,cmd_str) 
        
    elif command.count('includeillustration'):
        tex=tex.replace(cmd_str,'</p>\n=== Illustration ===\n<p>\n')
    elif command.count('madlibStyle'): 
        tex=tex.replace(cmd_str,'<span class="madlib">{}</span>'.format(options))
    else: 
        tex=tex.replace(cmd_str,'')
        

        if check_command_ignore(command): pass
        elif check_options(options,command): pass
        elif check_options_warn(options,command): logging.warning('environment: {}'.format(options))
        #elif 'paragraphs' in options: pass
        elif 'providecommand' in command: 
            logging.critical('custom command: "{}"'.format(options))
            custom_command=options
        elif command in custom_commands: pass
        else: 
            unknown=cmd_str
            #print unknown
            #raise ValueError
    return tex,unknown,custom_command
    
def convert_tex_paras(tex):
    def makepar(line): return '<p>'+line.rstrip(r"\\")+'</p>'
    def endstanza(line): return line.rstrip(r"\\")+'</p>\n<p>'
    
    paragraphs=[]
    poem=False
    
    if all( ln.endswith(r"\\") for ln in tex.splitlines()):
        out='<p>'+tex.replace(r"\\",'<br>')+'</p>'
        return out
    
    for line in tex.splitlines():
        line=line.strip()
        if line.endswith(r"\\"):
            if poem: paragraphs.append(endstanza(line))
            else: paragraphs.append(makepar(line))
        elif line.endswith(r"\\!"):
            paragraphs.append(makepar(line.rstrip('!'))+'<br>')
        elif line.endswith(r"\\*"):
            poem=True
            paragraphs.append(line.rstrip(r'\\*')+'<br>')
        elif line:
            line = '<br>'.join(line.split(r"\\"))
            paragraphs.append(line)
        
    out='\n'.join(paragraphs)
    if poem: out='<p>'+out+'</p>'
    return out
    
    #for parbreak in tex_para_re.findall(tex):
    #    wholetext,nextpar_firstchar=parbreak
    #    tex=tex.replace(wholetext,'</p>\n\n<p>{}'.format(nextpar_firstchar))
    #return '<p>\n'+tex.replace(r'\\','')
def convert_tex_quotes(tex):
    tex=tex.replace("``",'&ldquo;')
    tex=tex.replace("''",'&rdquo;')
    tex=tex.replace("`", '&lsquo;')
    tex=tex.replace("'", '&rsquo;')
    return tex

def convert_tex_accents(tex):
    for accented_letter in tex_accents_grave_re.findall(tex):
        #print accented_letter
        tex=tex.replace( "\\`{{{}}}".format(accented_letter), '&{}grave;'.format(accented_letter) )
    for accented_letter in tex_accents_acute_re.findall(tex):
        #print accented_letter
        tex=tex.replace( "\\'{{{}}}".format(accented_letter), '&{}acute;'.format(accented_letter) )
    return tex

def strip_comments(tex):
    out=[]
    for line in tex.splitlines():
        if line.startswith('%'): continue
        else: out.append(line)
    return '\n'.join(out)

def drop_custom_commands(tex):
    tag=r'\providecommand{'
    loc_start=tex.find(tag)
    if loc_start==-1: return tex
    
    loc_end = tex[loc_start:].find('}')
    command= tex[len(tag):loc_start+loc_end]
    command_name=command.lstrip('\\')
    logging.info('replacing custom command {}'.format(command))
    
    tex='\n'.join([ln for ln in tex.splitlines() if tag not in ln])
    
    
    # while command in tex:
    #     loc_start=tex.find(command)
    #     tex=tex.replace(command+'{','<span class="{}">'.format(command_name),1)
    #     tex=tex[:loc_start]+tex[loc_start:].replace('}','</span>',1)
    
    return tex
    

def latex2html(tex):

    tex=strip_comments(tex)

    tex=convert_tex_accents(tex)

    tex=drop_custom_commands(tex)

    for old,new in tex2html_replacements.iteritems():
        tex=tex.replace(old,new)

    tex=convert_tex_quotes(tex)
    
    for cmd in tex_paperdigital_re.findall(tex):
        pd_switch,inside=cmd
        cmd_str=''.join(cmd)
        if pd_switch==r'\\digital': tex=tex.replace(cmd_str,inside)
        else: tex=tex.replace(cmd_str,'')
    

    
    #print tex_command_re.findall(tex)
    #gascas
    unknowncommands,custom_commands=[],[]
    for cmd in tex_command_re.findall(tex): 
        tex,unknown,custom = convert_tex_command(tex,cmd,custom_commands)
        if unknown: unknowncommands.append(unknown)
        if custom: custom_commands.append(custom)
    for verb in tex_verb_re.findall(tex):
        tex=tex.replace('={}='.format(verb),'<span style="font-family:courier">{}</span>'.format(verb))
    tex=convert_tex_paras(tex)
    if unknowncommands:
        logging.info('unknown: {}'.format(unknowncommands))
    
    #html=BeautifulSoup(tex).prettify()#
    html=str(BeautifulSoup(tex))
    
    html=html.replace('\n','')
    
    #and you still wind up with blank latex command options
    html=html.replace('{}','')
    html=html.replace('[]','')
    #html=html.replace('[1]{<u></u>{{<i></i>}}}','')
    #html=html.replace('[1]{}[1]{{<em></em>{{ #1}}}}<p></p>','')
    # warningChars=['{','}']
    # if any( char in html for char in warningChars):
    #     print [char in html for char in warningChars]
    #     raise ValueError
        
    return html
    
if __name__ == '__main__':
    
    main()

