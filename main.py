import tkinter
from tkinter import *
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pydub import AudioSegment
from pydub.playback import play
import os
from wave import open as wave_open
import pygame
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import font

def center_window(width=300, height=200):
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    splash_root.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Splash screen
splash_root = Tk()
center_window(900, 600)
splash_root.overrideredirect(True)
splash_root.columnconfigure(0, weight=3)

app_name = Label(text="AUDIO TSUKOYOMI!!!", font=("Game Of Squids", 25))
app_name.grid(column=0, row=0)

dev_team_label = Label(text="Developed by LegionX", font=("Game Of Squids", 20))
dev_team_label.grid(column=0, row=1)

image = Image.open("resources/itachi2.jpg")
photo = ImageTk.PhotoImage(image.resize((650, 350), Image.LANCZOS))
img_label = Label(splash_root, image=photo)
img_label.image = photo
img_label.grid(column=0, row=2)

open_gif = Image.open("resources/sharingan.gif")
frames = open_gif.n_frames
imageObj = [PhotoImage(file="resources/sharingan.gif", format=f"gif -index {i}") for i in range(frames)]

showAnimation = None

def animation(count=0):
    global showAnimation
    newImage = imageObj[count]
    loading_label.configure(image=newImage)
    count += 1
    if count == frames:
        count = 0
    showAnimation = splash_root.after(50, animation, count)

loading_label = Label(splash_root, image="")
loading_label.grid(row=3)
animation(count=0)




def pause_audio():
    # Pause any existing playback
    pygame.mixer.pause()

def save_sound(filename, data, sound):
    with wave_open(filename, 'wb') as output_file:
        output_file.setnchannels(sound.channels)
        output_file.setsampwidth(sound.sample_width)
        output_file.setframerate(sound.frame_rate)
        output_file.writeframes(data)

def play_audio(audio_data, progress_bar):
    # Stop any existing playback
    pygame.mixer.stop()

    # Create a temporary sound object
    temp_sound = pygame.mixer.Sound(buffer=audio_data)

    # Get the sound duration in milliseconds
    duration = int(len(audio_data) / (44100 * 2) * 1000)

    # Reset progress bar
    progress_bar["value"] = 0
    progress_bar["maximum"] = duration

    # Function to update progress bar during playback
    def update_progress():
        current_time = pygame.mixer.music.get_pos()
        progress_bar["value"] = current_time
        if current_time < duration:
            root.after(100, lambda: update_progress())

    # Play the temporary sound
    temp_sound.play()

    # Update progress bar
    update_progress()

