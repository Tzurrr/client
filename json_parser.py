import json
import elogger
import sys
import local_logger


class ParseError(Exception):
    def __init__(self):
        message = "The contents of the File Wasn't Propriate"
        super(ParseError, self).__init__(message)


def parse_json_to_var(json_filename):
    try:
        with open(json_filename, "r") as log_file:
            log_json = json.load(log_file)
            return log_json            
    except Exception:
        err_type, value, traceback = sys.exc_info()
        elogger.write_logs_to_elastic('Error parsering %s: %s' % (value.filename, value.strerror))
        local_logger.log_to_local_file("filed parsing the conf file's JSON")
        raise ParseError

