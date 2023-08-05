from .avocent_request import AvocentRequest
from ..models import LoginResult

class LoginRequest(AvocentRequest):
	username = ""
	password = ""

	def __init__(self, username, password):
		super().__init__()
		self.username = username
		self.password = password

	def get_body(self):
		str = '<avtrans><sid></sid><action>login</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.topology</path></paths><payload><section structure="login"><parameter id="username" structure="RWtext"><value>{}</value></parameter><parameter id="password" structure="password"><value>{}</value></parameter></section></payload></avtrans>'
		return str.format(self.username, self.password)

	def parse_response(self, xml):
		if xml.find(".//error") is not None:
			return LoginResult(False, "")

		sid = xml.find(".//sid")
		return LoginResult(True, sid.text)
