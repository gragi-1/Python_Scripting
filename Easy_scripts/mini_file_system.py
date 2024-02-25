import os
import shutil

def create_file(filename):
    with open(filename, 'w') as file:
        file.write("")

def copy_file(source, destination):
    shutil.copy2(source, destination)

def move_file(source, destination):
    shutil.move(source, destination)

def delete_file(filename):
    os.remove(filename)

def create_directory(dirname):
    os.mkdir(dirname)

def delete_directory(dirname):
    shutil.rmtree(dirname)

def check_existence(path):
    if os.path.exists(path):
        print(f"The path {path} exists.")
    else:
        print(f"The path {path} does not exist.")

def rename(path, new_name):
    base_dir = os.path.dirname(path)
    new_path = os.path.join(base_dir, new_name)
    os.rename(path, new_path)

def list_files_and_directories(path):
    for name in os.listdir(path):
        print(name)

def get_file_size(filename):
    size = os.path.getsize(filename)
    print(f"The size of the file {filename} is {size} bytes.")

def file_management_system():
    while True:
        print("\nMini File Management System")
        print("1. Create File")
        print("2. Copy File")
        print("3. Move File")
        print("4. Delete File")
        print("5. Create Directory")
        print("6. Delete Directory")
        print("7. Check Existence")
        print("8. Rename")
        print("9. List Files and Directories")
        print("10. Get File Size")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            filename = input("Enter filename to create: ")
            create_file(filename)
        elif choice == '2':
            source = input("Enter source filename: ")
            destination = input("Enter destination filename: ")
            copy_file(source, destination)
        elif choice == '3':
            source = input("Enter source filename: ")
            destination = input("Enter destination filename: ")
            move_file(source, destination)
        elif choice == '4':
            filename = input("Enter filename to delete: ")
            delete_file(filename)
        elif choice == '5':
            dirname = input("Enter directory name to create: ")
            create_directory(dirname)
        elif choice == '6':
            dirname = input("Enter directory name to delete: ")
            delete_directory(dirname)
        elif choice == '7':
            path = input("Enter path to check: ")
            check_existence(path)
        elif choice == '8':
            path = input("Enter path to rename: ")
            new_name = input("Enter new name: ")
            rename(path, new_name)
        elif choice == '9':
            path = input("Enter path to list files and directories: ")
            list_files_and_directories(path)
        elif choice == '10':
            filename = input("Enter filename to get size: ")
            get_file_size(filename)
        elif choice == '11':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    file_management_system()