import logging
import sys
from python_elastic_logstash import ElasticHandler, ElasticFormatter
import json_parser


class BlankIndexException(Exception):
    def __init__(self):
        message = "Index name Expected"
        super(BlankIndexException, self).__init__(message)

def write_logs_to_elastic(event_string):
    conf_dict = json_parser.parse_json_to_var("/home/tzur/client/config.json")
    url_path = conf_dict["kibanas_url"]

    if url_path == "":
        return

    logger = logging.getLogger(event_string)
    logger.setLevel(logging.DEBUG)
    elastic_handler = ElasticHandler(url_path)
    elastic_handler.setFormatter(ElasticFormatter())
    logger.addHandler(elastic_handler)
    logger.info(event_string)

