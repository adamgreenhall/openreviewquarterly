#http://code.google.com/apis/documents/docs/1.0/developers_guide_python.html#DownloadingWPDocuments

import getpass,logging
import sys,os
#sys.path.insert(0,'../../code/python/gdata-current/gdata-python-client/src/')
#sys.path.append('~/Documents/code/python/')
from gdocs3 import client as gclient
#from gdata import spreadsheet.service.SpreadsheetsService as gdata_spreadsheetService
import gdata.spreadsheet.service





email_default = 'adam.greenhall@gmail.com'
app_name='adam-orq-builder'

def docs_authenticate(email=email_default,pw=None,get_spreadsheets=False):
    def spreadsheet_authenticate(email=email_default,pw=None):
        gs_client = gdata.spreadsheet.service.SpreadsheetsService()
        gs_client.ssl = True
        
        gs_client.ClientLogin(email,pw,source=app_name)
        return gs_client


    gd = gclient.DocsClient(source=app_name)
    if pw is None: 
        logging.info('logging in to gDocs as: {}'.format(email))
        pw=getpass.getpass()
    gd.ClientLogin(email, pw, gd.source)
    gd.ssl = True  # Force all API requests through HTTPS
    gd.http_client.debug = False  # Set to True for debugging HTTP requests
    
    if get_spreadsheets: gs=spreadsheet_authenticate(email,pw)
    else: gs=None

    return dict(document=gd,spreadsheet=gs)

def find_file(clients,title,kind='document'):
    def retry_without_exact(uri):
        uri=uri.replace('title-exact=true','')
        return client.GetDocList(uri),uri

    if kind not in ['document','spreadsheet','pdf']: kind=None
    #query='?title={}&title-exact=true&max-results=5'.format(title.replace(' ','&'))
    query='?title={}&max-results=5'.format(title.replace(' ','&'))
    if kind is None: uri='/feeds/default/private/full'+query
    else: uri='/feeds/default/private/full/-/{}'.format(kind)+query
    feed = clients['document'].GetDocList(uri)
    try: return feed.entry[0]
    except IndexError:
        #feed,uri=retry_without_exact(uri)
        #try: return feed.entry[0]
        #except IndexError:
        msg='Document {title} not found in gDocs. Search was for {search}'.format(title=title,search=uri)
        raise IOError(msg)
def find_folder(clients,foldername):
    feed = clients['document'].GetDocList(uri='/feeds/default/private/full/-/folder')
    for entry in feed.entry:
        if entry.title.text.lower() == foldername.lower(): return entry
    else: raise IOError('folder "{}" not found'.format(foldername))
def download_folder(clients,folder,localdirname='',kind='document',exportas='html'):
    outfilenames=[]
    folderfeed = clients['document'].GetDocList(uri=folder.content.src)
    for doc in folderfeed.entry:
        if doc.GetDocumentType() == kind:
            filename=download_file(clients,doc,dirname=localdirname,exportas=exportas)
            outfilenames.append(filename)
    return outfilenames
def download_file(clients,doc,dirname='',exportas='html'):
    filename = os.path.join(dirname,doc.title.text+'.'+exportas)
    logging.info('Downloading document to {f}...'.format(f=filename))

    docs_token=clients['document'].auth_token
    if doc.GetDocumentType()=='spreadsheet':
        logging.debug('authorizing spreadsheet download')
        clients['document'].auth_token = gdata.gauth.ClientLoginToken(clients['spreadsheet'].GetClientLoginToken())
        
    try: clients['document'].Export(doc, filename)
    except:
        msg= 'couldn\'t export "{name}" ({nativekind}) as {kind}'.format(name=doc.title.text,nativekind=doc.GetDocumentType(),kind=exportas) 
        logging.error(msg)
        raise
    clients['document'].auth_token=docs_token #reset to the documents authorization 
    return filename

def download(title='biographies',
           foldername=None,
           exportas='html',
           kind='document',
           dirname='.',
           email=email_default,
           clients=None):    
    #login
    if clients is None: clients=docs_authenticate(email=email,pw=None,get_spreadsheets=True)
    
    if foldername is None:
        #find doc
        doc=find_file(clients,title,kind)
        #export
        filename = download_file(clients, doc, dirname=dirname,exportas=exportas)
        return filename
    else: 
        #find folder
        folder=find_folder(clients,foldername)
        #export
        filenames=download_folder(clients,folder,localdirname=dirname,kind=kind,exportas='html')
        return filenames

def test():
    logging.basicConfig( level=logging.DEBUG, format='%(levelname)s: %(message)s')
    #filename=download(title='biographies',exportas='html',kind='document',dirname='info')
    filename=download(title='orq1 pieces',exportas='csv',kind='spreadsheet',dirname='info')
    #filename=download(foldername='ORQ4 interview',exportas='html',kind='document',dirname='info/orq4 interview')
    
    

if __name__ == '__main__': test()