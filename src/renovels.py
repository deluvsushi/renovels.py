import requests

class Renovels:
	def __init__(self) -> None:
		self.api = "https://api.renovels.org"
		self.recaptcha_api = "https://www.google.com/recaptcha/api2"
		self.headers = {
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
		}
		self.user_id = None
		self.access_token = None

	def generate_captcha(
			self,
			hl: str = "en",
			vh: int = 957769019,
			cb: str = "ldc1g171u95e",
			size: str = "invisible",
			chr: str = "[20,59,35]",
			v: str = "PRMRaAwB3KlylGQR57Dyk-pF",
			key: str = "6LdGNc8UAAAAAOi7mZdoujfQ0s-zHexDM8AWyB1J",
			co: str = "aHR0cHM6Ly9yZW5vdmVscy5vcmc6NDQz",
			bg: str = "!PjigOD0KAAQeDmbXbQEHnAPKGu-t_o708wc3kcTmcuDgv3uLL8uZv86ItulHJ4T8KxIrUaFTX3YvwThY_KZD2eAAaB1-LDAID-Ac9eenF4fc7jH8d7cs3bHwgC_v8MCYTsnbxk6XyKnzGcbDY5MkkUUvP1uqI5AgC01qW66QeMmAbcBXfsO9PQmcKCkdMpWg_rdnbLNQ8123t0zAn43NngTp2udEJLfTReZDUW0dFelpuWcLKQPgmqCp4ql7zuw0rdLz-I2SqLTq24KxiLQ_IdEDU47Stj7-kFGStxAIpC90Yb87l-ZvLnLOanQhqsSXrAFfk1Iq3WH8psN_HQocY5_3KvEM6icEVOTP7O92NwXtF_CR5rtEcRQCRWy6FwXq7IJU9llLiMGs-b-riJF6KZ41E7_thePws0-Rs7MZT1qMXfDjOi6rog3iqVJ89bXfaVRoCKr-pbvAOcJv2WNEIIVCCDQdEP0rSNHYFuQifX03gzB3xNYPctixe1UIMS2vdT75vaaRTSqG1NdZd8ur3DdhqZMs6CYr8ePZmMWKle3e0S5o3-jF2Whu7demXBYJJHLYUVUyBeSrwVROzUYEdz2ig2noOisgyAIgSYFhjQ2FpkpQ4pkBocNlmbmmJsceaA0b-Q8bNa4m9BDa6z3wX3ES_kRnOz9n_j2VK1LvkIElz4hMOQM3BbWqT4QrOIFcGU_ZdPc91aDCxhHfPPiZW8plmAuTam4XrCInIbT-UTP8L6sRzpqY3yuMySkWhmKQXNIYhThrl11GkbzmuUS8RKCwcZyDp1OK9RSNXXI6NSo5DXqb9XLNXU_d6DBIh8Ozrh7HsHE0m6pAZJCs-K4PwYwWbOebyWZiPiiQaqpzXtAqJVjNuZZ2Qv4jHzhV9v2HKgJeEPNucpB_nACcVURvFzL4VTiBxeb5XVoEWLeteBg-T4uEuGbV8dfQKJ6kCetWAycvzXwzzqH-X-_BSRzAVdcIcoxIJ-iQsXtsFRna4SJDvbThEtnCyyo9JMTjfhLOdK9t3kZ6fvKMTWmJWlQZ4t1c_0i2tT8BaUc9UumCe6RAuFLLlxY2qoGPcjbngQjMTakGAPyEVuiz0d4tmZb974qp1cELMXzjyuJciYUtYwW5c8zNOmwo8pzsPM09zHrlZTY7aA9BsR4ev9gl7c5KnEPKyhWjqEoljgeSF5FpyJs4ERQfgXpl82W9P75ppRXvbgeRz8L6eujdlI_Rd_SSM2TgNsQhZDn4HKA_ky7p0tMx5GW49Ww3-fKrns5p3DSy5x7COcsNNqnCGCmjft_awzS-bBgBAWaORIy5Ng*") -> str:
		parameters = f"v={v}&reason=q&c=<token>&k={key}&co={co}&hl={hl}&size={size}&chr={chr}&vh={vh}&bg={bg}"
		anchor = requests.get(
			f"{self.recaptcha_api}/anchor?ar=1&k={key}&co={co}&hl={hl}&v={v}&size={size}&cb={cb}",
			headers=self.headers).text
		recaptcha_token = anchor.split(
			'recaptcha-token" value="')[1].split('">')[0]
		data = parameters.replace("<token>", recaptcha_token)
		self.headers["content-type"] = "application/x-www-form-urlencoded"
		response = requests.post(
			f"{self.recaptcha_api}/reload?k={key}",
			data=data,
			headers=self.headers).text
		return response.split(
				'"rresp","'
			)[1].split('"')[0] if "rresp" in response else response

	def login(
			self,
			username: str,
			password: str) -> dict:
		data = {
			"user": username,
			"password": password,
			"g-recaptcha-response": self.generate_captcha()
		}
		response = requests.post(
			f"{self.api}/api/users/login/",
			data=data,
			headers=self.headers).json()
		if "content" in response:
			self.user_id = response["content"]["id"]
			self.access_token = response["content"]["access_token"]
			self.headers["authorization"] = f"bearer {self.access_token}"
		return response

	def send_comment(
			self,
			text: str,
			title_id: int,
			is_pinned: bool = False,
			is_spoiler: bool = False) -> dict:
		data = {
			"is_pinned": is_pinned,
			"is_spoiler": is_spoiler,
			"text": text,
			"title": title_id
		}
		return requests.post(
			f"{self.api}/api/activity/comments/?title_id={title_id}",
			data=data,
			headers=self.headers).json()

	def logging(self, path_name: str = "/") -> dict:
		data = {
			"user": self.user_id,
			"access_token": self.access_token,
			"msg": "CONSOLE",
			"location": {
				"pathname": path_name,
				"search": "",
				"hash": "",
				"key": ""
			},
			"deviceType": "desktop",
			"appVersion": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
			"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
		}
		return requests.post(
			f"{self.api}/api/logging/",
			data=data,
			headers=self.headers).json()

	def similar_titles(self, title: str) -> dict:
		return requests.get(
			f"{self.api}/api/titles/{title}/similar/",
			headers=self.headers).json()

	def search_title(
			self,
			title: str,
			count: int = 5) -> dict:
		return requests.get(
			f"{self.api}/api/search/?query={title}&count={count}",
			headers=self.headers).json()

	def search_publishers(
			self,
			username: str,
			page: int = 1,
			count: int = 10) -> dict:
		return requests.get(
			f"{self.api}/api/search/?count={count}&field=publishers&page={page}&query={username}",
			headers=self.headers).json()

	def edit_profile(
			self,
			username: str = None,
			adult: bool = False,
			sex: int = 0,
			yaoi: int = 0) -> dict:
		data = {
			"adult": adult,
			"sex": sex,
			"yaoi": yaoi
		}
		if username:
			data["username"] = username
		return requests.put(
			f"{self.api}/api/users/current/",
			data=data,
			headers=self.headers).json()

	def get_report_reasons(self) -> dict:
		return requests.get(
			f"{self.api}/api/reports/?get=reasons&type=title",
			headers=self.headers).json()

	def send_report(
			self,
			message: str,
			reason: int,
			title_id: int,
			type: str = "title") -> dict:
		data = {
			"message": message,
			"reason": reason,
			"target": title_id,
			"type": type
		}
		return requests.post(
			f"{self.api}/panel/api/reports/",
			data=data,
			headers=self.headers).json()

	def like_comment(
			self,
			comment_id: int,
			type: int = 0) -> dict:
		data = {
			"comment": comment_id,
			"type": type
		}
		return requests.post(
			f"{self.api}/api/activity/votes/",
			data=data,
			headers=self.headers).json()

	def get_genres(self) -> dict:
		return requests.get(
			f"{self.api}/api/forms/titles/?get=genres",
			headers=self.headers).json()

	def get_title_info(self, title: str) -> dict:
		return requests.get(
			f"{self.api}/api/titles/{title}/",
			headers=self.headers).json()

	def get_title_chapters(self, branch_id: int) -> dict:
		return requests.get(
			f"{self.api}/api/titles/chapters/?branch_id={branch_id}",
			headers=self.headers).json()

	def get_title_comments(
			self,
			title_id: int,
			page: int = 1,
			ordering: str = "-id") -> dict:
		data = {
			"title_id": title_id,
			"page": page,
			"ordering": ordering
		}
		return requests.get(
			f"{self.api}/api/activity/comments/?title_id={title_id}&page={page}&ordering={ordering}",
			data=data,
			headers=self.headers).json()

	def get_user_info(self, user_id: str) -> dict:
		return requests.get(
			f"{self.api}/api/users/{user_id}",
			headers=self.headers).json()

	def get_notifications(
			self,
			count: int = 30,
			page: int = 1,
			status: int = 0,
			type: int = 0) -> dict:
		return requests.get(
			f"{self.api}/api/users/notifications/?count={count}&page={page}&status={status}&type={type}",
			headers=self.headers).json()

	def get_notifications_count(self) -> dict:
		return requests.get(
			f"{self.api}/api/users/notifications/count/",
			headers=self.headers).json()

	def get_account_info(self) -> dict:
		return requests.get(
			f"{self.api}/api/users/current/",
			headers=self.headers).json()

	def get_daily_top_titles(self, count: int = 5) -> dict:
		return requests.get(
			f"{self.api}/api/titles/daily-top/?count={count}",
			headers=self.headers).json()

	def get_titles_last_chapters(
			self,
			page: int = 1,
			count: int = 5) -> dict:
		return requests.get(
			f"{self.api}/api/titles/last-chapters/?page={page}&count={count}",
			headers=self.headers).json()

	def add_to_bookmarks(
			self,
			title_id: int,
			type: int) -> dict:
		"""
		BOOKMARK-TYPES:
			0 - READING,
			1 - WILL READ,
			2 - HAS READ,
			3 - ABANDONED,
			4 - POSTPONED,
			5 - NOT INTERESTING
		"""
		data = {
			"mangaId": title_id,
			"title": title_id,
			"type": type
		}
		return requests.post(
			f"{self.api}/api/users/bookmarks/",
			data=data,
			headers=self.headers).json()

	def change_password(
			self,
			old_password: str,
			new_password: str) -> dict:
		data = {
			"old_password": old_password,
			"confirm_password": new_password,
			"password": new_password
		}
		return requests.put(
			f"{self.api}/api/users/current/",
			data=data,
			headers=self.headers).json()

	def bill_promo_code(self, promo_code: str) -> dict:
		data = {
			"promo_code": promo_code
		}
		return requests.post(
			f"{self.api}/api/billing/promo-codes/",
			data=data,
			headers=self.headers).json()

	def create_publishers(
			self,
			name: str,
			vk_url: str) -> dict:
		data = {
			"name": name,
			"vk": vk_url
		}
		return requests.post(
			f"{self.api}/api/publishers/",
			data=data,
			headers=self.headers).json()

	def rate_title(
			self,
			title_id: int,
			rating: int = 10) -> dict:
		data = {
			"rating": rating,
			"title": title_id
		}
		return requests.post(
			f"{self.api}/api/activity/ratings/",
			data=data,
			headers=self.headers).json()

	def like_chapter(
			self,
			chapter_id: int,
			type: int = 0) -> dict:
		data = {
			"chapter": chapter_id,
			"type": type
		}
		return requests.post(
			f"{self.api}/api/activity/votes/",
			data=data,
			headers=self.headers).json()

	def get_categories(self) -> dict:
		return requests.get(
			f"{self.api}/api/forms/titles/?get=categories",
			headers=self.headers).json()

	def get_age_limits(self) -> dict:
		return requests.get(
			f"{self.api}/api/forms/titles/?get=age_limit",
			headers=self.headers).json()

	def get_types(self) -> dict:
		return requests.get(
			f"{self.api}/api/forms/titles/?get=types",
			headers=self.headers).json()

	def get_statuses(self) -> dict:
		return requests.get(
			f"{self.api}/api/forms/titles/?get=status",
			headers=self.headers).json()

	def get_user_bookmarks(
			self,
			type: int,
			user_id: int,
			page: int = 1) -> dict:
		return requests.get(
			f"{self.api}/api/users/{user_id}/bookmarks/?ordering=-chapter_date&page={page}&type={type}",
			headers=self.headers).json()

	def get_user_history(
			self,
			user_id: int,
			page: int = 1) -> dict:
		return requests.get(
			f"{self.api}/api/users/{user_id}/history/?page={page}",
			headers=self.headers).json()

	def get_social_notifications(
			self,
			count: int = 30,
			page: int = 1) -> dict:
		return requests.get(
			f"{self.api}/api/users/notifications/?count={count}&page={page}&status=0&type=1",
			headers=self.headers).json()

	def get_important_notifications(
			self,
			count: int = 30,
			page: int = 1) -> dict:
		return requests.get(
			f"{self.api}/api/users/notifications/?count={count}&page={page}&status=0&type=2",
			headers=self.headers).json()
