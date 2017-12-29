poem = 'I never saw a man who looked\nWith such a wistful eye\n'

poem += "Upon that little tent of blue\n" 

poem += "Which prisoners call the sky\n"
print(poem)


file = open("..\..\sample_data\poem.txt","w")

file.write(poem)

file.close()

print("-----------hole text ----------------")
file = open("..\..\sample_data\poem.txt", "r")

contents = file.read()


print(contents)
file.close()

print("----------line by line -----------------")
file = open("..\..\sample_data\poem.txt", "r")

for line in file:
	print(line, end="")
file.close()

print("----------word by word-----------------")
file = open("..\..\sample_data\poem.txt")

for word in file.read().split():
	print(word, end=" ")

file.close()