try:
    from wizzi_utils.models.models import *
    from wizzi_utils.models import object_detection as od
    from wizzi_utils.models import pose_detection as pd
except ModuleNotFoundError as e:
    pass

from wizzi_utils.models import test
