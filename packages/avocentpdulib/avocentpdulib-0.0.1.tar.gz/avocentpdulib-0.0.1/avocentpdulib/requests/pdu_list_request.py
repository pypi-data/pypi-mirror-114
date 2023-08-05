from .avocent_request import AvocentRequest
from ..errors import ResponseParseError
from ..models import PduListResult, PduInfo, PduPortInfo, PduPortStatus

class PduListRequest(AvocentRequest):
	sid = ""

	def __init__(self, sid):
		super().__init__()
		self.sid = sid

	def get_body(self):
		str = '<avtrans><sid>{}</sid><action>get</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.topology</path></paths></avtrans>'
		return str.format(self.sid)

	def parse_response(self, xml):
		root_section = xml.find("./payload/section/array")
		if root_section is None:
			raise ResponseParseError("Can't find parent section array in xml response")

		pdus = []

		for pdu_xml in root_section.findall("./array"):
			pdu_name = pdu_xml.find("./parameter[@id='name']/value")
			if pdu_name is None:
				raise ResponseParseError("Missing name from pdu")

			pdu_type = pdu_xml.find("./parameter[@id='type']/value")
			ports = []

			for port_xml in pdu_xml.findall("./array"):
				port_name = port_xml.find("./parameter[@id='name']/value")
				if port_name is None:
					continue

				port_id = port_xml.find("./parameter[@id='port']/value")
				port_status = PduPortStatus(port_xml.find("./parameter[@id='status']/value").text)
				ports.append(PduPortInfo(port_name.text, port_id.text, port_status))

			pdus.append(PduInfo(pdu_name.text, pdu_type.text, ports))

		return PduListResult(pdus)
