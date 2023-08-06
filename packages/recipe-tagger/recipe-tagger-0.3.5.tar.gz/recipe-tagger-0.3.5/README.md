# Recipe Tagger

This package provides a classification and tagging system for ingredients and recipes. 
The functioning of the package is based on a dataset containing more than 700 ingredients mapped with their own class. 
If a provided ingredient is not mapped into the dataset, the library search for it on wikipedia pages, into the dictionary and into NLTK Wordnet to find the best possible class. 

An ingredient could be classified in one of the following class: 
- Vegetable
- Fruit
- Legume
- Meat
- Egg
- Diary
- Staple
- Condiment
- Nut
- Seafood
- Dessert

A recipe is tagged based on its ingredients class. 
The library also provides a function to get the class percentage of recipe ingredients. 

### Installation

```
pip install recipe_tagger
```

### How to use

```python
from recipe_tagger import recipe_tagger
```

**Get the class of a single ingredient**

```python
recipe_tagger.get_ingredient_class('aubergine')
# vegetable
```

**Get tags of a recipe (it is needed to provide all the ingredient of the recipe)**

```python
recipe_tagger.get_recipe_tags(['aubergine', 'chicken'])
# ['vegetable', 'meat']
```

**Get class percentage of a recipe (it is needed to provide all the ingredient of the recipe)**

```python
recipe_tagger.get_recipe_class_percentage(['aubergine', 'chicken', 'beef'])
# [('vegetable', '33.33%'), ('meat', '66.67%')]
```

### Todo
- [x] Handling of Wikipedia pages.
- [x] Better search over dictionary and Wikipedia pages of ingredient. 
- [ ] Possibility to add ingredient after search if it is not present. 
- [ ] Remove punctuation in provided ingrediets.
- [ ] Remove condiment if there are any other classes.
- [ ] Better search if the provided ingredient is composed by 2 words.
