# demo
杂货
一个基于笔趣阁的小说下载脚本（个别小说html布局不同可能下载不了），能自动检测本地是否存在同名小说，可进行追加，或覆盖等操作。
需要的库有
import requests
import os
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError
from tqdm import tqdm
import time
