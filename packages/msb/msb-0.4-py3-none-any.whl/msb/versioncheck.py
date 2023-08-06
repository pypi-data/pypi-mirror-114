import requests
from bs4 import BeautifulSoup


def getFromDB(file_url):
    res = requests.get(file_url)
    soup = BeautifulSoup(res.text, features="html.parser")
    version = soup.find("div", {"class": "resp"}).text
    return version


def isUpdates(file_url, clientVersion):
    version = getFromDB(file_url)
    return version != clientVersion

def isUpdatesMsb(file_url):
    version = ""
    try:
        from pip._internal.utils.misc import get_installed_distributions
    except ImportError:
        from pip import get_installed_distributions
    installed = get_installed_distributions()
    actualVersion = getFromDB(file_url)
    for i in installed:
        if i.key == "msb":
            #print(i.key)
            version = i.version
            #print(i.version)
    #print(actualVersion)
    return actualVersion != version


