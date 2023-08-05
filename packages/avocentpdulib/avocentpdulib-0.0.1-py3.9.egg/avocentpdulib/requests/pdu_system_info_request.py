from .avocent_request import AvocentRequest
from ..errors import ResponseParseError
from ..models import PduOverviewResult, PduOverviewEntry, PduScope, PduSystemInfoResult

class PduSystemInfoRequest(AvocentRequest):
	sid = ""

	def __init__(self, sid):
		super().__init__()
		self.sid = sid

	def get_body(self):
		str = '<avtrans><sid>{}</sid><action>get</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.applianceSettings.information</path></paths></avtrans>'
		return str.format(self.sid)

	def parse_response(self, xml):
		root_section = xml.find("./payload/section")
		if root_section is None:
			raise ResponseParseError("Can't find parent section array in xml response")

		info = PduSystemInfoResult()

		info.serial_number = root_section.find("./parameter[@id='identity']/parameter[@id='serialnumber']/value").text
		info.model_number = root_section.find("./parameter[@id='identity']/parameter[@id='modelnumber']/value").text
		info.bootcode_version = root_section.find("./parameter[@id='version']/parameter[@id='bootcodeversion']/value").text
		info.firmware_version = root_section.find("./parameter[@id='version']/parameter[@id='firmwareversion']/value").text
		info.booted_from = root_section.find("./parameter[@id='version']/parameter[@id='bootedFrom']/value").text
		info.cpu_model = root_section.find("./parameter[@id='cpuinfo']/parameter[@id='cpu']/value").text
		info.cpu_revision = root_section.find("./parameter[@id='cpuinfo']/parameter[@id='revision']/value").text
		info.cpu_bogomips = root_section.find("./parameter[@id='cpuinfo']/parameter[@id='bogomips']/value").text

		return info
