# AgentSpeakProperties
Tool for assessing software properties of AgentSpeak code

Goals of this work: 

Item 1: use a less subjective and ideally more quantifiable approach at
measuring coupling and cohesion in AgentSpeak code, to support the
rankings we have;

Item 2: be clearer about how the graphs for cyclomatic complexity are
obtained. If these can be generated automatically from code instead of
hand drawn, or at least if we're following a strict algorithm for
drawing them, we are being a lot more objective and we are making a
contribution there;


What to do:

Item 1: Coupling and Cohesion: Reproducibility of the ranking.
	
  - Perhaps put it in a pseudo code style, diagram, or equation (for example)
  - More explicit and systematic - makes it more useful for others to use

Item 2: How does one go from code to the graphs?
	
  - Write out the proceedure
  - Example: the first node is the selection of which option, then they are all the different plans that implement each of the plans for that option. 
  - Steps: 
    - Write in English,
    - write in pseudocode, 
		- write in python, 
		- generate graphviz and report
		- Perhaps use compilation type tools such as Lex, Yak, Bison
			- Lex - more about the syntax
			- Yak - specify rules
			- Bison - modern version of Yak
			- Map patterns to other patterns using the EBNF
