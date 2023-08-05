from .avocent_request import AvocentRequest
from ..errors import ResponseParseError
from ..models import OutletAction, PduOutletsResult, PduOutlet, PduPortStatus

class OutletActionRequest(AvocentRequest):
	sid = ""
	pdu = ""
	outlet_number = 0
	action = OutletAction.TURN_ON

	def __init__(self, sid, pdu, outlet_number, action):
		super().__init__()
		self.sid = sid
		self.pdu = pdu
		self.outlet_number = outlet_number
		self.action = action

	def get_body(self):
		strings = {
			OutletAction.TURN_ON: '<avtrans><sid>{}</sid><action>on</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.powermanagement.pdu_management.pduDevicesDetails.outletTable.Nazca_outlet_table</path><pathvar>{}</pathvar></paths><payload><section structure="table" id="outlet_details"><array id="{}"></array></section></payload></avtrans>',
			OutletAction.TURN_OFF: '<avtrans><sid>{}</sid><action>off</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.powermanagement.pdu_management.pduDevicesDetails.outletTable.Nazca_outlet_table</path><pathvar>{}</pathvar></paths><payload><section structure="table" id="outlet_details"><array id="{}"></array></section></payload></avtrans>',
			OutletAction.POWER_CYCLE: '<avtrans><sid>{}</sid><action>cycle</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.powermanagement.pdu_management.pduDevicesDetails.outletTable.Nazca_outlet_table</path><pathvar>{}</pathvar></paths><payload><section structure="table" id="outlet_details"><array id="{}"></array></section></payload></avtrans>'
		}

		str = strings[self.action]
		return str.format(self.sid, self.pdu, self.outlet_number)

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
