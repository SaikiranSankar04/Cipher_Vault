The safeguarding of sensitive data is becoming more and more important as the digital world changes. 
In our project **CipherVault**, we implement the TwoFish algorithm in Python to create a secure file management application.

**Contents**  


I. Description  
II. Design  
III. How to install and run the application locally on your device

**I. Description**

Modules used:   

|FUNCTION                  | MODULES USED
|:-------------------------| :----------------
|GUI 	                     | Tkinter, easygui    |
|File Handling	            | Os, shutil          |
|Cryptography	            | Twofish             |
|System Operations	      | Subprocess, psutil  |
|Time Operations	         | Time, datetime      |
|Database Connectivity	   | mysql,connector     |
|Emails	                  | smtplib             |
|OTP & 2FA	               | pyotp               |







**II. Design**

**High level design**

![image](https://github.com/SaikiranSankar04/Cipher_Vault/assets/128061632/497f8255-7fc3-45ce-928f-fefcd64a89bd)

**Low level design**

![image](https://github.com/SaikiranSankar04/Cipher_Vault/assets/128061632/db17c1d0-5b1b-435b-8434-5f3e59e55a75)

File Manager features:
1. Private folder:
   verify the password when opening folder
   create files and folder in this folder
   to access files in the folder use OTP verification
2. Time based access:
   a folder that can be accessed only during the specified time


PASSWORD:
1. PRIVATE FOLDER PASSWORD: to access the
2. ENCRYPTION PASSWORD: for all files- to save and open, modify...call when you use encrypt
