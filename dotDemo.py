# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 21:05:10 2022

@author: Patrick
"""

import graphviz

dot = graphviz.Digraph(comment='The Round Table')
dot  #doctest: +ELLIPSIS

dot.node('A', 'King Arthur')  # doctest: +NO_EXE
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')

print(dot.source)

dot.render('doctest-output/round-table.gv', view=True)