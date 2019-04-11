from datetime import datetime
from rdflib import URIRef, Literal, Namespace
from rdflib.namespace import RDF, OWL
from pyproms.prov_agent import ProvAgent
from pyproms.prov_entity import ProvEntity
from pyproms.owlclass import OwlClass


class LsutechProduct(OwlClass):
	def __init__(self,
				label,
				uri=None,
				blockchainuri=None,
				comment=None,
				wasAttributedTo=None,
				value=None,
				scanTime=None):
		OwlClass.__init__(self,
							label,
							uri,
							blockchainuri,
							comment
							)
		if wasAttributedTo:
			self.__set_wasAttributedTo(wasAttributedTo)
		else:
			self.wasAttributedTo = None

		if value:
			self.__set_value(value)
		else:
			self.value = None
		self.scanTime = scanTime if scanTime else datetime.strptime("2071-01-01T00:00:00","%Y-%m-%dT%H:%M:%S")
	def set_blockchainuri(self,blockchainuri):
		self.blockchainuri = blockchainuri

	def get_blockchainuri(self):
		return self.blockchainuri

	def __set_wasAttributedTo(self, wasAttributedTo):
		if type(wasAttributedTo) is ProvAgent:
			self.wasAttributedTo = wasAttributedTo
		else:
			raise TypeError('wasAttributedTo must be an Agent, not a %s' % type(wasAttributedTo))

	def __set_value(self, value):
		if (type(value) is str or
				type(value) is float or
				type(value) is int or
				type(value) is datetime.datetime):
					self.value = value
		else:
			raise TypeError('Entity \'value\' must be a string, int, float or datetime, not a %s' % type(value))

	def make_graph(self):
		OwlClass.make_graph(self)

		PROV = Namespace('http://www.w3.org/ns/prov#')
		XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
		LSUTECH = Namespace("http://www.lsutech.com#")

		self.g.remove((
			URIRef(self.uri),
			RDF.type,
			OWL.Class))
		self.g.add((URIRef(self.uri),
					RDF.type,
					PROV.Entity))
		if self.wasAttributedTo:
			self.g = self.g + self.wasAttributedTo.get_graph()
			self.g.add((
				URIRef(self.uri),
				PROV.wasAttributedTo,
				URIRef(self.wasAttributedTo.uri)))
		if self.value:
			if type(self.value) is datetime.datetime:
				self.g.add((URIRef(self.uri),
							PROV.value,
							Literal(self.value, datatype=XSD.dateTime)))
			elif type(self.value) is int:
				self.g.add((URIRef(self.uri),
							PROV.value,
							Literal(self.value, datatype=XSD.integer)))
			elif type(self.value) is float:
				self.g.add((URIRef(self.uri),
							PROV.value,
							Literal(self.value, datatype=XSD.float)))
			else:  # string
				self.g.add((URIRef(self.uri),
							PROV.value,
							Literal(self.value, datatype=XSD.string)))
		if self.scanTime:		
			self.g.add((URIRef(self.uri),
						PROV.scanTime,
						Literal(self.scanTime.strftime("%Y-%m-%dT%H:%M:%S"), 
								datatype=XSD.dateTime)))
		if self.blockchainuri:
			self.g.add((URIRef(self.uri),
				LSUTECH.blockchainuri,
				URIRef(self.blockchainuri)
				))

	def get_graph(self):
		if not self.g:
			self.make_graph()
		return self.g
