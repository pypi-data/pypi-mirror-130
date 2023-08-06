import os.path

import requests

cache_root = os.path.join(os.environ['HOME'], 'notecache')


def load_url_to_cache(url: str, overwrite=False):
    if url.startswith("https://raw.githubusercontent.com/notechats"):
        base_url = url.split("https://raw.githubusercontent.com/")[1]
        base_path, filename = os.path.split(base_url)
        cache_path = os.path.join(cache_root, base_path)
        file_path = os.path.join(cache_path, filename)

        # 如果缓存路径不存在则创建
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        # 如果文件已存在
        if os.path.exists(file_path):
            # 如果不覆盖就返回，覆盖就删除原文件
            if not overwrite:
                return
            else:
                os.remove(file_path)

        with open(os.path.join(cache_path, filename), 'wb') as f:
            content = requests.get(url).content
            f.write(content)
