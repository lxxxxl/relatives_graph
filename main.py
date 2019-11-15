#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from orm_defs import Base, Relative

import sys
import networkx as nx
import matplotlib.pyplot as plt


class RelativesController:
# ORM related vars
	session = None
	engine = None
	graph = None
# ################# 
    
	def __init__(self, db_connection_string):
		self.engine = create_engine(db_connection_string)
		Base.metadata.create_all(self.engine)
		self.graph = nx.Graph()
		

	def get_session(self):
		if self.session == None:
			self.session = scoped_session(sessionmaker(bind=self.engine))
		return self.session    
        
	def commit(self):
		self.get_session().commit()
####################

	def processDescendants(self, parent, generationIndex):
		for descendant in parent.descendants:
			self.graph.add_node(descendant,name=descendant.name)
			self.graph.add_edge(parent, descendant, weight=4.7)
			self.processDescendants(descendant, generationIndex+1)
			
	def loadRelatives(self):
		allRelatives = self.get_session().query(Relative).all()
		for relative in allRelatives:
			if relative.parents.count() == 0:
				self.graph.add_node(relative)
				self.processDescendants(relative,1)
		
		
		nx.draw(self.graph,with_labels=True, 
		width=5, edge_color='skyblue', 				# edge setup
		font_size=9, node_size=4500, node_shape='s', node_color='lightblue') # node setup
		#plt.savefig("path.png")
		plt.show()
		


def main():
	relativesController = RelativesController('sqlite:///database.db') 
	relativesController.loadRelatives()

main()
