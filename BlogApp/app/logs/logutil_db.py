import logging
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi.logger import logger as fastapi_logger
from pydantic import BaseModel
import sys

sys.path.append("..")
from logs import models
from logs import dbconf
from logs import session_scope


class SQLALCHAMYHandler(logging.Handler):
    """
    Logging handler for SqlAlchamy.
    """

    def __init__(self):
        logging.Handler.__init__(self)
        # defining custom log format
        self.LOG_FORMAT = "%(asctime)s:%(msecs)03d %(levelname)s " \
                          "%(filename)s:%(lineno)d %(message)s | "
        # defining the date format for logger
        self.LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
        models.Base.metadata.create_all(bind=dbconf.engine)

    class ProcessLogModel(BaseModel):
        created: datetime
        name: str
        loglevel: int
        loglevelname: str
        fileid: int
        args: str
        module: str
        funcname: str
        lineno: str
        exception: str
        process: int
        thread: str
        threadname: str

    # -------------- Log data ----------------- #
    def insert_log(self, log: ProcessLogModel):
        try:
            with session_scope() as session:
                db_log = models.ProcessLog(Created=log.created,
                                           Name=log.name,
                                           LogLevel=log.loglevel,
                                           LogLevelName=log.loglevelname,
                                           FileId=log.fileid,
                                           Args=log.args,
                                           Module=log.module,
                                           FuncName=log.funcname,
                                           LineNo=log.lineno,
                                           Except=log.exception,
                                           Process=log.process,
                                           Thread=log.thread,
                                           ThreadName=log.threadname)
                session.add(db_log)
                session.commit()
                # session.refresh(db_log)
        except SQLAlchemyError as e:
            raise e

    def emit(self, record):
        record.dbtime = datetime.utcfromtimestamp(record.created).strftime(
            "%Y-%m-%d %H:%M:%S")
        f = OneLineExceptionFormatter(self.LOG_FORMAT,
                                      self.LOG_DATE_FORMAT)
        if record.exc_info:
            record.exc_text = f.formatException(record.exc_info)
            # added for fixing quotes causing error
            record.exc_text = record.exc_text.replace("'",
                                                      '"')
        else:
            record.exc_text = ""

        # Insert log record:
        log_data = record.__dict__
        log = self.ProcessLogModel(created=log_data['dbtime'],
                                   name=str(log_data['name']),
                                   loglevel=int(log_data['levelno']),
                                   loglevelname=str(log_data['levelname']),
                                   fileid=int(log_data['msg']),
                                   args=str(log_data['args']),
                                   module=str(log_data['module']),
                                   funcname=str(log_data['funcName']),
                                   lineno=str(log_data['lineno']),
                                   exception=str(log_data['exc_text']),
                                   process=int(log_data['process']),
                                   thread=str(log_data['thread']),
                                   threadname=str(log_data['threadName']))
        # insert error log in to table
        self.insert_log(log)


# custom log formatter
class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super(OneLineExceptionFormatter, self).formatException(
            exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s


# defining log levels
# LOG_LEVEL = logging.ERROR

# Configuring Logs
# db_logger = logging.getLogger()
# db_logger.setLevel(LOG_LEVEL)

# add database handler
handler = SQLALCHAMYHandler()
# db_logger.addHandler(handler)

gunicorn_logger = logging.getLogger("gunicorn.error")
fastapi_logger.setLevel(gunicorn_logger.level)
# add database handler
fastapi_logger.addHandler(handler)
