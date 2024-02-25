import string
import random
import pyperclip

def generate_password(length, use_uppercase, use_numbers, use_special_chars):
    # Start with lowercase letters
    possible_chars = string.ascii_lowercase

    # Add uppercase letters, if specified
    if use_uppercase:
        possible_chars += string.ascii_uppercase

    # Add numbers, if specified
    if use_numbers:
        possible_chars += string.digits

    # Add special characters, if specified
    if use_special_chars:
        possible_chars += string.punctuation

    # Generate and return the password
    return ''.join(random.choice(possible_chars) for _ in range(length))

def main():
    # Dictionary to store passwords
    passwords = {}

    while True:
        print("\nPassword Manager")
        print("1. Generate new password")
        print("2. View passwords")
        print("3. Update password")
        print("4. Delete password")
        print("5. Copy password to clipboard")
        print("6. Exit")

        # Ask the user for the desired option
        option = int(input("Please select an option: "))

        if option == 1:
            # Ask the user for the desired password length and character types
            service = input("Enter the name of the service: ")
            length = int(input("Enter the desired password length: "))
            use_uppercase = input("Include uppercase letters? (yes/no): ").lower() == 'yes'
            use_numbers = input("Include numbers? (yes/no): ").lower() == 'yes'
            use_special_chars = input("Include special characters? (yes/no): ").lower() == 'yes'

            # Generate and store the password
            password = generate_password(length, use_uppercase, use_numbers, use_special_chars)
            passwords[service] = password
            print("Your password for " + service + " has been generated.")
        elif option == 2:
            # View passwords
            for service, password in passwords.items():
                print(service + ": " + password)
        elif option == 3:
            # Update password
            service = input("Enter the name of the service for which you want to update the password: ")
            if service in passwords:
                length = int(input("Enter the new desired password length: "))
                use_uppercase = input("Include uppercase letters in the new password? (yes/no): ").lower() == 'yes'
                use_numbers = input("Include numbers in the new password? (yes/no): ").lower() == 'yes'
                use_special_chars = input("Include special characters in the new password? (yes/no): ").lower() == 'yes'

                # Generate and update the password
                password = generate_password(length, use_uppercase, use_numbers, use_special_chars)
                passwords[service] = password
                print("Your password for " + service + " has been updated.")
            else:
                print("Service not found.")
        elif option == 4:
            # Delete password
            service = input("Enter the name of the service for which you want to delete the password: ")
            if service in passwords:
                del passwords[service]
                print("Your password for " + service + " has been deleted.")
            else:
                print("Service not found.")
        elif option == 5:
            # Copy password to clipboard
            service = input("Enter the name of the service for which you want to copy the password: ")
            if service in passwords:
                pyperclip.copy(passwords[service])
                print("Your password for " + service + " has been copied to the clipboard.")
            else:
                print("Service not found.")
        elif option == 6:
            # Exit the program
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()