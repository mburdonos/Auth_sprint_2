import logging
import traceback

logfile = 'log_1.log'

log = logging.getLogger("my_log")
log.setLevel(logging.INFO)
FH = logging.FileHandler(logfile, encoding='utf-8')
basic_formater = logging.Formatter('%(asctime)s : [%(levelname)s] : \
    %(message)s')
FH.setFormatter(basic_formater)
log.addHandler(FH)


def error_log(line_no):
    """функция для записи в лог сообщений об ошибке"""
    err_formater = logging.Formatter('%(asctime)s : [%(levelname)s][LINE '
                                     + line_no + '] : %(message)s')
    FH.setFormatter(err_formater)
    log.addHandler(FH)
    log.error(traceback.format_exc())
    FH.setFormatter(basic_formater)
    log.addHandler(FH)
