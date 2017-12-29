file = open("..\..\sample_data\my_file.txt", "w" )

# Interrrogate the file:
print( "File Name:",  file.name )

print( "Open Mode:",  file.mode )

print( "Readable:",  file.readable())

print( "Writable:",  file.writable())

# Write a function to deterine the file's status:
def get_status( f ):
    if ( f.closed != False ) :
        return "Closed"
    else :
        return "Open"

print( "File Status:" , get_status(file))  

file.close()

print( "File Status:" , get_status(file))