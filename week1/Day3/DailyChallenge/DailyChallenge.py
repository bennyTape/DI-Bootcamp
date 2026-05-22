# What You’ll learn
# Classes and Objects
# Dictionaries
# String Formatting
# Methods
# List manipulation and sorting


# Key Python Topics:

# Classes and Objects
# Dictionaries
# String Formatting
# Methods
# List manipulation (sorted())
# Conditional logic (if)
# String concatenation






class Farm:
    def __init__(self, farm_name):
        self.name = farm_name
        self.animals = {}

    def add_animal(self, animal_type=None, count=1, **kwargs):
        if animal_type is not None:
            if animal_type in self.animals:
                self.animals[animal_type] += count
            else:
                self.animals[animal_type] = count

        for key, valeur in kwargs.items():
            if key in self.animals:
                self.animals[key] += valeur
            else:
                self.animals[key] = valeur

    def get_info(self):
        my_list = self.animals.items()
        to_return = f"the farm's name is {self.name}\n"
        a = ""
        for x, y in my_list:
            a += f" {x} : {y} \n,"
        return to_return + a

    def get_animal_types(self):
        animaux_list = self.animals.keys()
        return sorted(animaux_list)

    def get_short_info(self):
        a = ""
        for x, y in self.animals.items():
            if y > 1:
                a = a + x + "s "
            else:
                a = a + x + " "
        return f"McDonald's farm has {a}"


macdonald = Farm("McDonald")
macdonald.add_animal('cow', 5)
macdonald.add_animal('sheep')
macdonald.add_animal('sheep')
macdonald.add_animal('goat', 12)
macdonald.add_animal(pig=3, chicken=10)
print(macdonald.get_short_info())
print(macdonald.get_info())