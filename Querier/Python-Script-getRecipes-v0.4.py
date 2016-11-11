'''
changes: 
Using Enhanced SPARQL query
'''
import os

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
	print '**************'
	print 'Recipe ID: ',finalId
	print '**************'
	print 'Number of Recipes: ',len(finalId)
	print '**************'

main()
