# def is used as normal
def incr():
    
    # create an initial value, i
    i = 1
    
    # while loop
    while True:
        
        # the value to return at each call
        yield i 
        
        # the operation to perform on i at each call
        i += 1  

inc = incr()




for i in inc:
	if i > 50:
		break 
	else: 
		print(i)

