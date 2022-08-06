import re
import requests
from .models import Test
# http://127.0.0.1:8000/api/bt-payouts/
def my_scheduled_job():
  requests.get(url = 'http://127.0.0.1:8000/api/bt-payouts/')