def process_sound_encrypt():
    key_encrypt = aes_key_entry.get()
    filename = filedialog.askopenfilename(title="Select a sound file", filetypes=[("Wave files", "*.wav")])

    if not filename:
        return

    try:
        sound = AudioSegment.from_wav(filename)
        sound_data = sound.raw_data

        iv = os.urandom(16)
        cipher = AES.new(key_encrypt.encode("utf-8"), AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(pad(sound_data, AES.block_size))

        # Save the encrypted sound to a temporary file
        encrypted_filename = "encrypted_sound.wav"
        save_sound(encrypted_filename, iv + encrypted_data, sound)

        # Display a message that encryption is complete
        messagebox.showinfo("Info", "Encrypted sound has been saved.")

        # Optionally, provide buttons for the user to play and pause the encrypted sound
        play_button = Button(root, text="Play Encrypted Sound",
                            command=lambda: play_audio(iv + encrypted_data, result_progress))
        play_button.place(x=1200, y=480)  # Adjust the coordinates based on your preference

        pause_button = Button(root, text="Pause Encrypted Sound", command=pause_audio)
        pause_button.place(x=1200, y=520)  # Adjust the coordinates based on your preference

    except Exception as e:
        messagebox.showerror("Error", f"Error encrypting sound: {str(e)}")

def process_sound_decrypt():
    key_decrypt = aes_key_entry.get()
    filename = filedialog.askopenfilename(title="Select an encrypted sound file", filetypes=[("Wave files", "*.wav")])

    if not filename:
        return

    try:
        sound = AudioSegment.from_wav(filename)
        encrypted_sound_data = sound.raw_data

        iv = encrypted_sound_data[:16]
        encrypted_data = encrypted_sound_data[16:]

        cipher = AES.new(key_decrypt.encode("utf-8"), AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        # Save the decrypted sound to a temporary file
        decrypted_filename = "decrypted_sound.wav"
        save_sound(decrypted_filename, decrypted_data, sound)

        # Display a message that decryption is complete
        messagebox.showinfo("Info", "Decrypted sound has been saved.")

        # Optionally, provide buttons for the user to play and pause the decrypted sound
        play_button = Button(root, text="Play Decrypted Sound",
                             command=lambda: play_audio(decrypted_data, result_progress))
        play_button.place(x=90, y=480)  # Adjust the coordinates based on your preference

        pause_button = Button(root, text="Pause Decrypted Sound", command=pause_audio)
        pause_button.place(x=90, y=520)  # Adjust the coordinates based on your preference

    except Exception as e:
        messagebox.showerror("Error", f"Error decrypting sound: {str(e)}")




    def move_labels():
        new_x_image = 100  # New x-coordinate for imageLabel
        new_y_image = 100  # New y-coordinate for imageLabel
        image_label.place(x=new_x_image, y=new_y_image)

        new_x_result = 200  # New x-coordinate for resultImgLabel
        new_y_result = 100  # New y-coordinate for resultImgLabel
        result_img_label.place(x=new_x_result, y=new_y_result)



# Main window
def main_window():
    global root, aes_key_entry, result_progress
    splash_root.after_cancel(showAnimation)
    splash_root.destroy()

    root = Tk()
    root.title("🎧 Audio Encryption 🎶")
    root.geometry("800x600")
    root.configure(bg="#000000")

    # Set the window to fullscreen
    root.attributes("-fullscreen", True)

    # Center the window on the screen
    root.geometry("+{}+{}".format(int((root.winfo_screenwidth() - root.winfo_reqwidth()) / 2),
                                   int((root.winfo_screenheight() - root.winfo_reqheight()) / 2)))

    # Add an Exit button
    exit_button = Button(root, text="🏃 Exit", command=root.destroy, font=("Pacifico", 16),
                         background="#FF5733", foreground="#ffffff")
    exit_button.pack(side="top", padx=10, pady= 20, anchor="ne")

    header_font = font.Font(family='Khumairoh', size=50, weight='bold')

    header_label = Label(root, text="LegionX\nAudio Encryption and Decryption", font=header_font,
                         foreground="#f1f1f1", background="#000000")
    header_label.pack(pady=20)

    # Modify the place coordinates for imageLabel
    image_label = Label(root, width=30, height=10, background="#000000", highlightbackground='white',
                        highlightthickness=2)
    image_label.place(x=90, y=480)  # Set the initial coordinates for imageLabel

    # Add resultImgLabel and set its initial coordinates
    result_img_label = Label(root, width=30, height=10, background="#000000", highlightbackground='white',
                             highlightthickness=2)
    result_img_label.place(x=1200, y=480)  # Set the initial coordinates for resultImgLabel

    subheading_font = font.Font(family='Luckitto', size=30, weight='bold')

    subheading_label = Label(root, text="Welcome to our Secret Lab!", font=subheading_font, pady=20,
                             foreground="#ffffff", background="#000000")
    subheading_label.pack()

    aes_key_label = Label(root, text="Enter AES Key:", font=("Luckitto", 30), foreground="#ffffff", background="#000000")
    aes_key_label.pack(pady=10)

    aes_key_entry = Entry(root, show="", font=("Pacifico", 25), background="#333333", foreground="#ffffff",
                          borderwidth=0, justify='center', width=20)
    aes_key_entry.insert(0, "Enter your key")
    aes_key_entry.pack(pady=10)

    encrypt_button = Button(root, text="🔒 Encrypt Sound", command=process_sound_encrypt, font=("Pacifico", 16), background="#4CAF50", foreground="#ffffff")
    encrypt_button.pack(pady=20, padx=110, side=LEFT)

    decrypt_button = Button(root, text="🔓 Decrypt Sound", command=process_sound_decrypt, font=("Pacifico", 16),
                            background="#FF5733", foreground="#ffffff")
    decrypt_button.pack(pady=20, padx=140, side=RIGHT)

    # Initialize pygame mixer
    pygame.mixer.init()
    # Add progress bars for audio playback
    image_progress = ttk.Progressbar(root, mode="determinate", length=220)
    image_progress.place(x=90, y=600, anchor="w")

    result_progress = ttk.Progressbar(root, mode="determinate", length=220)
    result_progress.place(x=1200, y=600, anchor="w")


# After 3000 milliseconds (3 seconds), close the splash screen and open the main window
splash_root.after(3000, main_window)
splash_root.mainloop()


