#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup

class Querier(object):
    def find_food_id(self, food_name):
        query='rsparql --service http://localhost:3030/F1/query \'SELECT ?p WHERE { GRAPH ?g { ?p <http://www.w3.org/2000/01/rdf-schema#label>"'+food_name+'"} }\''
        a=os.popen(query)
        data=a.read()
        a.close()
        #Extract food id
        return data[228:-64]

    def find_recipe_id (self, food_id):
        query='rsparql --service http://localhost:3030/F2/query "SELECT ?s WHERE { GRAPH ?o { ?s ?p <http://data.kasabi.com/dataset/foodista/food/'+str(food_id)+'>}}"'
        a=os.popen(query)
        data=a.read()
        a.close()

        #Extract recipe id: first id can be found at 236 ~ 236+8 ;last id can be found at len(data)-74 ~ len(data)-74+8; intervals between each id is 62
        recipe_of_food = []
        k = 236
        interval = 62
        while k <= len(data) - 74:
            recipe_of_food.append(data[k:k+8])
            k = k + interval
        return recipe_of_food

    def find_recipe_link (self, recipe_id):
        query ='rsparql --service http://localhost:3030/F2/query "SELECT ?o WHERE {GRAPH ?g { <http://data.kasabi.com/dataset/foodista/recipe/'+str(recipe_id)+'> <http://xmlns.com/foaf/0.1/isPrimaryTopicOf> ?o}}"'
        a=os.popen(query)
        data=a.read()
        a.close()
        return data[204:-71]

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
        link = querier.find_recipe_link(m)
        recipe_link.append(link)

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
