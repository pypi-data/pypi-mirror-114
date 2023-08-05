from .avocent_request import AvocentRequest
from ..errors import ResponseParseError
from ..models import PduOutletsResult, PduOutlet, PduPortStatus

class PduOutletsRequest(AvocentRequest):
	sid = ""
	pdu = ""

	def __init__(self, sid, pdu):
		super().__init__()
		self.sid = sid
		self.pdu = pdu

	def get_body(self):
		str = '<avtrans><sid>{}</sid><action>get</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.powermanagement.pdu_management.pduDevicesDetails.outletTable</path><pathvar>{}</pathvar></paths></avtrans>'
		return str.format(self.sid, self.pdu)

	def parse_response(self, xml):
		root_section = xml.find("./payload/section")
		if root_section is None:
			raise ResponseParseError("Can't find parent section array in xml response")

		outlets = []

		for outlet_xml in root_section.findall("./array"):
			outlet_number = int(outlet_xml.find("./parameter[@id='outlet_number']/value").text)
			outlet_name = outlet_xml.find("./parameter[@id='outlet_name']/value").text
			outlet_status = PduPortStatus(outlet_xml.find("./parameter[@id='status']/value").text)
			outlet_current = float(outlet_xml.find("./parameter[@id='outlet_current']/value").text)
			outlet_power = float(outlet_xml.find("./parameter[@id='outlet_power']/value").text)

			outlets.append(PduOutlet(outlet_number, outlet_name, outlet_status, outlet_current, outlet_power))

		return PduOutletsResult(outlets)
