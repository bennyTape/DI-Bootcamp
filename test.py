base_price =10
pizza =[]
while True:
    response = input("enter a topping")
    if response == "quit":
        break
    print(f"Adding {response} to your pizza")
    pizza.append(response)
    base_price+=2.5

print(f"the amount is {base_price}")

