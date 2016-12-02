# hws16_swt_FoodBomb
SWT Final Project

## How it works?
This is just part of the SWT final project.
This project query on the Foodista dataset with SPARQL query and also parse some important information which wasn't included in the dataset to provide a complete & useful recipe information for the client.
The client side is programmed in an android app by other teammates. Hence, here you only get the python scripts. If you are interested in the Android client app, please clone the code [here](https://github.com/10bitomaroof/AndroidReceipeApp)

## The Dataset
- [Foodista](https://datahub.io/dataset/foodista)
	* because kasabi is shut down, only the last data dump is alive. Here is a [backup](https://archive.org/download/kasabi) from other site, I think we'll only use [food.gz](https://archive.org/download/kasabi/food.gz).

## Getting Started
1. Download the latest [jena-fuseki-*-distribution](https://jena.apache.org/documentation/serving_data/)
2. Unpack the file
3. Run the Apache Fuseki server
`./fuseki-server --update --mem /ds`
4. Open your Browser with the adress below:
`localhost:3030`
5. Load the dataset(F1, F2 is in dataset.zip folder) into your Apache Fuseki server
![Fuseki-screenshot](https://github.com/lenatech/hws16_swt_FoodBomb/blob/master/assets/Fuseki-screenshot.jpg?raw=true)
6. Install all the required dependencies
`pip install -r requirements.txt`
If you don't have pip in your computer, download the script [here](https://bootstrap.pypa.io/get-pip.py)
Then, run `python get-pip.py`  
7. Execute the hws16_swt.py script by running
Edit your IP in hws_swt.py first
`python hws_swt.py`
8. Execute Client side Python script to see result
Edit your IP in client.py first
`python client.py`

## Big thanks to 
- swt16_project.py @[lenatech](https://github.com/lenatech)
- Evaluation @[farboda](https://github.com/farboda)



