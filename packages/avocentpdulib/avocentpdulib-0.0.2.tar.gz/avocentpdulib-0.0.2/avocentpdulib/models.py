from enum import Enum
from typing import List
from datetime import datetime

class LoginResult:
	def __init__(self, successful: bool, sid: str):
		self.successful = successful
		self.sid = sid

class OutletAction(Enum):
	TURN_ON = 0
	TURN_OFF = 1
	POWER_CYCLE = 2

class PduPortStatus(Enum):
	ON = "ON"
	OFF = "OFF"

class PduScope(Enum):
	PDU = "pdu"
	BANK = "circuit"
	OUTLET = "outlet"

class PduPortInfo:
	def __init__(self, name: str, portid: int, status: PduPortStatus):
		self.name = name
		self.portid = portid
		self.status = status

class PduInfo:
	def __init__(self, name: str, model: str, ports: List[PduPortInfo]):
		self.name = name
		self.model = model
		self.ports = ports

class PduListResult:
	def __init__(self, pdus: List[PduInfo]):
		self.pdus = pdus

class PduOutlet:
	def __init__(self, number: int, name: str, status: PduPortStatus, current: float, power: float):
		self.number = number
		self.name = name
		self.status = status
		self.current = current
		self.power = power

class PduOutletsResult:
	def __init__(self, outlets: List[PduOutlet]):
		self.outlets = outlets

class PduOverviewEntry:
	def __init__(self, scope: PduScope, name: str, current: float, voltage: int, power: float, power_factor: float, total_kwh: float):
		self.scope = scope
		self.name = name
		self.current = current
		self.voltage = voltage
		self.power = power
		self.power_factor = power_factor
		self.total_kwh = total_kwh

class PduOverviewResult:
	def __init__(self, entries: List[PduOverviewEntry]):
		self.entries = entries

class PduSystemInfoResult:
	serial_number: str = ""
	model_number: str = ""
	bootcode_version: str = ""
	firmware_version: str = ""
	booted_from: str = ""
	cpu_model: str = ""
	cpu_revision: str = ""
	cpu_bogomips: str = ""

class PduTotalPowerEntry:
	def __init__(self, scope: PduScope, name: str, start_time: datetime, total_kwh: float):
		self.scope = scope
		self.name = name
		self.start_time = start_time
		self.total_kwh = total_kwh

class PduTotalPowerResult:
	def __init__(self, entries: List[PduTotalPowerEntry]):
		self.entries = entries
