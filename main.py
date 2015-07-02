import urllib.request
import urllib.parse
import chardet


def _test():
    search = input('Wich manga do you want to download? ')
    searchedValues = {'name': search}

    url = 'http://www.mangatown.com/search.php'
    contents = encodedDownload(url, searchedValues)
    arq = open('search.html', 'w')
    arq.write(contents)
    arq.close()


class Downloader():
    '''
    Basic Downloader class to download from a given URL.
    '''
    def __init__(self, url, textEncoding=None):
        self.url = url
        self.textEncoding = textEncoding
        self.contents = ''

    def requestData(self):
        req = urllib.request.Request(self.url)
        resp = urllib.request.urlopen(req)
        return(resp)

    def getAsBytes(self):
        resp = self.requestData()
        is_downloaded = (resp.getcode() == 200)
        if not is_downloaded:
            print('ERROR: Could not request the data!')
        else:
            respData = resp.read()
            self.contents = respData
            return(respData)

    def get(self):
        respData = self.getAsBytes()
        if self.textEncoding is None:
            self.textEncoding = chardet.detect(respData)['encoding']
        respData = respData.decode(self.textEncoding, 'ignore')
        self.contents = respData
        return(respData)


class EncodedDownloader(Downloader):
    '''
    Class for encoding values and download the result.
    '''
    def __init__(self, url, encodingValues={}, textEncoding=None):
        self.encodingValues = encodingValues
        self.contents = ''
        super().__init__(url, textEncoding)

    def requestData(self):
        encodingData = urllib.parse.urlencode(self.encodingValues)
        encodingData = encodingData.encode('utf-8')
        req = urllib.request.Request(self.url, encodingData)
        resp = urllib.request.urlopen(req)
        return(resp)


def download(url, textEncoding=None):
    downloader = Downloader(url, textEncoding)
    contents = downloader.get()
    return(contents)


def encodedDownload(url, encodingValues={}, textEncoding=None):
    downloader = EncodedDownloader(url, encodingValues, textEncoding)
    contents = downloader.get()
    return(contents)


if __name__ == '__main__':
    _test()
