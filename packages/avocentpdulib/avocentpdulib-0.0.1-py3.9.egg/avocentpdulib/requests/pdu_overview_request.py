from .avocent_request import AvocentRequest
from ..errors import ResponseParseError
from ..models import PduOverviewResult, PduOverviewEntry, PduScope

class PduOverviewRequest(AvocentRequest):
	sid = ""
	pdu = ""

	def __init__(self, sid, pdu):
		super().__init__()
		self.sid = sid
		self.pdu = pdu

	def get_body(self):
		str = '<avtrans><sid>{}</sid><action>get</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.powermanagement.pdu_management.pduDevicesDetails.pduDevicesOverviewSettings</path><pathvar>{}</pathvar></paths></avtrans>'
		return str.format(self.sid, self.pdu)

	def parse_response(self, xml):
		root_section = xml.find("./payload/section")
		if root_section is None:
			raise ResponseParseError("Can't find parent section array in xml response")

		entries = []

		for entry_xml in root_section.findall("./array"):
			entry_scope = PduScope(entry_xml.find("./parameter[@id='scope']/value").text)
			entry_name = entry_xml.find("./parameter[@id='cID']/value").text
			entry_current = float(entry_xml.find("./parameter[@id='cValue']/value").text)
			entry_voltage = int(entry_xml.find("./parameter[@id='vValue']/value").text)
			entry_power = float(entry_xml.find("./parameter[@id='pcValue']/value").text)
			entry_power_factor = float(entry_xml.find("./parameter[@id='pcPowerFactor']/value").text)
			entry_kwh = float(entry_xml.find("./parameter[@id='cpValue']/value").text)

			entries.append(PduOverviewEntry(entry_scope, entry_name, entry_current, entry_voltage, entry_power, entry_power_factor, entry_kwh))

		return PduOverviewResult(entries)
