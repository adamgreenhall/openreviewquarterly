#!/usr/bin/python
from os import system as run
import sys,os,glob,logging,shutil

from BeautifulSoup import BeautifulSoup,Comment
from textile import textile

import config

import getgoogledoc
from utils import *
from orqclasses import Issue,Contributor,Piece,Illustration

indent='    '



def main(update=False, build=False):
    if update:  
        update_content_from_web()
    if build:   
        rebuild_content_locally()
    
def parsebios(biosfile):
    '''get all contributor biographies from a gdocs html file'''
    def getAuthor(bio):
        '''get a single bio from a paragraph in the html file'''
        author= ' '.join(bio.text.replace('&nbsp;',' ').replace('&#39;',"'").split()[:2])
        #justbio=bio.text[len(author):]
        justbio=bio
        [stuff.extract() for stuff in justbio.findAll(text=author)]
        justbio=''.join([str(c) for c in justbio.contents])
        return author,str(justbio)
        
    with open(biosfile,'r') as file: bioshtml=BeautifulSoup(file.read())
    
    bioshtml=drop_comments(bioshtml)
    
    contributors=[]
    for para in bioshtml('p'):
        author,bio=getAuthor(para)
        if author: contributors.append(Contributor(author,bio))
    return contributors    

def update_content_from_web():
    clients=getgoogledoc.docs_authenticate(email='adam.greenhall@gmail.com',get_spreadsheets=True)
    def downloadPieces(issue):
        """fetch the pieces of the issue from google."""
        localfolder=os.path.join(config.infodir,'issues/{}/'.format(urlify(issue.name)))
        if not os.path.exists(localfolder): os.makedirs(localfolder)
        
        #get the pieces spreadsheet
        pieces_doc_title='orq{} pieces'.format(issue.number)
        piecesfilename=getgoogledoc.download(title=pieces_doc_title,exportas='csv',kind='spreadsheet',dirname=localfolder,clients=clients)
        #get the piece documents
        foldername='ORQ{num} {name}'.format(num=issue.number,name=issue.name)
        filenames=getgoogledoc.download(foldername=foldername,kind='document',exportas='html',dirname=localfolder,clients=clients)
        return 
    
    for issueD in config.issues:
        issue=Issue(**issueD)
        if issue.number<config.skip_issues_before: 
            logging.warning('skipping downloading for early issues')
            continue
        else:
            downloadPieces(issue)
    biosfile=getgoogledoc.download(title='biographies',kind='document',exportas='html',dirname=config.infodir,clients=clients)
    
    return     


def getPieces(issue):
    '''
    create a list of Piece objects.
    convert the piece html files to haml partials.
    '''
        
    pieces,illustrations=[],[]
    localfolder=os.path.join(config.infodir,'issues/{}/'.format(urlify(issue.name)))
    piecesfilename = os.path.join(localfolder,'orq{num} pieces.csv'.format(num=issue.number))        
    
    fields,data= readCSV(piecesfilename)
    for row in data:
            if not any(row): continue #blank row in spreadsheet
            if row[2].strip()=='illustration':
                p=Illustration(
                    name=row[0].strip(),
                    author=row[1].strip(),
                    piece=pieces[-1],
                    )
                filename=get_piece_filename(p,illustration=True)
                p.add_content(filename)
                pieces[-1].add_illustration(p)
                illustrations.append(p)
            else:
                p=Piece(
                    name=row[0].strip(),
                    author=row[1].strip(),
                    kind=row[2].strip(),
                    issue=issue.name
                    )
                filename=get_piece_filename(p)
                p.add_content(filename)
                pieces.append(p)
                    
    issue.pieces = pieces
    return pieces,illustrations
                            
def credit_pieces(pieces,contributors):
    def get_author(piece,contributors):
        return [c for c in contributors if piece.author == c.name][0]
    def get_illustrator(piece,contributors):
        try: return [c for c in contributors if piece.illustration.author == c.name][0]
        except AttributeError: #no illustration for piece
            return None
        
    for p in pieces:
        author=get_author(p,contributors)
        author.add_piece(p)
        illustrator=get_illustrator(p,contributors)
        if illustrator is not None: illustrator.add_piece(p.illustration)
    return
    
    
    
def get_piece_filename(p,illustration=False):
    nm=urlify(p.name if p.name!='' else urlify('untitled {} {}'.format(p.author_first,p.author_last)))
    if illustration: nm=p.piecename+'.jpg'
    else: nm='_'+nm+'.haml'
    return config.siteroot+'issues/{}/{}'.format(urlify(p.issue),nm)



if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s')
    
    contributors=parsebios(os.path.join(config.infodir,'biographies.html'))
    
    if False: 
        # get authors database add script
        print '\n'.join(c.database_insert() for c in contributors)
    
    # get the pieces from the back issue add script
    for issue in config.issues:
        issue=Issue(**issue)
        pieces,illustrations=getPieces(issue)
        print '\n\n\n'.join(p.database_insert(n) for n,p in enumerate(issue.pieces))
        print '\n\n\n'.join(i.database_insert() for i in illustrations)

    # add using "cat filename.txt | rails console"