import logging 

logger = logging.getLogger('pyhgl')
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("[%(pathname)s:%(lineno)d] %(message)s "))
logger.addHandler(ch)



hook_verbose = False
tokenize_verbose = False
parser_verbose = False
