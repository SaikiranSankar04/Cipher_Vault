import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
import tkinter as tk
import easygui
import shutil
import pyotp
import math
import random
import smtplib
from twofish import Twofish
from tkinter import simpledialog
from datetime import datetime
import subprocess
import signal
minutes=0
new_password=None
file_path=""
folder_password=None
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


#password = '12345'

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
                tfencrypt(infile, outfile, new_password)
            os.remove(filename)
            os.rename(outfilename,filename)
            
        
    
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
    global new_password
    password = onetime_get_password()
    print("password:",password)
    print("new:",new_password)
    if(password ==new_password):
        outfilename = file_path+"decrypt"
        
        with open(file_path, 'rb') as infile, open(outfilename, 'wb') as outfile:
            tfdecrypt(infile, outfile, new_password)
        os.remove(file_path)
        os.rename(outfilename,file_path)
        
        os.startfile(file_path)
    return
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
            proceed()         
  #          os.startfile(file_path)
        else:
            print("Please Check your OTP again")
    
    otp_var = StringVar()
    otp_entry = Entry(otp_window, textvariable=otp_var, show='*')
    otp_entry.pack()
    
    verify_button = Button(otp_window, text="Verify OTP", command=verify_otp)
    verify_button.pack()
    
    proceed_button = Button(otp_window, text="Proceed", command=proceed)

def close_file():
    global file
    file.close()
    file_contents_label.config(text="")
    access_status.set("File Closed")

def save_password():
    global new_password
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()
    print("new in save:",new_password)
    if new_password == confirm_password:
        # Perform your actions here
        mb.showinfo("Success", "Passwords matched.")
        root_password.destroy()
    else:
        mb.showerror("Error", "Passwords do not match.")
def save_pw_folder():
    global new_pw_folder
    new_pw_folder = new_pw_entry.get()
    confirm_pw = confirm_pw_entry.get()
    print("new password folder:", new_pw_folder)
    print("confirm :", confirm_pw)
    if new_pw_folder == confirm_pw:
        # Perform your actions here
        mb.showinfo("Success", "Passwords matched.")
        folder_pw.destroy()
    else:
        mb.showerror("Error", "Passwords do not match.")

def create_pw_folder():
    global folder_pw
    folder_pw = Tk()
    folder_pw.title("Private Folder")

    new_pw_label = Label(folder_pw, text="Enter New Password:")
    new_pw_label.pack()

    global new_pw_entry
    new_pw_entry = Entry(folder_pw, show="*")
    new_pw_entry.pack()

    confirm_pw_label = Label(folder_pw, text="Confirm Password:")
    confirm_pw_label.pack()

    global confirm_pw_entry
    confirm_pw_entry = Entry(folder_pw, show="*")
    confirm_pw_entry.pack()

    submit_button = Button(folder_pw, text="Set Password", command=save_pw_folder)
    submit_button.pack()
    folder_pw.mainloop()
def save_password():
    global new_password,root_password
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()

    if new_password == confirm_password:
        mb.showinfo("Success", "Password saved: " + new_password)
        root_password.destroy()
    else:
        mb.showerror("Error", "Passwords do not match.")   
def create_password_encrypt():
    

    def get_password():
        global new_password_entry, confirm_password_entry, root_password
        root_password = tk.Tk()
        root_password.title("Password Entry")

            # Labels and Entry widgets for new and confirm passwords
        new_password_label = tk.Label(root_password, text="New Password:")
        new_password_label.grid(row=0, column=0)
        new_password_entry = tk.Entry(root_password, show='*')
        new_password_entry.grid(row=0, column=1)

        confirm_password_label = tk.Label(root_password, text="Confirm Password:")
        confirm_password_label.grid(row=1, column=0)
        confirm_password_entry = tk.Entry(root_password, show='*')
        confirm_password_entry.grid(row=1, column=1)

            # Button to save passwords
        save_button = tk.Button(root_password, text="Save", command=save_password)
        save_button.grid(row=2, columnspan=2)
        root_password.mainloop()
        
    get_password()     
       
def check_password():
    global new_password
    password = simpledialog.askstring("Password", "Enter password:", show='*')
    if password == new_password:
        mb.showinfo("Success", "Correct password entered!")
    else:
        mb.showerror("Error", "Incorrect password.")

'''def check_password_encrypt():
    global new_password
    password = simpledialog.askstring("Password", "Enter password:", show='*')
    if password == new_password:
        mb.showinfo("Success", "Correct password entered!")
        return True
    else:
        mb.showerror("Error", "Incorrect password.")
        return False'''

def onetime_get_password():
    root = tk.Tk()
    root.withdraw()
    password = simpledialog.askstring("Password", "Enter the decryption password:", show='*')
    return password

