import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
import easygui
import shutil
import pyotp
import math
import random
import smtplib
from twofish import Twofish
from tkinter import simpledialog
def tfencrypt(infile, outfile, password):

    bs = 16 #block size 16 bytes or 128 bits 
    plaintext=infile.read()

    if len(plaintext)%bs: #add padding 
	    padded_plaintext=str(plaintext+'%'*(bs-len(plaintext)%bs)).encode('utf-8')
    else:
	    padded_plaintext=plaintext.encode('utf-8')

    T = Twofish(str.encode(password))
    ciphertext=b''

    for x in range(int(len(padded_plaintext)/bs)):
	    ciphertext += T.encrypt(padded_plaintext[x*bs:(x+1)*bs])

    outfile.write(ciphertext)
    outfile.close()


def tfdecrypt(infile, outfile, password):

    bs = 16 #block size 16 bytes or 128 bits
    ciphertext = infile.read()
    T = Twofish(str.encode(password))
    plaintext=b''

    for x in range(int(len(ciphertext)/bs)):
        plaintext += T.decrypt(ciphertext[x*bs:(x+1)*bs])

    outfile.write(str.encode(plaintext.decode('utf-8').strip('%'))) #remove padding
    outfile.close()


password = '12345'

'''with open('infile.txt', 'r') as infile, open('outfile.txt', 'wb') as outfile:
    tfencrypt(infile, outfile, password)

with open('outfile.txt', 'rb') as infile, open('outfile_decrypted.txt', 'wb') as outfile:
    tfdecrypt(infile, outfile, password)'''


def Save():
    filename = ""
    def SaveAs():
        FileName = filedialog.asksaveasfile(initialdir="/", defaultextension='.txt', filetypes=[("text files", ".txt"), ("all files", ".*")])

        if FileName:
            # Get the filename entered by the user
            filename = FileName.name
            print("Selected filename:", filename)

            # Get the content from the Text widget and write it to the file
            FileText = str(textspace.get(1.0, END))
            FileName.write(FileText)
            FileName.close()
            outfilename = filename + '_encr'
            with open(filename, 'r') as infile, open(outfilename, 'wb') as outfile:
                tfencrypt(infile, outfile, password)
            os.remove(filename)
            os.rename(outfilename,filename)
            
        
    Screen.destroy()
    SaveWindow = Tk()

    button = Button(text="SaveAs", command=SaveAs)
    button.pack()
    textspace = Text(SaveWindow)
    textspace.pack()
    print("The file name is ",filename)
  
        #     os.rename("outfile.txt",filename)


#opening a file
'''def Open():  
    Read=easygui.fileopenbox()
    try:
        os.startfile(Read)
    except:
        mb.showinfo("file not found")'''


otp_secret = pyotp.random_base32()

# Create an OTP object
otp = pyotp.TOTP(otp_secret)
def get_gmail_credentials():
    gmail_username = simpledialog.askstring("Input", "Enter your Gmail username:")
    gmail_password = simpledialog.askstring("Input", "Enter your Gmail password:", show="*")  # Show '*' for password
    return gmail_username, gmail_password
'''
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    '''
def proceed():
    global file_path
    outfilename = file_path+"decrypt"
    with open(file_path, 'rb') as infile, open(outfilename, 'wb') as outfile:
        tfdecrypt(infile, outfile, password)
    os.remove(file_path)
    os.rename(outfilename,file_path)
    
    # os.startfile(file_path)

def OTP_Create():
    global file_path
    digits="0123456789"
    OTP=""
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    otp = OTP + " is your OTP"
    msg= otp
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    gmail_username, gmail_password = get_gmail_credentials()
    s.login(gmail_username,gmail_password)
    s.sendmail('&&&&&&&&&&&',gmail_username,msg)
    otp_window = Tk()
    otp_window.title("OTP Verification")
    
    def verify_otp():
        global file_path
        entered_otp = otp_entry.get()
        print(entered_otp)
        
        if entered_otp == OTP:
            print("Verified")
            proceed_button.pack()
        else:
            print("Please Check your OTP again")
    
    otp_var = StringVar()
    otp_entry = Entry(otp_window, textvariable=otp_var, show='*')
    otp_entry.pack()
    
    verify_button = Button(otp_window, text="Verify OTP", command=verify_otp)
    verify_button.pack()
    
    proceed_button = Button(otp_window, text="Proceed", command=proceed)
def Open():
    global file_path
    file_path = filedialog.askopenfilename()
    OTP_Create()
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
import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox as mb

NewFolder = ""
Folder = ""

def CreateFolder():
    global NewFolder
    global Folder

    def save_password():
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()

        if new_password == confirm_password:
            path = os.path.join(Folder, NewFolder)
            os.mkdir(path)
            mb.showinfo("Folder created successfully")
            root_password.destroy()
        else:
            mb.showerror("Error", "Passwords do not match.")

    Folder = filedialog.askdirectory()
    print("Enter a name for the folder")
    NewFolder = input()
    def no_action():
        path = os.path.join(Folder, NewFolder)
        os.mkdir(path)
        mb.showinfo("Folder created successfully")


    def yes_action():
        global root_password
        root_password = Tk()
        root_password.title("Set Password")

        new_password_label = Label(root_password, text="Enter New Password:")
        new_password_label.pack()

        global new_password_entry
        new_password_entry = Entry(root_password, show="*")
        new_password_entry.pack()

        confirm_password_label = Label(root_password, text="Confirm Password:")
        confirm_password_label.pack()

        global confirm_password_entry
        confirm_password_entry = Entry(root_password, show="*")
        confirm_password_entry.pack()

        submit_button = Button(root_password, text="Set Password", command=save_password)
        submit_button.pack()
        
        
    root = Tk()
    root.title("Do you want this to be a private folder?")

    ask_button1 = Button(root, text="Yes", command=yes_action)
    ask_button2 = Button(root, text="No",command=no_action)
    ask_button1.pack()
    ask_button2.pack()
    # root.destroy()
    # path = os.path.join(Folder, NewFolder)
    # os.mkdir(path)
    # mb.showinfo("Folder created successfully")


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
Screen.title("File Explorer")
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
CreateFolderButton = Button(text="Create Folder",command=CreateFolder)
CreateFolderButton.place(relx=0.3,rely=0.8)
MoveFileButton = Button(text="Move File",command=MoveFile)
MoveFileButton.place(relx=0.5,rely=0.8)



mainloop()
