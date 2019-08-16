# сделать загрузку из файла: репозиторий и версию ПО
# по окончании переписать файл настроек с указанием новой версии и зашифровать файл
# сделать защиту при чтении файла
# url='https://api.github.com/repos/ag8920/RemoteTable/releases/latest'
# out_file - закинуть в папку TMP

import json
import os

import requests
from tqdm import tqdm


# загрузка файла
def download_file(url: object, path: object, size: object) -> object:
    request = requests.get(url, stream=True)
    if request.status_code != 200:
        print('URL Error!')
        return

    downloaded_size = 0
    chunk_size = 65536
    with open(path, 'wb') as out_file:
        # pb = progressbar.ProgressBar(maxval=size).start()
        pb = tqdm(total=size)
        for chunk in request.iter_content(chunk_size):
            assert isinstance(chunk, object)
            out_file.write(chunk)
            # downloaded_size += len(chunk)
            # pb.update(downloaded_size)
            pb.update(len(chunk))
        pb.close()
    return


name = ""
old_version = ""
url = ""
path_settings = os.path.abspath(os.curdir)
settingsFile = 'settings.json'
fullpath = os.path.join(path_settings, settingsFile)
if os.path.isfile(fullpath):
    with open(fullpath) as f:
        data: object = json.load(f)
        url = data['url']
        old_version = float(data['version'])
        name = data['name']

out_file = os.path.abspath(name)  # r'G:/setup.exe'
r = requests.get(url)
if r.status_code == 200:
    response_dict = r.json()
    version = response_dict['tag_name']
    if old_version < float(version):
        old_version = version
        assets = response_dict['assets']
        repo_dict = assets[0]
        print('Download:', repo_dict['browser_download_url'])
        size = repo_dict['size']
        download_file(repo_dict['browser_download_url'], out_file, int(size))
        # print('Download: ' + size)

        # запись номера новой версии
        with open(fullpath, 'w', encoding='utf-8') as f:
            data['version'] = str(version)
            json.dump(data, f)

        if os.path.isfile(out_file):
            # os.remove(name)
            # os.rename('{0}.tmp'.format(name), name)
            os.startfile(name)
            # os.remove(file_path)
        else:
            print('File: ' + out_file + ' not found')
    else:
        print('No updates')
        if os.path.isfile(name):
            os.startfile(name)
else:
    print('URL: ' + url + ' Error')
