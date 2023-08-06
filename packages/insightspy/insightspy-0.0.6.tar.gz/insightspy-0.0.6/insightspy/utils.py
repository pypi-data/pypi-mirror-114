import re
import json
import urllib
import requests
import functools
import time
from tqdm import tqdm


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value

    return wrapper_timer


def _single_spaced(x):
    return re.sub(" +", " ", x)


def _versions(current_version):
    url = f"https://pypi.org/pypi/insightspy/json"
    data = json.load(urllib.request.urlopen(url))
    # Get versions on pip
    versions_list = list(data["releases"].keys())
    versions_list.sort(key=lambda s: list(map(int, s.split("."))))
    latest_version = versions_list[-1]
    if latest_version != current_version:
        print(
            "Local version of insightspy is not the latest version"
            + f"({current_version} < {latest_version})"
        )


def _connect(url, timeout=0.5):
    try:
        r = requests.head(url, timeout=timeout)  # noqa F841
        return True
    except requests.exceptions.ConnectionError:
        return False


def _parse_locus(x):
    return re.split("-|:", x)


def _list_to_int_list(lis):
    out = []
    for x in lis:
        # Convert to float
        try:
            z = float(x)
        except ValueError:
            raise TypeError("one or more elements of the list are not integer valued")
        # check that it is an integer
        if (int(z) - z) == 0:
            out.append(int(z))
        else:
            raise TypeError("one or more elements of the list are not integer valued")
    return out


def _download(urls):
    """Generic downloader

    Downloads files with pretty downloader bar

    Args:
        urls (dict): a dictionary where the keys are the file destinations and the
            values are the urls from which the files are downloaded
    """
    for file, url in urls.items():
        r = requests.get(url, stream=True)
        total_size_in_bytes = int(r.headers.get("content-length", 0))
        block_size = int(1.049e6)  # 1 Mebibyte
        print(f"Downloading {file}...")
        progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
        with open(file, "wb") as f:
            for data in r.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
            progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            raise ValueError("Download did not complete!")
