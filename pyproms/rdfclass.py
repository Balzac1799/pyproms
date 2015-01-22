from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import RDF, RDFS
import uuid


class RdfClass:
    def __init__(self,
                 label,
                 uri=None,
                 comment=None):
        self.g = None
        self.label = label
        if uri:
            self.uri = uri
        else:
            self.uri = 'http://placeholder.org#' + str(uuid.uuid4())
        self.comment = comment

    def set_uri(self, uri):
        self.uri = uri

    def set_comment(self, comment):
        self.comment = comment

    def make_graph(self):
        self.g = Graph()

        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    RDFS.Class))

        if self.uri:
            self.g.add((URIRef(self.uri),
                        RDFS.label,
                        Literal(self.label, datatype=XSD.string)))

        if self.comment:
            self.g.add((URIRef(self.uri),
                        RDFS.comment,
                        Literal(self.comment, datatype=XSD.string)))

    def get_graph(self):
        """
        Generates the RDF graph of this class

        :return: This class's RDF graph
        """
        if not self.g:
            self.__make_graph()

        return self.g

    def serialize_graph(self, format='turtle'):
        return self.get_graph().serialize(format=format)