# hws16_swt_FoodBomb
SWT Project

## The Dataset

- [The Recipe Dataset](https://ckannet-storage.commondatastorage.googleapis.com/2015-04-16T11:22:17.374Z/recipe-dataset.ttl)
- TBD (ex. allergen, Calories)
	* Nutrient: both are used in RDBMS.
	* [SR25](https://www.ars.usda.gov/northeast-area/beltsville-md/beltsville-human-nutrition-research-center/nutrient-data-laboratory/docs/sr25-download-files/)
	* [Canadian Nutrient File](http://www.hc-sc.gc.ca/fn-an/nutrition/fiche-nutri-data/cnf_downloads-telechargement_fcen-eng.php)

- [Foodista](https://datahub.io/dataset/foodista)
	* because kasabi is shut down, only the last data dump is alive. Here is a [backup](https://archive.org/download/kasabi) from other site, I think we'll only use [food.gz](https://archive.org/download/kasabi/food.gz).
- Run Server
`$ ./fuseki-server --update --mem /ds `


