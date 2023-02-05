from production import IF, THEN, AND, OR, backward_chain

# r = (
#     IF(OR('(?x) has x', '(?x) has y'),
#        THEN('(?x) has x or y')),
#
#     IF(AND('(?x) has x or y',
#            '(?x) has z'),
#        THEN('(?x) has x or y and z'))
# )
#
# res = backward_chain(r, 'bob has x or y and z')
# print('result: ', res)

#
# if __name__=='__main__':
#
#     #TODO: implement your code here!
#
#     # example how to print output:
#     print("Welcome to Expert System! TODO: implement")
#
#     # an example how to read input:
#     input_name = input("please write your name:\n")
#
#     print("Hello, ", input_name, "!")
#
#     # example how to read a numeric input:
#     input_age = int(input("what is your age?\n"))
#     print("Your age is", input_age)
#
#     print("Great! Now please implement the code for the lab :) ")
#
