# recipe-finder-app
An app made for finding recipes based on ingredients entered by the user.



## Getting Started
To run the app:
```
python main.py
```
If your working with VS Code and module imports are not recognized, add the project directory 
in the system environment variables, giving it a name of PYTHONPATH and specifying the full path to the folder.
```
Edit the system environment variables >> Environment Variables >> System Variables >> New
```
## Example

When the app is launched two options will appear - to create an account or log in.

Recipes matching user ingredients the most are displayed first:

![tasty-results](https://github.com/JustasDaugi/recipe-finder-app/assets/114675049/721656f6-218b-475e-8c6b-2d955dbbba09)

![bbc-results](https://github.com/JustasDaugi/recipe-finder-app/assets/114675049/8bccdbd8-a274-43d3-ba2b-8cabbcc3dc98)

Additional options - view all recipes, save recipes, delete recipes:

![all-tasty](https://github.com/JustasDaugi/recipe-finder-app/assets/114675049/a552bfd3-7069-4f75-acf4-370347aedab4)

![all-bbc](https://github.com/JustasDaugi/recipe-finder-app/assets/114675049/175c5565-c305-4b19-a3d0-5f54972c7438)

![view-saved](https://github.com/JustasDaugi/recipe-finder-app/assets/114675049/e787d579-1256-42c7-b8df-dc61c2301d8d)


## Acknowledgements
This dataset contains 1,617 recipes.

The dataset is available at [Kaggle](https://www.kaggle.com/gjbroughton/christmas-recipes) with no license given (I'd like to acknowledge the authors of each recipe and [BBC Good Food](https://www.bbcgoodfood.com/) website.).


#### Statistics
```
#record: 1617
#nodes per record: [16, 64]  -  avg = 26.08

TYPE distribution:
objects: [1, 1]  -  avg = 1.0
 arrays: [2, 2]  -  avg = 2.0
   keys: [6, 6]  -  avg = 6.0
 values: [7, 55]  -  avg = 17.08

DEPTH distribution:
maximum: [3, 3]  -  avg = 3.0

OUTDEGREE distribution OBJECT:
minimum: [6, 6]  -  avg = 6.0
average: [6.0, 6.0]  -  avg = 6.0
maximum: [6, 6]  -  avg = 6.0

OUTDEGREE distribution ARRAY:
minimum: [0, 19]  -  avg = 3.47
average: [1.5, 25.5]  -  avg = 6.54
maximum: [2, 41]  -  avg = 9.61
```

#### Example
```
{
  "Name": "Christmas pie",
  "url": "https://www.bbcgoodfood.com/recipes/2793/christmas-pie",
  "Description": "Combine a few key Christmas flavours here to make a pie that both children and adults will adore",
  "Author": "Mary Cadogan",
  "Ingredients": [
    "2 tbsp olive oil",
    "knob butter",
    "1 onion, finely chopped",
    "500g sausagemeat or skinned sausages",
    "grated zest of 1 lemon",
    "100g fresh white breadcrumbs",
    "85g ready-to-eat dried apricots, chopped",
    "50g chestnut, canned or vacuum-packed, chopped",
    "2 tsp chopped fresh or 1tsp dried thyme",
    "100g cranberries, fresh or frozen",
    "500g boneless, skinless chicken breasts",
    "500g pack ready-made shortcrust pastry",
    "beaten egg, to glaze"
  ],
  "Method": [
    "Heat oven to 190C/fan 170C/gas 5. Heat 1 tbsp oil and the butter in a frying pan, then add the onion and fry for 5 mins until softened. Cool slightly. Tip the sausagemeat, lemon zest, breadcrumbs, apricots, chestnuts and thyme into a bowl. Add the onion and cranberries, and mix everything together with your hands, adding plenty of pepper and a little salt.",
    "Cut each chicken breast into three fillets lengthwise and season all over with salt and pepper. Heat the remaining oil in the frying pan, and fry the chicken fillets quickly until browned, about 6-8 mins.",
    "Roll out two-thirds of the pastry to line a 20-23cm springform or deep loose-based tart tin. Press in half the sausage mix and spread to level. Then add the chicken pieces in one layer and cover with the rest of the sausage. Press down lightly.",
    "Roll out the remaining pastry. Brush the edges of the pastry with beaten egg and cover with the pastry lid. Pinch the edges to seal, then trim. Brush the top of the pie with egg, then roll out the trimmings to make holly leaf shapes and berries. Decorate the pie and brush again with egg.",
    "Set the tin on a baking sheet and bake for 50-60 mins, then cool in the tin for 15 mins. Remove and leave to cool completely. Serve with a winter salad and pickles."
  ]
}
```
