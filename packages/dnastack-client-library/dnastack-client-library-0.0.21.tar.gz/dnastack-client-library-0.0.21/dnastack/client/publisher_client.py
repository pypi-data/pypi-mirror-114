from dnastack.client import *
import json


class PublisherClient:
    def __init__(
        self,
        dataconnect_url=None,
        collections_url=None,
    ):
        self.dataconnect_url = dataconnect_url
        self.collections_url = collections_url

        self.dataconnect = self.dataconnect(self)
        self.collections = self.collections(self)

    class dataconnect:
        def __init__(self, parent):
            self.parent = parent

        def query(self, q, download=False):
            return json.loads(
                dataconnect_client.query(
                    self.parent.dataconnect_url,
                    q,
                    download,
                )
            )

        def list_tables(self):
            return json.loads(
                dataconnect_client.list_tables(self.parent.dataconnect_url)
            )

        def get_table(self, table_name):
            return json.loads(
                dataconnect_client.get_table(self.parent.dataconnect_url, table_name)
            )

    class collections:
        def __init__(self, parent):
            self.parent = parent

        def list(self):
            return collections_client.list_collections(self.parent.collections_url)

        def list_tables(self, collection_name):
            return collections_client.list_tables(
                self.parent.collections_url, collection_name
            )

        def query(self, collection_name, query):
            return collections_client.query(
                self.parent.collections_url, collection_name, query
            )

    def load(self, urls, output_dir=downloads_directory):
        download_content = []
        download_files(
            urls,
            output_dir,
            download_content,
        )
        return download_content

    def download(self, urls, output_dir=downloads_directory):
        return download_files(
            urls,
            output_dir,
        )
