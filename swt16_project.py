#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
import re
from SPARQLWrapper import SPARQLWrapper, JSON
import codecs

class Querier(object):

    def sendQuery(self,query,dataset):
        sparql = SPARQLWrapper("http://localhost:3030/"+dataset+"/query")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results

    def find_food_id(self,food_name):
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

    def find_recipe_id (self, food_id):
        dataset = "F2"
        query = """
                PREFIX recipe: <http://linkedrecipes.org/schema/>
                PREFIX kasabif: <http://data.kasabi.com/dataset/foodista/food/>
                SELECT ?recipe_id WHERE{
                    GRAPH ?graph { ?recipe_id recipe:ingredient kasabif:"""+food_id+""" .}
                }
                """
        results = self.sendQuery(query, dataset)
        
        recipe_of_food = []
        for result in results["results"]["bindings"]:
            recipe_of_food.append(result["recipe_id"]["value"][-8:])
        return recipe_of_food

    def find_recipe_info (self, recipe_id):
        dataset = "F2"
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX kasabir: <http://data.kasabi.com/dataset/foodista/recipe/>
                SELECT ?recipe_link ?recipe_image{
                    GRAPH ?graph { kasabir:"""+recipe_id+""" foaf:isPrimaryTopicOf ?recipe_link.
                    kasabir:"""+recipe_id+""" foaf:depiction ?recipe_image.}
                }
                """

        results = self.sendQuery(query, dataset)
        result = results["results"]["bindings"][0]
        recipe_link = result["recipe_link"]["value"]
        recipe_image = result["recipe_image"]["value"]
        return (recipe_link, recipe_image)


class Parser(object):
    def __init__(self):
        self.parse_ingredients = []
        self.parse_preparation = []
        self.parse_title = []

    def parse(self, link):
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
    print 'Please provide your ingredients in a text file: ingredients_name.txt'
    file_name = raw_input('> ')
    print '\n'

    food_name_list = open(file_name, "r+").read().splitlines()
    print "Ingredients_Name: ", food_name_list

    querier = Querier()

    all_recipes = []
    for food_name in food_name_list:
        food_id = querier.find_food_id(food_name)
        all_recipes.append(querier.find_recipe_id(food_id))

    #Need to optimize this part
    for x in range(len(all_recipes)):
        if len(all_recipes)==1:
            recipe_id=all_recipes[0]
            break
        else:
            if (x+1)<len(all_recipes):
                r1 = all_recipes[0]
                r2 = all_recipes[x+1]
                all_recipes[0]= [val for val in r1 if val in r2]
                recipe_id = all_recipes[0]
            else:
                break

    #Get recipe Link for parsing
    recipe_link = []
    for m in recipe_id:
        recipe_info = querier.find_recipe_info(m)
        recipe_link.append(recipe_info[0])
        print "recipe_img: ", recipe_info[1]

    parser = Parser()
    for link in recipe_link:
        parser.parse(link)
        title = parser.getTitle()[0]
        print "Recipe_Name: ", title
        print '\n'

        print 'Brief_Ingredients:'
        ingredients = parser.getIngredients()
        for l in ingredients:
            print l
        print '\n'

        print 'Steps_Detatils: '
        preparation = parser.getPreparation()
        for m in preparation:
            print m
        print '\n'
