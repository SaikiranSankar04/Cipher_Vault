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
from datetime import datetime,timedelta
import subprocess
import signal
import psutil
import time
import mysql.connector

#global variables
file_path=""
folder_password=None
NewFolder = ""
Folder = ""

#Creating a connection object
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Csstudent_saikiran3",
  database="FileExplorer"
)



connection = mydb
cursor = connection.cursor()
create_query = "CREATE TABLE IF NOT EXISTS Passwords (Title VARCHAR(50) ,passwords VARCHAR(50) )"     
cursor.execute(create_query)
connection.commit()
create_query = "CREATE TABLE IF NOT EXISTS AccessTime (Duration INT )"     
cursor.execute(create_query)
connection.commit()

#Using Twofish for encrypting a file
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


#Using Twofish for decrypting a file
def tfdecrypt(infile, outfile, password):

    bs = 16 #block size 16 bytes or 128 bits
    ciphertext = infile.read()
    T = Twofish(str.encode(password))
    plaintext=b''

    for x in range(int(len(ciphertext)/bs)):
        plaintext += T.decrypt(ciphertext[x*bs:(x+1)*bs])

    outfile.write(str.encode(plaintext.decode('utf-8').strip('%'))) #remove padding
    outfile.close()

#Function to save the newly created file
def Save():
    filename = ""
    SaveWindow = tk.Tk()
    def SaveAs():
        FileName = filedialog.asksaveasfile(initialdir="/", defaultextension='.txt', filetypes=[("text files", ".txt"), ("all files", ".*")])

        if FileName:
            # Get the filename entered by the user
            filename = FileName.name
                       
            # Get the content from the Text widget and write it to the file
            FileText = str(textspace.get(1.0, END))
            FileName.write(FileText)
            FileName.close()
            outfilename = filename + '_encr'
            connection = mydb
            cursor = connection.cursor()

            select_query = "SELECT Passwords FROM Passwords WHERE Title = %s"
            title_to_search = ("Encryption",)

            cursor.execute(select_query, title_to_search)

            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    new_password = row[0] 
            with open(filename, 'r') as infile, open(outfilename, 'wb') as outfile:
                tfencrypt(infile, outfile, new_password)
            os.remove(filename)
            os.rename(outfilename,filename)

    button = tk.Button(SaveWindow,text="SaveAs", command=SaveAs)
    button.pack()
    textspace = tk.Text(SaveWindow)
    textspace.pack()
    print("The file name is ",filename)


#To open and decrypt the file
def proceed():
    global file_path
    
    password = onetime_get_password()
    connection = mydb
    cursor = connection.cursor()

    select_query = "SELECT Passwords FROM Passwords WHERE Title = %s"
    title_to_search = ("Encryption",)

    cursor.execute(select_query, title_to_search)

    rows = cursor.fetchall()

    if rows:
        for row in rows:
            new_password = row[0] 
    if(password ==new_password):
        outfilename = file_path+"decrypt"
        
        with open(file_path, 'rb') as infile, open(outfilename, 'wb') as outfile:
            tfdecrypt(infile, outfile, new_password)
        
        
        os.startfile(outfilename)
        file_to_delete = outfilename
        deleted = False
        time.sleep(20)
        while not deleted:
            # Check if Notepad is running
            notepad_running = False
            for proc in psutil.process_iter(['pid', 'name']):
                if 'notepad.exe' in proc.info['name'].lower():
                    notepad_running = True
                    break

            # If Notepad is not running, delete the file
            if not notepad_running:
                if os.path.exists(file_to_delete):
                    os.remove(file_to_delete)
                    deleted = True 
                    print(f"File '{file_to_delete}' deleted.")
                else:
                    print(f"File '{file_to_delete}' not found.")
            
            # Wait for a certain period before checking again
            time.sleep(5)  # Check every 5 seconds
        
    return

#OTP ACCESS- TO ACCESS FILES IN THE PRIVATE FOLDER
otp_secret = pyotp.random_base32() 
otp = pyotp.TOTP(otp_secret)        

#To get gmail and password of the user
def get_gmail_credentials():
    gmail_username = simpledialog.askstring("Input", "Enter your Gmail username:")
    gmail_password = simpledialog.askstring("Input", "Enter your Gmail password:", show="*")  # Show '*' for password
    return gmail_username, gmail_password


