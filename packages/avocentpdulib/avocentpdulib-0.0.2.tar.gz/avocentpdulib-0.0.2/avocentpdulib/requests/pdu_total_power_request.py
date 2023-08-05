from .avocent_request import AvocentRequest
from ..errors import ResponseParseError
from ..models import PduTotalPowerResult, PduTotalPowerEntry, PduScope
from datetime import datetime

class PduTotalPowerRequest(AvocentRequest):
	sid = ""
	pdu = ""

	def __init__(self, sid, pdu):
		super().__init__()
		self.sid = sid
		self.pdu = pdu

	def get_body(self):
		str = '<avtrans><sid>{}</sid><action>get</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.powermanagement.pdu_management.pduDevicesDetails.cp_section</path><pathvar>{}</pathvar></paths></avtrans>'
		return str.format(self.sid, self.pdu)

	def parse_response(self, xml):
		root_section = xml.find("./payload/section")
		if root_section is None:
			raise ResponseParseError("Can't find parent section array in xml response")

		entries = []

		for entry_xml in root_section.findall("./array"):
			entry_scope = PduScope(entry_xml.find("./parameter[@id='scope']/value").text)
			entry_name = entry_xml.find("./parameter[@id='cpID']/value").text
			entry_start_time = entry_xml.find("./parameter[@id='cpStartTime']/value").text
			entry_kwh = float(entry_xml.find("./parameter[@id='cpValue']/value").text)

			entry_start_time_parsed = None
			try:
				entry_start_time_parsed = datetime.strptime(entry_start_time, "%Y-%m-%d %H:%M:%S")
			except ValueError:
				print("Can't parse {}".format(entry_start_time))

			entries.append(PduTotalPowerEntry(entry_scope, entry_name, entry_start_time_parsed, entry_kwh))

		return PduTotalPowerResult(entries)
