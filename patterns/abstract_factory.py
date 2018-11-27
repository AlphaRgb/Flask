#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: AlphaFF
# @Date:   2018-11-09 13:26:42
# @Email: liushahedi@gmail.com
# @Last Modified by:   AlphaFF
# @Last Modified time: 2018-11-09 13:39:10

import random


class PetShop:
    """A pet shop"""

    def __init__(self, animal_factory):
        self.pet_factory = animal_factory

    def show_pet(self):
        pet = self.pet_factory()
        print("it says {}".format(pet.speak()))


class Dog:
    def speak(self):
        return "woof"

    def __str__(self):
        return "Dog"


class Cat:
    def speak(self):
        return "meow"

    def __str__(self):
        return "cat"


def random_animal():
    return random.choice([Dog, Cat])()


if __name__ == '__main__':
    cat_shop = PetShop(Cat)
    cat_shop.show_pet()

    shop = PetShop(random_animal)
    for i in range(10):
        shop.show_pet()
        print('=' * 20)
