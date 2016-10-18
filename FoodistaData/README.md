## How these are generated

<http://data.kasabi.com/dataset/foodista/food/#>
Row1 ~ 41805
`head -n 41805 foodista > F1`

<http://data.kasabi.com/dataset/foodistan/#>
41806~962730
`head -n 962730 foodista | tail -n 920925 > F2`

<http://data.kasabi.com/dataset/foodista/tags/#>
962731~977280
`head -n 977280 foodista | tail -n 14550 > F3`

<http://data.kasabi.com/dataset/foodista/technique/#>
977281~978237
`head -n 978237 foodista | tail -n 957 > F4`

<http://data.kasabi.com/dataset/foodista/tool/#>
978238~979067
`head -n 979067 foodista | tail -n 830 > F5`

<http://www.foodista.com/food/#>
979068~986718
`head -n 986718 foodista | tail -n 7651 > F6`

<http://www.foodista.com/recipe/#>
986719~1019500
`head -n 1019500 foodista | tail -n 32782 > F7`

<http://www.foodista.com/technique/#>
1019501~1019650
`head -n 1019650 foodista | tail -n 150 > F8`

<http://www.foodista.com/tool/#>
1019799~1019651
`head -n 1019799 foodista | tail -n 149 > F9`
