from week1.Day4.ExerciseXP.ExerciceXp import Dog
import random


# Step 2: Create the PetDog class
class PetDog(Dog):
    def __init__(self, name, age, weight):
        super().__init__(name, age, weight)
        self.trained = False

    def train(self):
        print(self.bark())
        self.trained = True

    def play(self, *args):
        dog_names = ', '.join([dog.name for dog in args] + [self.name])
        print(f'{dog_names} all play together')

    def do_a_trick(self):
        if self.trained:
            tricks = ["does a barrel roll", "stands on his back legs", "shakes your hand", "plays dead"]
            print(f'{self.name} {random.choice(tricks)}')
        else:
            print(f'{self.name} is not trained yet!')

# Step 3: Test PetDog methods
dog1 = PetDog('Rex',   5, 30)
dog2 = PetDog('Buddy', 3, 20)
dog3 = PetDog('Max',   4, 25)

print('--- Train ---')
dog1.train()
dog2.train()

print('\n--- Play ---')
dog1.play(dog2, dog3)

print('\n--- Do a Trick ---')
dog1.do_a_trick()        
dog2.do_a_trick()        
dog3.do_a_trick()        



