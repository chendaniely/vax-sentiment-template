"""This script takes a CSV file and converts it into a .net and .gml file

This script should be called form the root project directory
not from the src directory
"""

import pandas as pd
import numpy as np
import networkx as nx
from copy import deepcopy
import sys
import matplotlib.pyplot as plt
from glob import glob
import os

fileName = sys.argv[1]


def getFiles(fileName):
    matches = glob('*'+fileName+'*')
    bigFile = matches[0]
    data = pd.DataFrame.from_csv(bigFile)
    return clearSource(data)


def clearSource(data):
    columns = ['source','target']
    pre = len(data)
    for column in columns:
        data = data[pd.notnull(data[column])]
    post = len(data)
    print "Filtered %s rows to %s rows by removing rows with blank values in columns %s" % (pre,post,columns)
    return data


def getStuff(data,labels):
    forEdges = labels == ['edge']
    columns = list(data.columns.values)
    items = dict()

    nameFunc = {True: lambda x,y: '%s - %s - %s' % (x['source'],x['edge'],x['target']),
                False: lambda x,y: x[y]}[forEdges]

    extra = ['source','target'] * forEdges

    for label in labels:
        relevant = [col for col in columns if label+'-' in col] + extra
        print "Extracting %s data from %s" % (label,relevant)
        for i in data.index:
            row = data.ix[i]
            for col in relevant:
                if str(row[col]).lower() != 'nan':
                    name = nameFunc(row,label)
                    if name not in items:
                        items[name] = dict()
                    items[name][col.replace(label+'-','')] = row[col]
    return items

def getNodes(data):
    return getStuff(data,['source','target'])


def getEdges(data):
    return getStuff(data,['edge'])


def addNodes(graph,nodes):
    for key,value in nodes.iteritems():
        graph.add_node(key,attr_dict=value)
    return graph

def addEdges(graph,edges):
    for key,value in edges.iteritems():
        value['label'] = key
        value['edge'] = key.split(' - ')[1]
        graph.add_edge(value['source'],value['target'],attr_dict = value)
    return graph

def createNetwork(edges,nodes):
    graph = nx.MultiDiGraph()
    graph = addNodes(graph,nodes)
    graph = addEdges(graph,edges)
    return graph


def drawIt(graph,what='graph'):
    style=nx.spring_layout(graph)
    size = graph.number_of_nodes()
    print "Drawing %s of size %s:" % (what,size)
    if size > 20:
        plt.figure(figsize=(10,10))
        if size > 40:
            nx.draw(graph,style,node_size=60,font_size=8)
        else:
            nx.draw(graph,style)
    else:
        nx.draw(graph,style)
    plt.show()


def getGraph(fileRef):
    data = getFiles(fileName)
    nodes = getNodes(data)
    edges = getEdges(data)
    graph = createNetwork(edges, nodes)

    gml_output_path = os.path.join('output', 'network',
                                   fileRef.
                                   split('.')[0].
                                   split('/')[1] + '.gml')

    print "Writing GML file to %s" % gml_output_path
    nx.write_gml(graph, gml_output_path)

    net_output_path = os.path.join('output', 'network',
                                   fileRef.
                                   split('.')[0].
                                   split('/')[1] + '.net')

    print "Writing net file to %s" % net_output_path
    nx.write_pajek(graph, net_output_path)

    params = (graph.number_of_nodes(), graph.number_of_edges())
    print "Graph has %s nodes, %s edges" % params
    print


getGraph(fileName)
