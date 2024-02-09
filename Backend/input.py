while True:
    user_input = input("Enter something (type 'exit' to end): ")

    # Check if the user wants to exit
    if user_input.lower() == 'exit':
        print("Exiting the loop.")
        break

    # Process the user input (you can perform any desired operation here)
    print("You entered:", user_input)