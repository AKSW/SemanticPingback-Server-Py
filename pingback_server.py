#!/usr/bin/env python3

from flask import Flask
from flask_cors import CORS
from flask import g
from flask import request
from flask import render_template

import rdflib
from semanticpingback import SemanticPingbackReceiver

import logging

class default_settings():
    GRAPH_FILE = "links.ttl"

app = Flask(__name__)
app.config.from_object('pingback_server.default_settings')
app.config.from_envvar('PINGBACK_SERVER_SETTINGS', silent=True)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def pingback():
    success = None

    if request.method == 'POST':
        sp = SemanticPingbackReceiver()

        links = sp.receivePing(request=request)

        if len(links):
            success = True
        else :
            success = False

        graph = get_graph()
        graph += links
        write_graph()

    graph = get_graph()
    triples = graph.triples((None, None, None))

    if 'ENDPOINT_URL' in app.config:
        endpointurl = app.config['ENDPOINT_URL']
    else:
        endpointurl = request.host_url

    return render_template('start.html', links=triples, success=success,
                           endpointurl=endpointurl)

def get_graph():
    graph = getattr(g, '_graph', None)
    if graph is None:
        graph = rdflib.Graph()
        graph.parse(app.config['GRAPH_FILE'], format="turtle")
        g._graph = graph
    return graph

def write_graph(graph=None):
    if graph is None:
        graph = getattr(g, '_graph', None)
    graph.serialize(app.config['GRAPH_FILE'], format="turtle")

@app.teardown_appcontext
def close_connection(exception):
    graph = getattr(g, '_graph', None)
    if graph is not None:
        write_graph(graph)
        graph.close()