#To create and send an OTP to the user's gmail
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
        else:
            print("Please Check your OTP again")
    
    otp_var = StringVar()
    otp_entry = Entry(otp_window, textvariable=otp_var, show='*')
    otp_entry.pack()
    
    verify_button = Button(otp_window, text="Verify OTP", command=verify_otp)
    verify_button.pack()
    
    proceed_button = Button(otp_window, text="Proceed", command=proceed)

#To set password for the private folder
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

    submit_button = Button(folder_pw, text="Set Password", command=save_password_folder)
    submit_button.pack()
    folder_pw.mainloop()

def save_password_folder():
    connection = mydb
    cursor = connection.cursor()
    new_password = new_pw_entry.get()
    confirm_password = confirm_pw_entry.get()
    insert_query = "INSERT INTO Passwords (Title, passwords) VALUES (%s, %s)"
    user_data = ("Folder", new_password)
    cursor.execute(insert_query, user_data)
    connection.commit()

    if new_password == confirm_password:
        mb.showinfo("Success", "Password saved: " + new_password)
        folder_pw.destroy()  # Close the window
    else:
        mb.showerror("Error", "Passwords do not match.")

#To create password for encrypting files
def create_password_encrypt():
    def save_password():
        # Retrieve passwords from the entry fields
        password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()
        
        # Check if passwords match
        if password == confirm_password:
            connection = mydb
            cursor = connection.cursor()

            insert_query = "INSERT INTO Passwords (Title, passwords) VALUES (%s, %s)"
            user_data = ("Encryption", password) 
            cursor.execute(insert_query, user_data)
            connection.commit()
            root_password.destroy()  # Close the window after saving

    def get_password():
        connection = mydb
        cursor = connection.cursor()

        global new_password_entry, confirm_password_entry, root_password
        root_password = tk.Tk()
        root_password.title("Password Entry")
        
        new_pwd_lbl = tk.Label(root_password, text="New Password:")
        new_pwd_lbl.grid(row=0, column=0)
        new_password_entry = tk.Entry(root_password, show='*')
        new_password_entry.grid(row=0, column=1)

        conf_pwd_lbl = tk.Label(root_password, text="Confirm Password:")
        conf_pwd_lbl.grid(row=1, column=0)
        confirm_password_entry = tk.Entry(root_password, show='*')
        confirm_password_entry.grid(row=1, column=1)

        save_button = tk.Button(root_password, text="Save", command=save_password)
        save_button.grid(row=2, columnspan=2)
        root_password.mainloop()

    get_password()


#To check if entered password matches for accessing files of the Private Folder    
def check_password():
    new_password=""
    password = simpledialog.askstring("Password", "Enter password:", show='*')
    connection = mydb
    cursor = connection.cursor()

    select_query = "SELECT Passwords FROM Passwords WHERE Title = %s"
    title_to_search = ("Folder",)

    cursor.execute(select_query, title_to_search)

    rows = cursor.fetchall()

    if rows:
        
        for row in rows:
            new_password = row[0]
            
    if password == new_password:
        mb.showinfo("Success", "Correct password entered!")
    else:
        mb.showerror("Error", "Incorrect password.")


#To prompt user to enter the decryption password to decrypt files
def onetime_get_password():
    root = tk.Tk()
    root.withdraw()
    password = simpledialog.askstring("Password", "Enter the decryption password:", show='*')
    return password

