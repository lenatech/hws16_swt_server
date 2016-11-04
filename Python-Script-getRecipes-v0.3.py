'''
changes: it's able to read the ingredients based on their names (it can change the ingredient names to IDs)
'''
import os

def gettingTheFromTheLinkStringRecipe ( data ):
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

def gettingTheFromTheLinkStringName ( data ):
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
	queryString='rsparql --service http://localhost:3030/F2/query "SELECT ?s WHERE { GRAPH ?o { ?s ?p <http://data.kasabi.com/dataset/foodista/food/'+str(oneIngredientName)+'>}}"'
	a=os.popen(queryString)
	data=a.read()
	a.close()
	return gettingTheFromTheLinkStringRecipe(data)

def findTheCommonRecipes ( recipesArray1 ,  recipesArray2):
	newRecipesArray1=[]
	for i in range(len(recipesArray1)-1):
		for j in range(len(recipesArray2)-1):
			if recipesArray1[i]==recipesArray2[j]:
				newRecipesArray1.append(recipesArray1[i])
				break
	return newRecipesArray1

def findingTheIdofTheName(arrayOfIngredients):
	newArrayOfIngredients=[]
	for i in range(len(arrayOfIngredients)):
		queryString='rsparql --service http://localhost:3030/F1/query \'SELECT ?p WHERE { GRAPH ?g { ?p ?s "'+arrayOfIngredients[i]+'"} }\''
		a=os.popen(queryString)
		data=a.read()
		a.close()
		print 'data >', data
		print 'here >',gettingTheFromTheLinkStringName(data)
		newArrayOfIngredients.append(gettingTheFromTheLinkStringName(data))
	print 'start'
	print newArrayOfIngredients
	print 'bye'
	return newArrayOfIngredients

def main():
	temp = open ("ingredients.txt", "r+")
	arrayOfIngredientsName = temp.read().splitlines()
	arrayOfIngredientsID = findingTheIdofTheName(arrayOfIngredientsName)
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
	print finalId
	print len(finalId)

main()
