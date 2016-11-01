import os

def changeDataToStringLinkArray ( data ):
	recipes=[]
	i=0
	itemp=0
	j=0
	while i<len(data):
		if data[i]=='h' and data[i+1]=='t' and data[i+2]=='t' and data[i+3]=='p':
			itemp=i
			recipes.append("")
			while data[itemp]!='>':
				recipes[j]+=data[itemp]
				itemp+=1
			j+=1
		i += 1
	return recipes

def sendQueryToFuseki ( oneIngredientName ):
	queryString='rsparql --service http://localhost:3030/ds/query "SELECT ?s WHERE { GRAPH ?o { ?s ?p <http://data.kasabi.com/dataset/foodista/food/'+oneIngredientName+'>}}"'
	a=os.popen(queryString)
	data=a.read()
	return changeDataToStringLinkArray(data)

def findTheCommonRecipes ( recipesArray1 ,  recipesArray2):
	newRecipesArray1=[]
	for i in range(len(recipesArray1)-1):
		for j in range(len(recipesArray2)-1):
			if recipesArray1[i]==recipesArray2[j]:
				newRecipesArray1.append(recipesArray1[i])
				break
	return newRecipesArray1

def main():
	temp = open ("ingredients.txt", "r+")
	arrayOfIngredients = temp.read().splitlines()
	allRecipesArray=[]	
	aCounter=0
	while aCounter<len(arrayOfIngredients):
		allRecipesArray.append(sendQueryToFuseki(arrayOfIngredients[aCounter]))
		aCounter+=1

	for x in range(len(allRecipesArray)):
		if (x+1)<len(allRecipesArray):
			allRecipesArray[0]=findTheCommonRecipes(allRecipesArray[0],allRecipesArray[x+1])
	print allRecipesArray[0]
	print len(allRecipesArray[0])
main()
