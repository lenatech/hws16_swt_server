'''
changes: 
the bug "recipe returns none #1" fixed.
'''
import os
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import copy


def gettingTheIdFromTheLinkStringRecipe ( data ):
	recipes=[]
	i=0
	itemp=0
	j=0
	while i<len(data):
		if data[i]=='i' and data[i+1]=='p' and data[i+2]=='e' and data[i+3]=='/':
			itemp=i+4
			recipes.append("")
			while data[itemp]!='>':
				recipes[j]+=data[itemp]
				itemp+=1
			j+=1
		i += 1
	return recipes

def gettingTheIdFromTheLinkStringName ( data ):
	nameID=""
	i=0
	itemp=0
	j=0
	while i<len(data):
		if data[i]=='o' and data[i+1]=='o' and data[i+2]=='d' and data[i+3]=='/':
			itemp=i+4
			while data[itemp]!='>':
				nameID+=data[itemp]
				itemp+=1
			j+=1
		i += 1
	
	return nameID


def gettingTheTagNames ( data ):
	tags=[]
	i=0
	itemp=0
	j=0
	while i<len(data):
		if data[i]=='a' and data[i+1]=='g' and data[i+2]=='s' and data[i+3]=='/':
			itemp=i+4
			tags.append("")
			while data[itemp]!='>':
				tags[j]+=data[itemp]
				itemp+=1
			j+=1
		i += 1
	return tags

def sendQueryToFuseki ( oneIngredientName ):
	queryString='rsparql --service http://localhost:3030/F2/query "'
	queryString+="""PREFIX recipe: <http://linkedrecipes.org/schema/> PREFIX kasabif: <http://data.kasabi.com/dataset/foodista/food/> SELECT ?recipe_id WHERE{GRAPH ?graph { ?recipe_id recipe:ingredient kasabif:"""+oneIngredientName+""" .}}"""
	queryString+='"'
	a=os.popen(queryString)
	data=a.read()
	a.close()
	return gettingTheIdFromTheLinkStringRecipe(data)

def findTheCommonRecipes ( recipesArray1 ,  recipesArray2):
	newRecipesArray1=[]
	for i in range(len(recipesArray1)):
		for j in range(len(recipesArray2)):
			if recipesArray1[i]==recipesArray2[j]:
				newRecipesArray1.append(recipesArray1[i])
				break
	
	return newRecipesArray1

def findingTheIdofTheName(arrayOfIngredients):
	newArrayOfIngredients=[]
	for i in range(len(arrayOfIngredients)):
		queryString='rsparql --service http://localhost:3030/F1/query "'
		queryString+="""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?food_id WHERE{GRAPH ?g { ?food_id rdfs:label \'"""+arrayOfIngredients[i]+"""\' .}}"""
		queryString+='"'
		a=os.popen(queryString)
		data=a.read()
		a.close()
		newArrayOfIngredients.append(gettingTheIdFromTheLinkStringName(data))
	return newArrayOfIngredients

def gettingTags(recId):
	queryString='rsparql --service http://localhost:3030/F2/query "'
	queryString+="""PREFIX recipe: <http://linkedrecipes.org/schema/> PREFIX recID: <http://data.kasabi.com/dataset/foodista/recipe/> SELECT ?recipe_id WHERE{GRAPH ?graph { recID:"""+recId+""" recipe:category ?recipe_id.}}"""
	queryString+='"'
	a=os.popen(queryString)
	data=a.read()
	a.close()
	return gettingTheTagNames(data)

def sendQuery( query, dataset):
        sparql = SPARQLWrapper("http://localhost:3030/"+dataset+"/query")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results

def countTags(recId):
	dataset = "F2"
	recString=""
	for i in range(len(recId)):
		recString+=" ?recipe_id = kasabir:"+str(recId[i])
		if i != (len(recId)-1):
			recString+=" ||"
	query="""PREFIX recipe: <http://linkedrecipes.org/schema/> PREFIX kasabir: <http://data.kasabi.com/dataset/foodista/recipe/> SELECT ?recipe WHERE{ SELECT (SAMPLE(?recipe_id) as ?recipe) ?tag (count(?tag) as ?count) WHERE{ GRAPH ?graph { ?recipe_id recipe:category ?tag.} FILTER("""+recString+""")}GROUP BY (?tag) ORDER BY DESC(?count)}GROUP BY (?recipe) LIMIT 5"""
        sparql = SPARQLWrapper("http://localhost:3030/F2/query")
	results = sendQuery(query, dataset)
	relevant_recipe=[]
	for result in results["results"]["bindings"]:
		relevant_recipe.append(result["recipe"]["value"][-8:])
	return relevant_recipe

def main():
	temp = open ("ingredients.txt", "r+")
	arrayOfIngredientsName = temp.read().splitlines()
	arrayOfIngredientsID = findingTheIdofTheName(arrayOfIngredientsName)
	print '**************'
	print 'Ingredient Names: ',arrayOfIngredientsName
	print '**************'
	print 'Ingredient IDs: ',arrayOfIngredientsID
	print '**************'
	allRecipesArray=[]
	aCounter=0
	while aCounter<len(arrayOfIngredientsID):
		allRecipesArray.append(sendQueryToFuseki(arrayOfIngredientsID[aCounter]))
		aCounter+=1
	

	backUpAllRecipesArray= copy.copy(allRecipesArray)
	for x in range(len(allRecipesArray)):
		if len(allRecipesArray)==1:
			finalId=allRecipesArray[0]
			break
		else:
			if (x+1)<len(allRecipesArray):
				allRecipesArray[0]=findTheCommonRecipes(allRecipesArray[0],allRecipesArray[x+1])
				finalId=allRecipesArray[0]
			else:
				break

	if len(finalId)<5:
		for i in range(len(backUpAllRecipesArray)-1):
			del backUpAllRecipesArray[-1]
			temp=copy.copy(backUpAllRecipesArray)
			common=[]
			for x in range(len(temp)):
				if len(temp)==1:
					common=temp[0]
					break
				else:
					if (x+1)<len(temp):
						temp[0]=findTheCommonRecipes(temp[0],temp[x+1])
						common=temp[0]
					else:
						break
			if len(common)>0:
				for x in range(len(common)):
					if len(finalId)<5:
						finalId.append(common[x])
			if len(finalId)==5:
				break
	'''
	tagArray=[]
	aCounter=0
	while aCounter<len(finalId):
		tagArray.append(gettingTags(finalId[aCounter]))
		aCounter+=1
	print len(tagArray)
	for i in range(len(tagArray)):
		print tagArray[i]
	'''
	print '**************'
	print 'Recipe ID: ',finalId
	print '**************'
	print 'Number of Recipes: ',len(finalId)
	print '**************'
	if len(finalId)==5:
		print 'Number of Recipes: ',finalId
	if len(finalId)>5:
		print 'Number of Recipes: ',countTags(finalId)
main()
