from pyproms.utils import HashValue
from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import RDF, RDFS, OWL



class OwlClass(object):
    """
    This class creates generic RDF classes that require only an rdfs:label
    property to be specified. It is mostly used by inheritance to produce
    specialised RDF classes, such as Report or Entity.
    """
    def __init__(self,
                 label,
                 uri=None,
                 blockchainuri=None,
                 comment=None):
        self.g = None
        self.label = label
        self.comment = comment
        self.blockchainuri = blockchainuri
        if uri:
            self.uri = uri
        else:
            self.uri = 'http://www.lsutech.com#' + str(HashValue("%(label)s#%(cmt)s#%(blcu)s"%{"blcu":self.blockchainuri if self.blockchainuri else "",
                "label":self.label,
                "cmt":self.comment}))


    def set_uri(self, uri):
        self.uri = uri

    def set_comment(self, comment):
        self.comment = comment

    def make_graph(self):
        """
        Constructs an RDF graph for this class using its instance variables

        :return: an rdflib Graph object
        """
        self.g = Graph()

        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        LSUTECH = Namespace("http://www.lsutech.com/#")

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    OWL.Class))

        self.g.add((URIRef(self.uri),
                    RDFS.label,
                    Literal(self.label, datatype=XSD.string)))

        if self.comment:
            self.g.add((URIRef(self.uri),
                        RDFS.comment,
                        Literal(self.comment, datatype=XSD.string)))
        if self.blockchainuri:
            self.g.add((URIRef(self.blockchainuri),
                        LSUTECH.blockchainuri,
                        OWL.Class
                        ))

    def get_graph(self):
        """
        Generates the RDF graph of this class

        :return: This class's RDF graph
        """
        if not self.g:
            self.make_graph()

        return self.g

    def serialize_graph(self, format='turtle'):
        return self.get_graph().serialize(format=format)
