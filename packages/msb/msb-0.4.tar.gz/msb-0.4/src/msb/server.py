import requests
import urllib.request
from tqdm import tqdm
from bs4 import BeautifulSoup


def check_connection(url):
    try:
        get = requests.get(url)
        soup = BeautifulSoup(get.text, features="html.parser")
        res = soup.find("div", {"class": "res"}).text
        if res == "":
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


def getForgeCode(url, version):
    get = requests.get(url)
    server = get.json()
    code = server["forgeAvailableVersions"][version]
    return code


def getSpigotCode(url, version):
    get = requests.get(url)
    server = get.json()
    code = server['spigotAvailableVersions'][version]
    return code


def login(file_url, key, userID, login, password):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept": "*/*", "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }

    data = f"key={key}&userID={userID}&login={login}&password={password}"
    res = requests.post(file_url, headers=headers, data=data)
    soup = BeautifulSoup(res.text, features='html.parser')
    response = soup.find('div', {"class": 'response'}).text

    return response


def getVipAmount(file_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept": "*/*", "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }

    res = requests.get(file_url, headers=headers)
    soup = BeautifulSoup(res.text, features="html.parser")
    response = soup.find("div", {"class": "resp"}).text

    return response

def deleteOneNumber(file_url, key, login, password):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept": "*/*", "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }

    data = f"key={key}&login={login}&password={password}"
    res = requests.post(file_url, headers=headers, data=data)
    soup = BeautifulSoup(res.text, features='html.parser')
    response = soup.find('div', {"class": 'resp'}).text

    return response