from django.core.exceptions import ObjectDoesNotExist
from Company.models import *

from utils.decorator import singleton

@singleton
class LoadPreprocessor:
    pass