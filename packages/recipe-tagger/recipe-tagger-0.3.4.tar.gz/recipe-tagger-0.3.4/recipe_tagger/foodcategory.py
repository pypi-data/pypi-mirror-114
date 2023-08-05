from enum import Enum
from nltk.corpus import wordnet

class FoodCategory(Enum):
    vegetable = 0
    fruit = 1
    legume = 2
    meat = 3
    egg = 4
    dairy = 5
    staple = 6  
    condiment = 7  
    nut = 8  
    seafood = 9
    dessert = 10

class CategorySynset():
    categories = [wordnet.synset(f'{FoodCategory.vegetable.name}.n.01'),
                    wordnet.synset(f'{FoodCategory.fruit.name}.n.01'),
                    wordnet.synset(f'{FoodCategory.legume.name}.n.01'),
                    wordnet.synset(f'{FoodCategory.meat.name}.n.01'),
                    wordnet.synset(f'{FoodCategory.egg.name}.n.01'),
                    wordnet.synset(f'{FoodCategory.dairy.name}.n.01'),
                    wordnet.synset(f'{FoodCategory.staple.name}.n.01'),
                    wordnet.synset(f'{FoodCategory.condiment.name}.n.01'),
                    wordnet.synset(f'{FoodCategory.nut.name}.n.01'),
                    wordnet.synset(f'{FoodCategory.seafood.name}.n.01'),
                    ]