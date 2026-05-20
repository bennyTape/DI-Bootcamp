#Challenge 1
# Ask the user for a number and a length.
# Create a program that prints a list of multiples of the number until the list length reaches length.
nb = int(input("Enter a number"))

length = int(input("Enter a length"))

multiple = [ p*nb for p in range(1,length+1)]

print(multiple)





#Challenge 2
# Write a program that asks a string to the user, and display a new string with any duplicate consecutive letters removed.
word = input(" Enter a word :")
f =""
for i in word :
    if i in f:
        0
    else:
     f = f+i
print(f)