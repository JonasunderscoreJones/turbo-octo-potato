# Open the file in write mode ('w')
with open('uwu.txt', 'w') as file:
    while True:
        input1 = input('Enter input-1 (or leave it empty to exit): ')
        input2 = input('Enter input-2 (or leave it empty to exit): ')

        # Check if both inputs are empty, and exit the loop if they are
        if not input1 and not input2:
            break

        # Write the input pair to the file in the specified format
        file.write(f"'{input1}': '{input2}',\n")

print('Data saved to uwu.txt.')
