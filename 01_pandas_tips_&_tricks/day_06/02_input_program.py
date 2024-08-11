# name = input("Enter your name:") #user input
# print(name) #output

# print("hello", name,"or sunao") #print

person_A_name = input("What is your name?")
person_A_age = input("Enter your age")

person_B_name = input("What is your name?")
person_B_age = input("Enter your age")

if person_A_age > person_B_age:
    print("Hello, " + person_A_name + ". You are older than " +  person_B_name +".")

else:
    print("Hello, " + person_B_name+ ". You are older than " +  person_A_name +".")