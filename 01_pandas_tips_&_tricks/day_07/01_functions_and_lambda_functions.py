# # Functions
# def greet_user():
#     print("Greet the user and ask for their name.")
#     return input("What is your name? ")

# def process_greeting(name):
#     print("\nNice to meet you, " + name)
    
# # Call functions in order.
# name = process_greeting()
# process_greeting(name)


# # Functions
# def greet_user():
#     print("Greet the user and ask for their name.")
#     return input("What is your name? ")

# def process_greeting(name="User"):
#     print("\nNice to meet you, " + name)

# # Call functions in order.
# name = greet_user()  # Store the returned value from greet_user() in the 'name' variable
# process_greeting(name)  # Pass the 'name' variable to process_greeting() function

# if name:  # Check if 'name' has a value
#     process_greeting(name)  # Pass the 'name' variable to process_greeting() function
# else:
#     process_greeting()  # Call process_greeting() without providing a name

# process_greeting(name if name else None)


# # Functions
# def greet_user():
#     return input("What is your name? ")

# def process_greeting(name=None):
#     name = name if name else "User"
#     print("\nNice to meet you, " + name)

# # Call functions
# name = greet_user()
# process_greeting(name)


# def square(number):
#     return print(number * number)

# square(9)



# print("\nLet's have a conversation!")
# # Repeat Conversation
# while True:
#     print("\nYou can type 'quit' at any time to exit the program.\n")
#     user_input = input("Say something:\t").lower().strip()
#     if user_input == 'quit':
#         break
#     else:
#         print('You said "'+user_input+'".')
    


# # Recursion
# def factorial(n):
#     if n == 1:
#         return 1
#     else:
#         return n * factorial(n-1)
    
# print(factorial(5))




# lambda function

# x = lambda a: a +10
# print(x(int(input("Enter your Number"))))

x = lambda a, b: a*b
print(x(2,7))