import os

from django.contrib.auth import get_user_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

User = get_user_model()
