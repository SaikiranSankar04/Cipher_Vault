import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
import easygui
import shutil
#Saving a file
from cryptography.fernet import Fernet # Import the necessary module from the cryptography library

# Generate a random encryption key
def generate_key():
    return Fernet.generate_key()  # Generate a 32-byte encryption key using Fernet

# Generate an encryption key
key = generate_key()  # Call the generate_key function to create the encryption key

print("Encryption Key:", key)  # Print the generated encryption key

from cryptography.fernet import Fernet

# Generate a random encryption key
def generate_key():
    return Fernet.generate_key()

# Encrypt the contents of a file using the provided key
def encrypt_file(filename, key):
    cipher_suite = Fernet(key)  # Initialize a Fernet object with the encryption key
    with open(filename, 'rb') as file:
        plaintext = file.read()  # Read the plaintext data from the file
    encrypted_data = cipher_suite.encrypt(plaintext)  # Encrypt the plaintext data
    with open(filename + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)  # Write the encrypted data to a new file

# Generate an encryption key
key = generate_key()

# Specify the source file to be encrypted
source_file = 'plaintext.txt'

# Encrypt the file using the generated key
encrypt_file(source_file, key)

# Inform the user about the successful encryption
print(f'{source_file} encrypted.')  # Print a message indicating successful encryption

# Print the encrypted content in hexadecimal format
encrypted_filename = source_file + '.encrypted'
with open(encrypted_filename, 'rb') as encrypted_file:
    encrypted_data = encrypted_file.read()
    encrypted = encrypted_data.hex()
    print("Encrypted Content:", encrypted)


from cryptography.fernet import Fernet

# Generate a random encryption key
def generate_key():
    return Fernet.generate_key()

# Encrypt the contents of a file using the provided key
def encrypt_file(filename, key):
    cipher_suite = Fernet(key)  # Initialize a Fernet object with the key
    with open(filename, 'rb') as file:
        plaintext = file.read()  # Read the plaintext data from the file
    encrypted_data = cipher_suite.encrypt(plaintext)  # Encrypt the plaintext
    with open(filename + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)  # Write the encrypted data to a new file

# Decrypt the contents of an encrypted file using the provided key
def decrypt_file(encrypted_filename, key):
    cipher_suite = Fernet(key)  # Initialize a Fernet object with the key
    with open(encrypted_filename, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()  # Read the encrypted data from the file
    decrypted_data = cipher_suite.decrypt(encrypted_data)  # Decrypt the data
    decrypted_filename = encrypted_filename.replace('.encrypted', '.decrypted')  # Generate a new filename
    with open(decrypted_filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)  # Write the decrypted data to a new file

key = generate_key()  # Generate an encryption key
source_file = 'plaintext.txt'  # Specify the source file to be encrypted

# Encrypt the file using the generated key
encrypt_file(source_file, key)

encrypted_file = source_file + '.encrypted'  # Generate the name of the encrypted file

# Decrypt the encrypted file using the same key
decrypt_file(encrypted_file, key)

# Inform the user about the successful decryption
print(f'{encrypted_file} decrypted.')

# Print the content of the decrypted file
decrypted_filename = source_file + '.decrypted'
with open(decrypted_filename, 'r') as decrypted_file:
    decrypted_content = decrypted_file.read()
    print("Decrypted Content:\n", decrypted_content)







    
def Save():
    def SaveAs():
        FileName = filedialog.asksaveasfile(initialdir="/",defaultextension='.txt',filetypes=[("text files",".txt"),("all files",".*")])
        FileText=str(textspace.get(1.0,END))
        FileName.write(FileText)
    Screen.destroy()
    SaveWindow= Tk()
    button = Button(text="SaveAs", command=SaveAs)
    button.pack()
    textspace = Text(SaveWindow)
    textspace.pack()
#opening a file
def Open():
    Read=easygui.fileopenbox()
    try:
        os.startfile(Read)
    except:
        mb.showinfo("file not found")
#Renaming a file
def Rename():
    Read=easygui.fileopenbox()
    pathnew = os.path.dirname(Read)
    extension=os.path.splitext(Read)[1]
    print("Enter new name of the file")
    newName=input()
    path1 = os.path.join(pathnew, newName+extension)
    print(path1)
    os.rename(Read,path1) 
    mb.showinfo("File Renamed !")
#deleting a file
def Delete():
    Read=easygui.fileopenbox()
    if os.path.exists(Read):
        os.remove(Read)             
    else:
        mb.showinfo("File not found , please check!")
#copying a file
def Copy():
    Read=easygui.fileopenbox()
    destination1=filedialog.askdirectory()
    shutil.copy(Read,destination1)
    mb.showinfo("File successfully copied ")
#deleting a folder
def DeleteFolder():
    DelFolder = filedialog.askdirectory()
    os.rmdir(DelFolder)
    mb.showinfo("Folder successfully deleted")
#creating a folder
def CreateFolder():
    Folder = filedialog.askdirectory()
    print("Enter a name for the folder")
    NewFolder=input()
    path = os.path.join(Folder, NewFolder)  
    os.mkdir(path)
    mb.showinfo("Folder created successfully")
#Moving the file
def MoveFile():
    Read=easygui.fileopenbox()
    Destination =filedialog.askdirectory()
    if(Read==Destination):
        mb.showinfo('confirmation', "Source and destination are same")
    else:
        shutil.move(Read, Destination)  
        mb.showinfo("File has moved  successfully")
#creating buttons and Initializing window
Screen=Tk()
Screen.title("File Explorer by - ProjectGururkul ")
Screen.geometry("500x500")
Screen.config(bg="pink")
SaveButton = Button(text="Save",command=Save)
SaveButton.place(relx=0.3,rely=0.2)
OpenButton = Button(text="Open",command=Open)
OpenButton.place(relx=0.5,rely=0.2)
RenameButton = Button(text="Rename",command=Rename)
RenameButton.place(relx=0.3,rely=0.4)
CopyButton = Button(text="Copy",command=Copy)
CopyButton.place(relx=0.5,rely=0.4)
DeleteButton = Button(text="Delete File",command=Delete)
DeleteButton.place(relx=0.3,rely=0.6)
DeleteFolderButton = Button(text="Delete Folder",command=DeleteFolder)
DeleteFolderButton.place(relx=0.5,rely=0.6)
CreateFolderButton = Button(text="Create Folder",command=Rename)
CreateFolderButton.place(relx=0.3,rely=0.8)
MoveFileButton = Button(text="Move File",command=MoveFile)
MoveFileButton.place(relx=0.5,rely=0.8)
mainloop()
