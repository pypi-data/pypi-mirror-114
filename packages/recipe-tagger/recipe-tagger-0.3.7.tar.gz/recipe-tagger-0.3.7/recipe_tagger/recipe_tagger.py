"""
Module containg all the main methods of the package. 
"""


import io
import pkgutil
import re
from collections import Counter

import numpy as np
import wikipediaapi
from nltk import tag
from nltk.corpus import wordnet
from PyDictionary import PyDictionary
from pyfood.utils import Shelf
from textblob import Word

from .foodcategory import CategorySynset, FoodCategory

embedding_path = "data/ingredient_embedding.npy"


def __get_embedding():
    """
    Get the dataset of ingredients as a dictionary.

    :return: a dictionary representing the embedding
    """
    embedding_io = io.BytesIO(pkgutil.get_data(__name__, embedding_path))
    return np.load(embedding_io, allow_pickle=True).item()


def __remove_punctuation(word):
    word = word.strip()
    return re.sub(r"[^\w\s]", "", word)


def lemmatize_word(word):
    """
    Lemmatize the provided word.
    Lemmatization is the process of converting a word to its base form.

    :param word: the word to be lemmatized.
    :return: the word lemmatized.
    """
    w = Word(word)
    return w.lemmatize()


def is_ingredient_vegan(ingredient):
    """
    Check if the provided ingredient is vegan or not.

    :param ingredient: the name of the ingredient.
    :return: a bool indicating whether the ingredient is vegan or not.
    """
    ingredient = ingredient.strip()
    shelf = Shelf("Milan", month_id=0)
    results = shelf.process_ingredients([ingredient])
    return results["labels"]["vegan"]


def is_recipe_vegan(ingredients):
    """
    Check if the provided ingredients contained in a recipe ar vegan or not.
    If only one element is not vegan the recipe is not vegan.

    :param ingredients: the list of the ingredients.
    :return: a bool indicating wheter the recipe is vegan or not.
    """
    shelf = Shelf("Milan", month_id=0)
    results = shelf.process_ingredients(ingredients)
    return results["labels"]["vegan"]


def add_ingredient(ingredient, tag):
    """
    Map the provided ingredient and the tag into the embedding dataset.
    Tag must be one the following FoodCategory:
    vegetable, fruit, meat, legume, diary, egg, staple,
    condiment, nut, seafood, dessert

    :param ingredient: the name of the ingredient.
    :param tag: the class of the ingredient. Must be one of the listed above.
    :return: a bool indicating if the operation has succeded or not.
    """
    embedding = __get_embedding()
    ingredient = ingredient.strip()
    tag = tag.strip()
    if ingredient in embedding:
        return False

    embedding[ingredient] = FoodCategory[tag].value
    return True


def search_ingredient_hypernyms(ingredient):
    """
    Predict the class of the provided ingredient based on the Wu & Palmer’s
    similarity between ingredient, his hypernyms and the 11 FoodCategory.
    The FoodCategory is choosen based on the maximum similarity value between
    the ingredient, its hypernym and the various categories. If the predicted
    category is different between ingredient and hypernym the category is
    choosen based on the avarege of both.

    :param ingredient: the name of the ingredient.
    :return: the class of the ingredient.
    """
    if " " in ingredient:
        ingredient = ingredient.split(" ")[-1]

    ingredient = wordnet.synsets(ingredient)[0]
    hypernym = ingredient.hypernyms()[0]
    categories = CategorySynset.categories

    sim = []
    hypernym_sim = []
    for cat in categories:
        sim.append(ingredient.wup_similarity(cat))
        hypernym_sim.append(hypernym.wup_similarity(cat))

    best_sim = sim.index(max(sim))
    best_hyp = hypernym_sim.index(max(hypernym_sim))

    if best_sim == best_hyp:
        return FoodCategory(best_sim).name
    else:
        sum = [(x + y) / 2 for x, y in zip(sim, hypernym_sim)]
        return FoodCategory(sum.index(max(sum)))


def search_ingredient_class(ingredient):
    """
    Search on wikipedia and english dictionary the class of
    the provided ingredient.
    Returns the most occurrences of a single FoodCategory class based on
    the two research.

    :param ingredient: the name of the ingredient.
    :return: the class of the ingredient.
    """
    if " " in ingredient:
        ingredient = ingredient.split(" ")[-1]

    dictionary = PyDictionary()
    wiki = wikipediaapi.Wikipedia("en")

    page = wiki.page(ingredient)
    meaning = dictionary.meaning(ingredient)["Noun"]
    ontology = ", ".join(meaning) if meaning else ""

    categories = []
    for category in FoodCategory:
        if page and re.search(r"\b({0})\b".format(category.name), page.summary):
            categories.append(category.name)
        if ontology and re.search(r"\b({0})\b".format(category.name), ontology):
            categories.append(category.name)
    return max(categories, key=categories.count) if len(categories) else None


def get_ingredient_class(ingredient):
    """
    Predict the class of the provided ingredient based on the embeddings.
    If the ingredient cannot be found in the dictionary it will be
    searched on wikipedia pages or hypernyms.

    :param ingredient: the name of the ingredient.
    :return: the class of the ingredient.
    """
    embedding = __get_embedding()
    ingredient = __remove_punctuation(ingredient)
    lemmatized_ing = lemmatize_word(ingredient)
    if lemmatized_ing in embedding:
        return FoodCategory(embedding[lemmatized_ing]).name
    else:
        web_class = search_ingredient_class(ingredient)
        hyp_class = search_ingredient_hypernyms(lemmatized_ing)
        return web_class if web_class else hyp_class


def get_recipe_class_percentage(ingredients):
    """
    Classify a recipe in tags based on its ingredient.
    Returns the percentages of ingredient class in the recipe provided.

    :param ingredients: list of ingredients in the recipe.
    :return: list of tuples containg classes and percentages.
    """
    tags = [get_ingredient_class(ingredient) for ingredient in ingredients]
    c = Counter(tags)
    return [(i, str(round(c[i] / len(tags) * 100.0, 2)) + "%") for i in c]


def get_recipe_tags(ingredients):
    """
    Classify a recipe in tags based on its ingredient.
    Tag could be: Vegetable, Fruit, Meat, Legume, Diary,
    Egg, Staple, Condiment, Nut, Seafood

    :param ingredients: list of ingredients in the recipe.
    :return: set of tags for the recipe.
    """
    tags = [get_ingredient_class(ingredient) for ingredient in ingredients]
    if None in tags:
        tags.remove(None)
    if len(tags) >= 2 and FoodCategory.condiment.name in tags:
        tags.remove(FoodCategory.condiment.name)
    return list(set(tags)) if len(tags) else tags
