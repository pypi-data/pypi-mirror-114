from abc import ABC, abstractmethod

class AvocentRequest(ABC):

	@abstractmethod
	def get_body(self):
		pass

	@abstractmethod
	def parse_response(self, xml):
		pass
