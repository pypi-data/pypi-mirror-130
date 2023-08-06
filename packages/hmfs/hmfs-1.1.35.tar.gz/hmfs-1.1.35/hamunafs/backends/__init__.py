from .base import BackendBase
from .bk_qiniu import Qiniu
from .bk_yaocdn import YaoStorage

backend_factory = {
    'qiniu': Qiniu,
    'yaocdn': YaoStorage
}