# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 15:37:33 2017

@author: canggih
"""

import pydot
import requests
from bs4 import BeautifulSoup

class MathGenealogy:
    # the source of the data
    baseURL = "https://www.genealogy.math.ndsu.nodak.edu/id.php?id="
        
    def find_ancestors(self,personID,personName):
        self._dictPair = []
        self._dictName = []
        
        # _dictName contains the ID and the name
        self._dictName.append([personID,personName])
        
        # Recursive function to get the ancestors
        self.parse_ancestors(personID)
        
        
        self._dictName = [list(t) for t in set(tuple(element) for element in self._dictName)]
        self._dictId = [i[0] for i in self._dictName]
        
        # _dictPair contains person ID and one ID of his/her ancestor
        self._dictPair = [list(t) for t in set(tuple(element) for element in self._dictPair)]      
        
        
        dictPairName = []
        for d in self._dictPair:
            x = self._dictName[self._dictId.index(d[0])][1]
            y = self._dictName[self._dictId.index(d[1])][1]
            dictPairName.append([x,y])
        
        self.draw_ancestors(personID,dictPairName)
        
        
    def parse_ancestors(self,idAncestor):
        getData = requests.get(self.baseURL + idAncestor)
        parseRaw = BeautifulSoup(getData.text,"html.parser")
        	
        ancData = parseRaw.select("#paddingWrapper > p")[1].findAll("a")
        	
        if ancData != None:
        	for ancDatum in ancData:
        		ancId = ancDatum["href"].split("=")[1]
        		ancName = ancDatum.string
        		self._dictName.append([ancId,ancName])
        		self._dictPair.append([ancId,idAncestor])
        		self.parse_ancestors(ancId)
          
    def draw_ancestors(self,fileName,pairName):
        graph = pydot.Dot(graph_type='digraph')
        
        for edge in pairName:
            nodea = pydot.Node(edge[0])
            nodeb = pydot.Node(edge[1])
            graph.add_node(nodea)
            graph.add_node(nodeb)
            graph.add_edge(pydot.Edge(nodea,nodeb))
            
        graph.write(fileName + ".png",format="png")