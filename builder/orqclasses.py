import os,logging,shutil,subprocess
from config import siteroot,illustration_tag,illustration_tag_sized
from utils import *
#import premailer

indent='    '

from BeautifulSoup import BeautifulSoup,Comment

class Issue(object):
    def __init__(self,name,number,season,description='',current=False):
        vars(self).update(locals()) #load in inputs
    def __repr__(self): return '<Issue {}:{}>'.format(self.number,self.name)

def create_piece(**inputs):
    if inputs['kind']=='illustration': return Illustration(**inputs)
    else:
        inputs.pop('last') 
        return Piece(**inputs)

class Piece(object):
    def __init__(self, name,author,kind,issue):
        vars(self).update(locals()) #load in inputs
        #self.author=author.replace('&#39;',"'")
        names=self.author.split(' ')
        self.author_first=names[0]
        self.author_last=names[-1]
        
        piecename=urlify(self.name) if self.name!='' else urlify('untitled {} {}'.format(self.author_first,self.author_last))
        self.partial_filename=os.path.join(siteroot,'issues/{issue}/_{piecename}.haml'.format(issue=urlify(self.issue),piecename=piecename))
        self.url = '/issues/'+urlify(self.issue)+'#'+urlify(piecename)
        self.individual_filename=os.path.join(siteroot,'issues/{issue}/{piecename}.html.haml'.format(issue=urlify(self.issue),piecename=piecename))
    def database_insert(self,number_in_issue=None):
        args=dict(title=self.name, number=number_in_issue, kind=self.kind, content=self.html().replace('\n',' '))
        if args['number'] is None: args.pop('number')
        formatted_args=[":{}=>'{}'".format(k,escape_quotes(v)) for k,v in args.iteritems()]
        formatted_args=', '.join(formatted_args)
        formatted_args+=', :author_id=>Author.where(:first_name=>"{}",:last_name=>"{}").first.id'.format(self.author_first,self.author_last)
        formatted_args+=', :issue_id=>Issue.where(:title=>"{}").first.id'.format(self.issue)    
        #author_id: nil, issue_id: nil,
        return "Piece.new({}).save()".format(formatted_args)
        
    def html(self): return self.content_html
    def add_illustration(self,illustration): 
        self.illustration=illustration
        html=self.content_html
        
        out=html.find(illustration_tag)
        tag=illustration_tag
        if out==-1:
            out=html.find(illustration_tag_sized)
            if out==-1:
                logging.debug('illustration tag not found within {}   placing at end of piece.'.format(self.url))
                tag=None
            else: tag=illustration_tag_sized
        if tag is None:
            self.content_html+=self.illustration.html()
        else:
            if tag==illustration_tag: 
                size='100%'
            else: 
                size=tag.split('width:')[1].strip().split(' ')[0]
            self.content_html=html.replace(tag, self.illustration.html(size))
        return
        
    def add_content(self,filename):
        logging.info('reading '+filename+' author: '+self.author)
        self.content_html=subprocess.check_output(['haml','{}'.format(filename)])

class Illustration(Piece):
    def __init__(self, name,author,piece):
        self.parent_piece_name = piece.name
        self.parent_piece_author = piece.author
        self.issue=piece.issue
        if name=='': 
            self.name=piece.name #title the illustration by its accompanying piece name
            self.named_by_piece=True
        else: 
            self.name=name
            self.named_by_piece=False
        self.author=author
        names=self.author.split(' ')        
        self.author_first=names[0]
        self.author_last=names[-1]        
        self.piecename=urlify('{} {}'.format(self.name,self.author))
        self.url = os.path.join('/illustrations/{}.jpg'.format(self.piecename))
        self.kind='illustration'
    def add_content(self,filename): pass
    def html(self,width='100%'): 
        return "<img src='#{url}' width='#{width}'>\n".format(url=self.url,width=width)
class Contributor(object):
    def __init__(self, name,bio):
        self.name=name
        names=self.name.split(' ')
        self.firstname=names[0]
        self.lastname=names[-1]
        self.bio=bio        
        self.pieces=[]
    def add_piece(self,piece): self.pieces.append(piece)
    def __repr__(self): return '<Contributor: '+self.name+'>'
    def database_insert(self):
        return "Author.new(:first_name=>\"{fnm}\",:last_name=>\"{lnm}\", :biography=>'{bio}').save()".format(fnm=self.firstname,lnm=self.lastname,bio=escape_quotes(strip_classes(self.bio)))