"""
A commandline tool for drawing RDF graphs in Graphviz DOT format

You can draw the graph of an RDF file directly:

.. code-block: bash

   rdf2dot my_rdf_file.rdf | dot -Tpng | display

"""

import os
import rdflib
import rdflib.extras.cmdlineutils

import re
import sys
import html
import yaml
import collections

from rdflib import XSD

LABEL_PROPERTIES = [
    rdflib.RDFS.label,
    rdflib.URIRef("http://purl.org/dc/elements/1.1/title"),
    rdflib.URIRef("http://xmlns.com/foaf/0.1/name"),
    rdflib.URIRef("http://www.w3.org/2006/vcard/ns#fn"),
    rdflib.URIRef("http://www.w3.org/2006/vcard/ns#org"),
    rdflib.URIRef("http://purl.org/dc/terms/title"),    
]

XSDTERMS = [
    XSD[x]
    for x in (
        "anyURI",
        "base64Binary",
        "boolean",
        "byte",
        "date",
        "dateTime",
        "decimal",
        "double",
        "duration",
        "float",
        "gDay",
        "gMonth",
        "gMonthDay",
        "gYear",
        "gYearMonth",
        "hexBinary",
        "ID",
        "IDREF",
        "IDREFS",
        "int",
        "integer",
        "language",
        "long",
        "Name",
        "NCName",
        "negativeInteger",
        "NMTOKEN",
        "NMTOKENS",
        "nonNegativeInteger",
        "nonPositiveInteger",
        "normalizedString",
        "positiveInteger",
        "QName",
        "short",
        "string",
        "time",
        "token",
        "unsignedByte",
        "unsignedInt",
        "unsignedLong",
        "unsignedShort",
    )
]

EDGECOLOR = "blue"
NODECOLOR = "black"
ISACOLOR = "black"


def rdf2dot(g, stream, opts=None, html_labels=True):
    """
    Convert the RDF graph to DOT
    writes the dot output to the stream
    """

    if opts in [None, []]:
        opts = {}            

    fields = collections.defaultdict(set)
    nodes = {}

    def node(x):

        if x not in nodes:
            nodes[x] = "node%d" % len(nodes)
        return nodes[x]

    def label(x, g):

        for labelProp in LABEL_PROPERTIES:
            l = g.value(x, labelProp)
            if l:
                return l

        try:
            return g.namespace_manager.compute_qname(x)[2]
        except:
            return x

    def formatliteral(l, g):
        v = html.escape(l)
        if l.datatype:
            return "&quot;%s&quot;^^%s" % (v, qname(l.datatype, g))
        elif l.language:
            return "&quot;%s&quot;@%s" % (v, l.language)
        return "&quot;%s&quot;" % v

    def qname(x, g):
        try:
            q = g.compute_qname(x)
            return q[0] + ":" + q[2]
        except:
            return x

    def default_color(p, placement='arrow'):
        color = None
        

        for fn in ["coloring.yaml", os.path.join(os.getenv("HOME"), "coloring.yaml")]:
            if os.path.exists(fn):
                break

        for k, v in yaml.load(open(fn), Loader=yaml.SafeLoader).items():
            if re.match(k, p):        
                color = v.get(placement, None)
                
                if color is not None:
                    return color

        return "black"

    color = opts.get('color', default_color)
    

    stream.write('''
            digraph { 
                node [ fontname="DejaVuSans-Oblique" ] ;
                ranksep = 1;
                startType = 0
                overlap = false;

    ''')

    for s, p, o in g:
        sn = node(s)

        if p == rdflib.RDFS.label:
            continue

        if isinstance(o, (rdflib.URIRef, rdflib.BNode)):
            on = node(o)
            if html_labels:
                stream.write(
                    f"""
                        \t{sn} -> {on} [ color={color(p, 'arrow')}, label=< <font point-size='15' 
                                        color='#666666'>{qname(p ,g)}</font> > ] ;
                    """
                )
            else:
                stream.write(
                    f"""
                        \t{sn} -> {on} [ color={color(p, 'arrow')}, label={re.sub('[^0-9a-zA-Z]', '', qname(p ,g))} ] ;
                    """
                )

        else:
            fields[sn].add((qname(p, g), formatliteral(o, g)))

    for u, n in nodes.items():
        stream.write("# %s %s\n" % (u, n))
        f = [
           f"""<tr><td align='left'><font point-size="10">{x[0]}: </font></td><td align='left'><font point-size="10">{x[1]}</font></td></tr>"""
                for x in sorted(fields[n])            
        ]

        full_uri_row =  f"""
        
              <td href='{u}' bgcolor='{color(u, 'bgcolor')}' colspan='2'>
              <font point-size='5' color='#6666ff'>{html.escape(u)}</font></td>
        """
        #TODO: control inserting it 

        #TODO: not actually color
        pos_line = ""
        if color(u, 'pos'):
            pos_line = 'pos = "' + color(u, 'pos') + '"'

        if html_labels:
            stream.write(
                re.sub("[\n ]+", " ", f"""{n} [ 
                        shape=record
                        fillcolor={color(u, 'bgcolor')}
                        style=filled color={color(u, 'node_color')} 
                        height=0.1 width=0.1 margin="0.1,0.1" 
                        {pos_line}

                        label=<  
                                <table border="0" cellpadding="2" cellspacing="1">
                                <tr>
                                    <td colspan="2" href="{u}">
                                    <font color='{color(u, 'node_label').strip()}'><B>
                                        {html.escape(label(u, g)).strip()}
                                    </B></font>
                                    </td>
                                </tr>
                                {''.join(f)}
                                </table>
                            >, tooltip = "{u}"
                        ]""")
            )        
        else:
            stream.write(
                re.sub("[\n ]+", " ", f"""{n} [ 
                        shape=box
                        fillcolor={color(u, 'bgcolor')}
                        style=filled color={color(u, 'node_color')} 
                        height=0.1 width=0.1 margin="0.1,0.1" 
                        {pos_line}

                        label={re.sub('[^0-9a-zA-Z]', '', html.escape(label(u, g)).strip())}, 
                        tooltip = "{u}"
                        ]""")
            )
        #{''.join(f)}

    stream.write("}\n")


def _help():
    sys.stderr.write(
        """
rdf2dot.py [-f <format>] files...
Read RDF files given on STDOUT, writes a graph of the RDFS schema in DOT
language to stdout
-f specifies parser to use, if not given,

"""
    )


def cli():
    rdflib.extras.cmdlineutils.main(rdf2dot, _help)


if __name__ == "__main__":
    cli()