# Example usage:
# password = get_password()
   


# Create the main Tkinter window with a different variable name


def update_countdown(remaining_time, label):
    if remaining_time > 0:
        minutes, seconds = divmod(remaining_time, 60)
        hours, minutes = divmod(minutes, 60)
        label.config(text=f"Time Remaining: {hours:02d}:{minutes:02d}:{seconds:02d}")
        main_window.after(1000, update_countdown, remaining_time - 1, label)

def check_access():
    
    global minutes
    global file_path
    main_window = Tk()
    current_time = datetime.now().time()
    start_time = datetime.now().strftime("%H:%M")

    end_time = (datetime.strptime(start_time, "%H:%M") + timedelta(minutes=minutes)).strftime("%H:%M")

    if start_time <= end_time:
        access_status.set("Access Granted")
        file_path = filedialog.askopenfilename()
        proceed()

        # Create and place the countdown label
        countdown_label = Label(main_window, text="Time Remaining: 00:00:00")
        countdown_label.place(relx=0.3, rely=0.9)

        # Calculate remaining time and start countdown
        remaining_time = (datetime.strptime(end_time, "%H:%M") - datetime.strptime(start_time, "%H:%M")).seconds
        update_countdown(remaining_time, countdown_label)
        print(remaining_time)
        # Wait for some time (simulate a delay)
        time.sleep(minutes * 60)

        # Close Notepad or perform other actions after time expires
        os.system("taskkill /im notepad.exe /f")
        countdown_label.config(text="Time's Up!")  # Display 'Time's Up!' after file access time is over
    else:
        access_status.set("Access Denied")
        file_contents_label.config(text="")

# ... rest of your code where the check_access() function is called or utilized

    main_window.mainloop()  # Start the main Tkinter event loop


       
    
''' # Create the Tkinter windows
    window = tk.Tk()
    window.title("File Access Control")

    # Create labels and entry fields
    start_time_label = tk.Label(window, text="Start Time (HH:MM):")
    start_time_label.pack()
    start_time_entry = tk.Entry(window)
    start_time_entry.pack()

    end_time_label = tk.Label(window, text="End Time (HH:MM):")
    end_time_label.pack()
    end_time_entry = tk.Entry(window)
    end_time_entry.pack()

    access_button = tk.Button(window, text="Check Access", command=check_access)
    access_button.pack()

    access_status = tk.StringVar()
    access_status_label = tk.Label(window, textvariable=access_status)
    access_status_label.pack()

    file_contents_label = tk.Label(window)
    file_contents_label.pack()'''
def mins():
    global minutes
    def get_minutes():
        global minutes
        try:
            minutes = int(entry.get())
            mb.showinfo("Success", f"Entered minutes: {minutes}")
        except ValueError:
            mb.showerror("Error", "Please enter a valid number!")

    root = tk.Tk()
    root.title("Enter Minutes")

    label = tk.Label(root, text="Enter number of minutes:")
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    button = tk.Button(root, text="Submit", command=get_minutes)
    button.pack()
    
    


def Open():
    global file_path
    folder_path = filedialog.askdirectory()
    current_directory = os.getcwd()
    a=current_directory+"\private_folder"
    b=current_directory+"\time_access"
    a= a.replace("\\","/")
    
    if (folder_path==a):
        check_password()
        file_path = filedialog.askopenfilename()
        
        OTP_Create()
        
    elif(folder_path==b):
        check_access()
        
        
        
    else:
        file_path = filedialog.askopenfilename()
        # os.startfile(file_path)
        proceed()
        
        
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

    save_pw_folder()

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
        



#Moving the file
def MoveFile():
    Read=easygui.fileopenbox()
    Destination =filedialog.askdirectory()
    if(Read==Destination):
        mb.showinfo('confirmation', "Source and destination are same")
    else:
        shutil.move(Read, Destination)  
        mb.showinfo("File has moved  successfully")

def create_folders():
    folders = ['private_folder', 'time_access']
    for folder_name in folders:
        folder_path = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
create_folders()  #to initialise two folders-private & timebased
current_directory = os.getcwd()
folder_to_protect = os.path.join(current_directory, "private_folder")
create_password_encrypt()
#create_pw_folder()
mins()

create_pw_folder()
#check_password()
# Protect the folder
#protect_folder(folder_to_protect, entered_password)
#root_password.mainloop() 
#creating buttons and Initializing window
def on_closing():
    # Perform any cleanup actions here before closing the window
    # Optionally ask for confirmation before closing
    if mb.askokcancel("Quit", "Do you want to quit?"):
        Screen.destroy()
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
Screen.protocol("WM_DELETE_WINDOW", on_closing)  
Screen.mainloop()
