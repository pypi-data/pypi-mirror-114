from .models.login_result import LoginResult
from .requests.avocent_request import AvocentRequest
from .requests.login_request import LoginRequest
from .requests.pdu_list_request import PduListRequest
from .requests.pdu_outlets_request import PduOutletsRequest
from .requests.pdu_overview_request import PduOverviewRequest
from .requests.pdu_total_power_request import PduTotalPowerRequest, PduTotalPowerResult
from .requests.outlet_action_request import OutletActionRequest
from .models.outlet_action import OutletAction
from .models.login_result import LoginResult
from .models.pdu_list_result import PduListResult
from .models.pdu_outlets_result import PduOutletsResult
from .models.pdu_overview_result import PduOverviewResult
from .models.pdu_total_power_result import PduTotalPowerResult
from .errors import AuthenticationError

import defusedxml.ElementTree as ET
import urllib3
import aiohttp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AvocentPdu:
	host = "https://192.168.0.0"
	username = ""
	password = ""
	endpoint = "/appliance/avtrans"

	sid = ""
	http_session = None

	def __init__(self, host, username, password, endpoint="/appliance/avtrans", verify_ssl=False):
		self.host = host
		self.username = username
		self.password = password
		self.endpoint = endpoint
		self.http_session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=verify_ssl))

	async def close(self):
		return await self.http_session.close()

	async def login(self) -> LoginResult:
		req = LoginRequest(self.username, self.password)
		result = await self._do_request(req, relogin_on_failure=False)
		if result.successful:
			self.sid = result.sid
		return result

	async def list_pdus(self) -> PduListResult:
		self._ensure_authenticated()
		req = PduListRequest(self.sid)
		return await self._do_request(req)

	async def get_pdu_outlets(self, pdu) -> PduOutletsResult:
		self._ensure_authenticated()
		req = PduOutletsRequest(self.sid, pdu)
		return await self._do_request(req)

	async def get_pdu_overview(self, pdu) -> PduOverviewResult:
		self._ensure_authenticated()
		req = PduOverviewRequest(self.sid, pdu)
		return await self._do_request(req)

	async def get_pdu_total_powers(self, pdu) -> PduTotalPowerResult:
		self._ensure_authenticated()
		req = PduTotalPowerRequest(self.sid, pdu)
		return await self._do_request(req)

	async def send_outlet_action(self, pdu, outlet_number, action: OutletAction) -> PduOutletsResult:
		self._ensure_authenticated()
		req = OutletActionRequest(self.sid, pdu, outlet_number, action)
		return await self._do_request(req)

	def _ensure_authenticated(self):
		if self.sid == "":
			raise AuthenticationError("Authentication is required to use methods.")

	async def _do_request(self, request: AvocentRequest, relogin_on_failure = True):
		body = request.get_body()
		async with self.http_session.post(self.host + self.endpoint, data=body) as response:
			content = (await response.text()).encode()
			response.raise_for_status()

			if relogin_on_failure and b"<payload structure=\"login\">" in content:
				result = await self.login()
				if not result.successful:
					raise AuthenticationError("Suddently the authentication with avocent failed. Have the credentials been changed?")
				if hasattr(request, "sid"):
					request.sid = self.sid
				return await self._do_request(request, relogin_on_failure=False)

			return self._parse_response(request, content)

	def _parse_response(self, request, content):
		xml_root = ET.fromstring(content, forbid_dtd=True, forbid_entities=True, forbid_external=True)
		return request.parse_response(xml_root)
