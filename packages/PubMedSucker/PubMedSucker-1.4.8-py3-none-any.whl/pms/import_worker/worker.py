import os
import time
import json
import urllib
from Configs import getConfig
from linetimer import CodeTimer
import logging
from logging import Logger
import sys
from getversion import get_module_version

from neobulkmp import WorkerSourcing
from pms.import_worker.downloader import download
from pms.import_worker.parser import PubMedXMLParser
from py2neo import Node, Graph
import pms

config = getConfig()

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)-15s %(processName)-8s %(module)-8s %(levelname)-8s:  %(message)s",
    handlers=[logging.StreamHandler((sys.stdout))],
)


class Worker(WorkerSourcing):
    log: Logger = None

    def _gather_source_data(self, xml_url: str):

        source_file = None
        # Check if argument is a local file or an url
        if os.path.isfile(xml_url):
            self.log.debug(f"{xml_url} is a local file. No download needed")
            source_file = xml_url

        elif urllib.parse.urlparse(xml_url).scheme in ["ftp", "http", "https", "ftps"]:
            source_file = download(xml_url)
        else:
            raise ValueError(
                f"Invalid source url/file. Expected HTTP/FTP-URL or local Path, got '{xml_url}'"
            )
        # Check if file is existent and accessible
        try:
            f = open(source_file)
        except:
            raise ValueError(f"Can not access '{source_file}'")
        finally:
            f.close()
        self.source_file = source_file

    def run(self):
        self.cache = self.cache_backend(self.cache_backend_params)
        self.log: logging.Logger = self.get_logger()
        self.log.addHandler(logging.FileHandler(config.WORKER_LOGFILE))
        self.graph = Graph(**config.NEO4J)
        self._gather_source_data(self.worker_parameter["xml_url"])
        if (
            self._fetch_loading_log() is not None
            and not config.FORCE_REMERGING_LOADED_PUBMED_XMLS
        ):
            self.log.info(
                "Skip '{}' . File was allready parsed and loaded into DB. ...".format(
                    self.source_file
                )
            )
            return
        self.log.info(f"Start parsing {self.worker_parameter['xml_url']} gogogoooo!")
        self.parser = PubMedXMLParser(parent_worker=self, xml_file=self.source_file)

        self.parser.run(self.cache)
        self._create_loading_log()

    def _create_node(self, labels: "list(str)", props: dict):
        # this is a little helper function to create some log,metadata nodes
        tx = self.graph.begin()
        tx.create(Node(*labels, **props))
        tx.commit()

    def _create_loading_log(self):
        self._create_node(
            config.LOADING_LOG_LABELS,
            {
                "filename": str(os.path.basename(self.source_file)),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S %z"),
                "PubMedSucker_Version": get_module_version(pms)[0],
                "article_deletions_count": len(self.parser.delete_pmids),
                "to_be_deleted_articles": self.parser.delete_pmids,
            },
        )

    def _fetch_loading_log(self):
        query = "MATCH (n:{}) WHERE n.filename='{}' return n".format(
            ":".join(config.LOADING_LOG_LABELS),
            str(os.path.basename(self.source_file)),
        )
        tx = self.graph
        cursor = tx.run(query)
        result = cursor.data()
        if len(result) == 0:
            return None
        else:
            return result[0]
