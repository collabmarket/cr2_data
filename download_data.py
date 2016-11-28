import os
import json
import urllib
import zipfile

def open_sources(filename):
    with open(filename) as data_file:
        return json.load(data_file)

def make_tmp(tmp):
    if not os.path.exists(tmp):
        os.mkdir(tmp)

def make_folders(sources):
    root = sources.keys().pop()
    if not os.path.exists(root):
        os.mkdir(root)
    folders = sources[root].keys()
    for folder in folders:
        fold = os.path.join(root, folder)
        if not os.path.exists(fold):
            os.mkdir(fold)

def download(period, sources):
    root = sources.keys().pop()
    items = sources[root][period]
    for item in items:
        filename = os.path.join(tmp, item['filename']+'.zip')
        urllib.urlretrieve(item['url'], filename)

def extractfiles(period, sources):
    root = sources.keys().pop()
    items = sources[root][period]
    for item in items:
        filename = os.path.join(tmp, item['filename']+'.zip')
        fold = os.path.join(root, period)
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall(fold)
        zip_ref.close()


if __name__ == '__main__':
    make_tmp('tmp')
    sources = open_sources('data.json')
    make_folders(sources)
    download('monthly', sources)
    download('daily', sources)
    extractfiles('monthly', sources)
    extractfiles('daily', sources)
