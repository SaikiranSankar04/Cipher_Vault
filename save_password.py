import tkinter as tk
from tkinter import messagebox as mb

new_password = None
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


def save_password():
    global new_password
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()

    if new_password == confirm_password:
        mb.showinfo("Success", "Password saved: " + new_password)
        root_password.destroy()
    else:
        mb.showerror("Error", "Passwords do not match.")

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

# Example usage:
get_password()
with open('infile.txt', 'r') as infile, open('outfile.txt', 'wb') as outfile:
    tfencrypt(infile, outfile, new_password)

with open('outfile.txt', 'rb') as infile, open('outfile_decrypted.txt', 'wb') as outfile:
    tfdecrypt(infile, outfile, new_password)

