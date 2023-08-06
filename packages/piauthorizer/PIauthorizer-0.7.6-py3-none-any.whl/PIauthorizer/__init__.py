from .autorest import *
from .ConfigManager import *
from .functional import *
from .logging import *

STS_URL = os.environ.get('AUTH_STS_URL', None)
if not STS_URL:
    raise Exception('No AUTH_STS_URL variable')
