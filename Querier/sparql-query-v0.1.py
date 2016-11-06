'''
This script uses Jena to send SPARQL queries to the Apache Fuseki Server on port 3030.
So, first you need to download Jena from here: https://jena.apache.org/download/index.cgi
Then you need to set up your envoironment in order to be able to use jena. Luckilly it's the same in linux and mac. you can use this instruction:
https://jena.apache.org/documentation/tools/index.html

on linux and mac it's like this:
export JENAROOT=the directory you downloaded Jena to
export PATH=$PATH:$JENAROOT/bin
use this command to test if it works: sparql --version

These are the exact commands that I used in my linux machine:
farbod@farbod:~/Desktop$ export JENAROOT=/home/farbod/Downloads/apache-jena-3.1.0
farbod@farbod:~/Desktop$ export PATH=$PATH:$JENAROOT/bin
farbod@farbod:~/Desktop$ sparql --version

The following SPARQL query is just a simple query for testing.
'''

import os
f=os.popen('s-query --service http://localhost:3030/ds/query "prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> prefix owl: <http://www.w3.org/2002/07/owl#> prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?g ?s ?p ?o WHERE { GRAPH ?g { ?s ?p ?o} } LIMIT 25"')
printMe=f.read()
print printMe
