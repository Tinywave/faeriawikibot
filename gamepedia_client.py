import mwclient
import hashlib


class GamepediaClient:
    mwc = None

    '''
    Login on creation
    '''

    def __init__(self, url='faeria.gamepedia.com', username=None, password=None):
        self.mwc = mwclient.Site(url, path='/')
        if username is not None and password is not None:
            self.mwc.login(username, password)

    '''
    Login to edit pages and get attribution
    '''

    def login(self, username, password):
        self.mwc.login(username, password)

    '''
    Return the text content of a page
    '''

    def read(self, pagename):
        return self.mwc.Pages[pagename].text()

    '''
    Overwrite whole page with text
    '''

    def write(self, pagename, text):
        page = self.mwc.Pages[pagename]
        page.save(text)

    '''
    Upload local image to wiki
    '''

    def upload_images(self, imagename, destination, description, onlyupdate):
        if onlyupdate:
            img = self.mwc.Images[destination]
            if img.exists:
                sha1 = hashlib.sha1()
                sha1sum = ''
                with open(imagename, 'rb') as f:
                    sha1.update(f.read())
                    sha1sum = sha1.hexdigest()
                if img.imageinfo['sha1'] == sha1sum:
                    return
        self.mwc.upload(file=open(imagename, 'rb'), filename=destination, description=description, ignore=True)




    '''
    Upload remote image to wiki
    '''

    def upload_remote_image(self, url, destination, description):
        self.mwc.upload(url=url, filename=destination, description=description)


