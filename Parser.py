#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

class Parser(object):
    def __init__(self, recipeName):
        self.recipeName = recipeName

        self.recipeID = []
        self.parse_ingredients = []
        self.parse_preparation = []

    def generateID(self, number):
        IDs = ["222ZYXGD", "2222B2RC"]
        self.recipeID = IDs[number]
        return self.recipeID

    def parse(self):
        base_url = "http://www.foodista.com/recipe/"
        parse_url = base_url + self.recipeID + "/" + self.recipeName

        res = requests.get(parse_url)
        soup = BeautifulSoup(res.text)

        for post in soup.find_all(attrs={"itemprop": "ingredients"}):
            self.parse_ingredients.append(post.get_text())

        for post in soup.find_all(attrs={"itemprop": "recipeInstructions"}):
            self.parse_preparation.append(post.get_text())

    def getIngredients(self):
        return self.parse_ingredients

    def getPreparation(self):
        return self.parse_preparation



if __name__ == '__main__':
    print 'barnabys-caesar-salad mango-lassismoothie'
    recipeNames = [p.lower() for p in raw_input('> ').split(' ')]

    for number in range(len(recipeNames)):
        parser = Parser(recipeNames[number])
        parser.generateID(number)
        parser.parse()

        print 'Ingredients for', recipeNames[number]
        ingredients = parser.getIngredients()
        for l in ingredients:
            print l
        print '\n'

        print 'Preparation for', recipeNames[number]
        preparation = parser.getPreparation()
        for m in preparation:
            print m
        print '\n'
