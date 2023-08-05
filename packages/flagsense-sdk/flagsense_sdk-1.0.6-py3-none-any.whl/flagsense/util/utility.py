import requests
import time

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Utility:
	@staticmethod
	def wait_until(condition, period=0.5):
		while True:
			if condition():
				return
			time.sleep(period)
	
	@staticmethod
	def wait_until_with_timeout(condition, period=0.5, timeout=10):
		mustEndAt = time.time() + timeout
		while time.time() < mustEndAt:
			if condition():
				return True
			time.sleep(period)
		return False
	
	@staticmethod
	def get_or_default(obj, key, defaultValue):
		if obj and key in obj:
			return obj[key]
		return defaultValue
	
	@staticmethod
	def requests_retry_session(
			retries=5,
			backoff_factor=2,
			session=None
	):
		session = session or requests.Session()
		retry = Retry(
			total=retries,
			read=retries,
			connect=retries,
			backoff_factor=backoff_factor,
			status_forcelist=[205, 408, 422, 429, 500, 501, 502, 503, 504]
		)
		adapter = HTTPAdapter(max_retries=retry)
		session.mount('https://', adapter)
		return session
