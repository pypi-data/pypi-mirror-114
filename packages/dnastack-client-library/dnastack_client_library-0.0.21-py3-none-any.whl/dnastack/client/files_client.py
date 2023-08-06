import click
import urllib3
import threading
import os
from typing import Optional
from dnastack.constants import *
from requests import Response
from requests.exceptions import HTTPError
from dnastack.client.utils import get_drs_client
import gzip
import re
import sys
import io
import pandas as pd

# since our downloads are multi-threaded, we use a lock to avoid race conditions
output_lock = threading.Lock()
exit_code_lock = threading.Lock()


def get_host(url):
    return re.search(r"(?<=https://)([^/])+(?=/.*)", url).group(0)


def handle_file_response(download_file, data):
    # decode if fasta
    if re.search(r"\.fa", download_file):
        data = data.decode("utf-8")

    return data


def file_to_dataframe(download_file, data):
    # turn into dataframe for FASTA/FASTQ files, otherwise just return raw data
    if re.search(r"\.fa", download_file):
        data = data.split("\n", maxsplit=1)

        meta = data[0]
        sequence = data[1].replace("\n", "")  # remove newlines

        return pd.DataFrame({"meta": [meta], "sequence": [sequence]})

    return data


def is_drs_url(url):
    return url[:6] == "drs://"


def get_object_info_url_from_drs(url):
    drs_host = re.search(r"(?<=drs://)([^/])+(?=/.*)", url)
    if not drs_host:
        click.secho(f"Could not get drs host from url {url}\n", fg="red")
        raise Exception(f"Could not get drs host from url {url}")
    object_url = f"https://{drs_host.group(0)}/ga4gh/drs/v1/"
    return object_url, drs_host


def get_object_id_from_drs(url):
    object_id = re.search(r"(?<=/)(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})", url)
    if object_id:
        return object_id.group(0)
    else:
        click.secho(f"Could not get drs object id from url {url}\n", fg="red")
        raise Exception(f"Could not get drs object id from url {url}")


def exit_download(url, code, exit_codes):
    if exit_codes is not None:
        exit_code_lock.acquire()
        exit_codes[url] = code
        exit_code_lock.release()


def download_file(url, output_dir, out: Optional[list] = None, exit_codes=None):

    http = urllib3.PoolManager()
    chunk_size = 1024
    download_url = url
    download_file = ""
    signed_access_ids = ["az-blobstore-signed"]

    if is_drs_url(url):
        # parse the drs url to the resource url
        try:
            drs_server, drs_host = get_object_info_url_from_drs(url)
            drs_client = get_drs_client(drs_server)
            object_id = get_object_id_from_drs(url)
            object_info = drs_client.get_object_info(object_id)
        except HTTPError as e:
            if e.response.status_code == 404:
                click.secho(f"DRS object with id {object_id} does not exist", fg="red")
            elif e.response.status_code == 403:
                click.secho("Access Denied", fg="red")
            else:
                click.secho(
                    "There was an error getting object info from the DRS Client",
                    fg="red",
                )
                exit_download(url, 1, exit_codes)
                return
        except Exception as e:
            exit_download(url, 1, exit_codes)
            return

        if "access_methods" in object_info.keys():
            for access_method in object_info["access_methods"][0]:
                if access_method.get("access_id", None):
                    if access_method["access_id"] in signed_access_ids:
                        click.echo("found signed access_id @ access_method level")
                        try:
                            object_access = drs_client.get_object_access(
                                object_id, access_method["access_id"]
                            )
                        except HTTPError as e:
                            click.echo(e)
                            exit_download(url, 1, exit_codes)
                        download_url = object_access["url"]
                        break

                # if we have an https, use that
                if access_method["type"] == "https":
                    download_url = access_method["access_url"]["url"]
                    download_file = download_url.split("/")[-1]
                    break
        else:
            return  # next page token, just return
    else:
        click.secho(f"[{url}] is not a valid DRS url", fg="red")
        exit_download(url, 1, exit_codes)
        return

    try:
        download_stream = http.request("GET", download_url, preload_content=False)
    except:
        click.secho("There was an error downloading " + download_url, fg="red")
        exit_download(url, 1, exit_codes)
        return

    if out is not None:
        data = handle_file_response(download_file, download_stream.read())
        output_lock.acquire()
        out = out.append(file_to_dataframe(download_file, data))
        output_lock.release()

    else:
        with open(f"{output_dir}/{download_file}", "wb+") as dest:
            stream_size = int(download_stream.headers["Content-Length"])
            click.echo(f"Downloading {url} into {output_dir}/{download_file}")
            file_stream = download_stream.stream(chunk_size)
            with click.progressbar(length=stream_size, color=True) as download_progress:
                for chunk in file_stream:
                    dest.write(chunk)
                    download_progress.update(chunk_size)
    exit_download(url, 0, exit_codes)


def download_files(
    urls,
    output_dir=downloads_directory,
    out=None,
):
    download_threads = []
    exit_codes = {}

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for url in urls:
        download = threading.Thread(
            target=download_file(
                url,
                output_dir,
                out=out,
                exit_codes=exit_codes,
            ),
            name=url,
        )
        download.daemon = True
        download_threads.append(download)
        download.start()

    for thread in download_threads:
        thread.join()

    # at least one download failed, raise an exception
    failed_downloads = [url for url, code in exit_codes.items() if code != 0]
    if len(failed_downloads) > 0:
        raise Exception(f"One or more downloads failed: [{','.join(failed_downloads)}]")