#To check if folder is accessible within the given time
def check_timer():
    main_window = Tk()
    #global minutes
    global file_path

    current_time = datetime.now().time()
    start_time = datetime.now().strftime("%H:%M")
    connection = mydb
    cursor = connection.cursor()
    select_query = "SELECT Duration FROM AccessTime"
    cursor.execute(select_query)
    row = cursor.fetchone()

    if row:
        minutes = row[0]
    end_time = (datetime.strptime(start_time, "%H:%M") + timedelta(minutes=minutes)).strftime("%H:%M")
    
    def update_countdown(remaining_time, label):
        if remaining_time > 0:
            minutes, seconds = divmod(remaining_time, 60)
            hours, minutes = divmod(minutes, 60)
            label.config(text=f"Time Remaining: {hours:02d}:{minutes:02d}:{seconds:02d}")
            main_window.after(1000, update_countdown, remaining_time - 1, label)

    if start_time <= end_time:
        file_path = filedialog.askopenfilename()
        
        
        password = onetime_get_password()
        connection = mydb
        cursor = connection.cursor()

        select_query = "SELECT Passwords FROM Passwords WHERE Title = %s"
        title_to_search = ("Encryption",)

        cursor.execute(select_query, title_to_search)

        rows = cursor.fetchall()

        if rows:
            for row in rows:
                new_password = row[0] 
        if(password ==new_password):
            outfilename = file_path+"decrypt"
        
        with open(file_path, 'rb') as infile, open(outfilename, 'wb') as outfile:
            tfdecrypt(infile, outfile, new_password)

        subprocess.Popen(['notepad', outfilename], creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        countdown_label = Label(main_window, text="Time Remaining: 00:00:00")
        countdown_label.place(relx=0.3, rely=0.9)
        
        remaining_time = (datetime.strptime(end_time, "%H:%M") - datetime.strptime(start_time, "%H:%M")).seconds
        update_countdown(remaining_time, countdown_label)
        
        # Terminate Notepad after a specific time (in seconds)
        def terminate_notepad():
            os.system('taskkill /f /im notepad.exe')  # Kill the Notepad process
            countdown_label.config(text="Time's Up!")  # Display 'Time's Up!' after file access time is over
            try:
                os.path.exists(outfilename)
                os.remove(outfilename)
                print(f"File '{outfilename}' deleted.")
            except:
                print(f"File '{outfilename}' not found.")            
        main_window.after(remaining_time * 1000, terminate_notepad)  # Schedule to terminate after remaining_time seconds
    main_window.mainloop()

#To set the number of minutes to access the Time based access folder
def mins():

    def get_minutes():
       
        try:
            connection=mydb
            cursor = connection.cursor()
            minutes = int(entry.get())
            mb.showinfo("Success", f"Entered minutes: {minutes}")
            insert_query = "INSERT INTO AccessTime (Duration) VALUES (%s)"
            user_data = (minutes,) 
            cursor.execute(insert_query, user_data)
            connection.commit()
            root.destroy()
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
    root.mainloop()
    

#To open the required file
def Open():
    global file_path
    folder_path = filedialog.askdirectory()
    current_directory = os.getcwd()
    a=current_directory+"\private_folder"
    b=current_directory+"\\time_access"
    a= a.replace("\\","/")
    b=b.replace("\\","/")
    print(folder_path)
    print("B",b)
    if (folder_path==a):
        check_password()
        file_path = filedialog.askopenfilename()
        
        OTP_Create()
        
    elif(folder_path==b):
        print("in elif")
        check_timer()
 
    else:
        file_path = filedialog.askopenfilename()
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


def CreateFolder():
    global NewFolder
    global Folder

    Folder = filedialog.askdirectory()
    print("Enter a name for the folder")
    NewFolder = input()
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

#To create two folders-private_folder & time_access on first time usage of the application
def create_folders():
    folders = ['private_folder', 'time_access']
    for folder_name in folders:
        folder_path = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
create_folders()  #to initialise two folders-private & timebased
current_directory = os.getcwd()
folder_to_protect = os.path.join(current_directory, "private_folder")
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
count=0
while (count<3):
    count+=1
    a=(tables[0])
    if (count==1):  
        if (a==None):
            mins()
    if (count==2):
        if (a==None):
            create_password_encrypt()
            create_pw_folder()


#Asking confirmation to close the application
def on_closing():
    if mb.askokcancel("Quit", "Do you want to quit?"):
        Screen.destroy()

Screen = Tk()
Screen.title("File Explorer")
Screen.protocol("WM_DELETE_WINDOW", on_closing)
# Create a frame for the buttons
button_frame = Frame(Screen, bg="pink")
button_frame.pack(padx=20, pady=20)

# Define and place buttons in the frame using grid layout
buttons = [
    ("Create file", Save),
    ("Create Folder", CreateFolder),
    ("Open", Open),
    ("Rename", Rename),
    ("Copy", Copy),
    ("Move File", MoveFile),
    ("Delete File", Delete),
    ("Delete Folder", DeleteFolder),
    
]

for i, (text, command) in enumerate(buttons):
    button = tk.Button(button_frame, text=text, command=command)
    button.grid(row=i, column=0, pady=5, padx=10, sticky="ew")
Screen.mainloop()
