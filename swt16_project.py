#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import os
import requests
from bs4 import BeautifulSoup
import re
from SPARQLWrapper import SPARQLWrapper, JSON
import codecs
import json

class Socket(object):
    def create_conn(self, HOST, PORT):
        # Create Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #Bind HOST&PORT Socket
        try:
            s.bind((HOST, PORT))
        except socket.error as err:
            print 'Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1]
            sys.exit()
        # Setup and Start TCP listener
        # Socket start listening
        s.listen(10)
        conn, addr = s.accept()
        print conn
        print addr
        print 'Now Connected with ' + addr[0] + ':' + str(addr[1])
        return conn

    def receive(self, conn):
        return conn.recv(1024)

    def send(self, conn, data):
        conn.sendall(data)
    def close(self, conn):
        conn.close()

class Querier(object):

    def sendQuery(self, query, dataset):
        sparql = SPARQLWrapper("http://localhost:3030/"+dataset+"/query")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results

    def find_food_id(self, food_name):
        dataset = "F1"
        query = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?food_id WHERE{
                    GRAPH ?g { ?food_id rdfs:label \'"""+food_name+"""\' .}
                }
                """
        results = self.sendQuery(query, dataset)
        result = results["results"]["bindings"][0]
        food_id = result["food_id"]["value"][-8:]
        return food_id

    def find_recipe_ids(self, priority_food_ids, other_food_ids):
        priorities = (self.combinePrefix("kasabif:", priority_food_ids))[0] if len(priority_food_ids) ==1 else ", ".join(str(x) for x in self.combinePrefix("kasabif:", priority_food_ids))
        others = (self.combinePrefix("?other = kasabif:", other_food_ids))[0] if len(other_food_ids) ==1 else " || ".join(str(x) for x in self.combinePrefix("?other = kasabif:", other_food_ids))

        dataset = "F2"
        if len(other_food_ids) <1:
            query = """
                PREFIX recipe: <http://linkedrecipes.org/schema/>
                PREFIX kasabif: <http://data.kasabi.com/dataset/foodista/food/>
                SELECT ?recipe_id WHERE{
                    GRAPH ?graph {?recipe_id recipe:ingredient """+priorities+""".}
                }
                """
        else:
            query = """
                PREFIX recipe: <http://linkedrecipes.org/schema/>
                PREFIX kasabif: <http://data.kasabi.com/dataset/foodista/food/>
                SELECT ?recipe_id WHERE{
                    GRAPH ?graph {?recipe_id recipe:ingredient """+priorities+""", ?other.}
                    FILTER("""+others+""")
                }
                """
        results = self.sendQuery(query, dataset)

        recipe_of_food = []
        for result in results["results"]["bindings"]:
            recipe_of_food.append(result["recipe_id"]["value"][-8:])
        return recipe_of_food

    def combinePrefix(self, prefix, id_list):
        L = [prefix + food_id for food_id in id_list]
        return L

    def find_recipe_info(self, recipe_id):
        dataset = "F2"
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX kasabir: <http://data.kasabi.com/dataset/foodista/recipe/>
                PREFIX recipe: <http://linkedrecipes.org/schema/>
                PREFIX kasabit: <http://data.kasabi.com/dataset/foodista/tags/>
                PREFIX purl: <http://purl.org/dc/terms/>

                SELECT
                    DISTINCT ?recipe_link
                    (SAMPLE (?img) as ?recipe_image)
                    (SAMPLE (?desc) as ?recipe_description)
                    (group_concat(distinct strafter(str(?recipe_tag), 'http://data.kasabi.com/dataset/foodista/tags/' );separator='|') as ?recipe_tags)
                    (group_concat(distinct strafter(str(?recipe_related), 'http://data.kasabi.com/dataset/foodista/recipe/' );separator='|') as ?recipe_relateds)
                    (group_concat(distinct strafter(str(?recipe_technique), 'http://data.kasabi.com/dataset/foodista/technique/' );separator='|') as ?recipe_techniques)
                WHERE {
                    GRAPH ?graph{
                        kasabir:"""+recipe_id+""" foaf:isPrimaryTopicOf ?recipe_link.
                        kasabir:"""+recipe_id+""" foaf:depiction ?img.
                        OPTIONAL{kasabir:"""+recipe_id+""" purl:description ?desc}.
                        OPTIONAL { VALUES ?desc{"none"} }.
                        OPTIONAL{kasabir:"""+recipe_id+""" recipe:category ?recipe_tag}.
                        OPTIONAL{VALUES ?recipe_tag{"none"} }.
                        OPTIONAL{kasabir:"""+recipe_id+""" purl:related ?recipe_related}.
                        OPTIONAL{VALUES ?recipe_related{"none"} }.
                        OPTIONAL{kasabir:"""+recipe_id+""" recipe:uses ?recipe_technique}.
                        OPTIONAL{VALUES ?recipe_technique{"none"} }.
                    }
                }GROUP BY ?recipe_link
                """
        results = self.sendQuery(query, dataset)
        result = results["results"]["bindings"][0]
        recipe_link = result["recipe_link"]["value"]
        recipe_image = result["recipe_image"]["value"]
        recipe_description = result["recipe_description"]["value"]
        recipe_tags = [str(j) for j in (result["recipe_tags"]["value"]).split('|')]
        recipe_relateds = [str(j) for j in (result["recipe_relateds"]["value"]).split('|')]
        recipe_techniques = [str(j) for j in (result["recipe_techniques"]["value"]).split('|')]
        return (recipe_link, recipe_image, recipe_description, recipe_tags, recipe_relateds, recipe_techniques)

class Parser(object):
    def __init__(self):
        self.parse_title = []

    def parse(self, link):
        self.parse_ingredients = []
        self.parse_preparation = []
        res = requests.get(link)
        soup = BeautifulSoup(res.text, "lxml")

        for post in soup.find_all(attrs={"itemprop": "ingredients"}):
            self.parse_ingredients.append(post.get_text())

        for post in soup.find_all(attrs={"itemprop": "recipeInstructions"}):
            self.parse_preparation.append(post.get_text())

        for post in soup.find_all(attrs={"itemprop": "name"}):
            self.parse_title.append(post.get_text())

    def getIngredients(self):
        return self.parse_ingredients

    def getPreparation(self):
        return self.parse_preparation

    def getTitle(self):
        return self.parse_title

if __name__ == '__main__':
    while True:
        HOST = '192.168.0.24'
        PORT = 2222

        sk = Socket()
        conn = sk.create_conn(HOST, PORT)
        receive_string = sk.receive(conn)

        data_loaded = json.loads(receive_string)

        querier = Querier()

        priority_food_ids = []
        other_food_ids = []
        for k, v in data_loaded.items():
            if v == 1:
                food_id = querier.find_food_id(k)
                priority_food_ids.append(food_id)
            elif v == 0:
                food_id = querier.find_food_id(k)
                other_food_ids.append(food_id)
            else:
                print "priority missing"

        recipe_id = querier.find_recipe_ids(priority_food_ids, other_food_ids)
        #Write file for Evaluation
        file = codecs.open("recipe_ids.txt", "w", "utf-8")
        for j in recipe_id:
            file.write(j+" ")
        file.close()

        parser = Parser()

        result_dict = []
        for x in range(len(recipe_id)):
            recipe = {}
            recipe_link, recipe_image, recipe_description, recipe_tags, recipe_relateds, recipe_techniques = querier.find_recipe_info(recipe_id[x])
            parser.parse(recipe_link)

            recipe["recipeName"] = parser.getTitle()[x]
            recipe["description"] = recipe_description
            recipe["imgURL"] = recipe_image
            recipe["ingredients"] = parser.getIngredients()
            recipe["preparation"] = parser.getPreparation()
            recipe["tags"] = recipe_tags
            recipe["techniques"] = recipe_techniques
            #recipe["tools"] = recipe_tools
            recipe["related"] = recipe_relateds

            result_dict.append(recipe)

        serialized_dict = json.dumps(result_dict)
        sk.send(conn, serialized_dict)
        sk.close(conn)
