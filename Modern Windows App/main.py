import time
import customtkinter as ctk         # used to display GUI window...to install use "pip install customtkinter"
from CTkMessagebox import CTkMessagebox  # used to display GUI popup window...to install use "pip install CTkMessagebox"
from PIL import Image               # used to display background
import webbrowser                   # used to open browser window to see onboard RC car
import socket                       # used to send messages to ESP32




# Create an instance of tkinter frame or window
window = ctk.CTk()
window.title("RC Car App")
ctk.set_appearance_mode("dark")


# Set the size of the window
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))


# Create three frames in the window
header = ctk.CTkFrame(window, fg_color='black')
content = ctk.CTkFrame(window)
footer = ctk.CTkFrame(window, fg_color='black')

window.columnconfigure(0, weight=1)  # 100%
window.rowconfigure(0, weight=1)  # 5%
window.rowconfigure(1, weight=18)  # 90%
window.rowconfigure(2, weight=1)  # 5%
header.grid(row=0, sticky='news')
content.grid(row=1, sticky='news')
footer.grid(row=2, sticky='news')

# Create a client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
clientSocket.connect(("192.168.18.139", 4080))

connectFlag = 0
contentFlag = 0
drivingElapsedFlag = 0


def connect_function():
    global connectFlag
    if connectFlag == 0:
        connectButtonText.set("Disconnect from RC Car")
        connectFlag = 1
        show_content()
    else:
        connectButtonText.set("Connect to RC Car")
        connectFlag = 0
        show_content()


def show_content():
    global contentFlag
    if contentFlag == 0:
        webbrowser.open("http://192.168.18.144/")       # open up default browser to requested URL
        contentFlag = 1
    else:
        contentFlag = 0


# Index for RC Car movement:
#
# "1" sent to steer car left..."2" sent to reset steering
# "3" sent to steer car right..."2" sent to reset steering
# "5" sent to move car backwards..."6" sent to stop movement
# "7" sent to move car forwards..."8" sent to stop movement

def time_elapsed(steering):
    global drivingElapsedFlag
    if steering == 'forward' or steering == 'back':
        time.sleep(1)
        data = "6"
        clientSocket.send(data.encode())
        drivingElapsedFlag = 0


def left_button_pressed():
    global connectFlag
    if connectFlag == 1:
        data = "1"
        clientSocket.send(data.encode())


def middle_button_pressed():
    global connectFlag
    if connectFlag == 1:
        data = "2"
        clientSocket.send(data.encode())


def right_button_pressed():
    global connectFlag
    if connectFlag == 1:
        data = "3"
        clientSocket.send(data.encode())


def back_button_pressed():
    global drivingElapsedFlag
    global connectFlag
    if connectFlag == 1:
        if drivingElapsedFlag == 0:
            # Send data to server
            data = "5"
            clientSocket.send(data.encode())
            drivingElapsedFlag = 1
            time_elapsed('back')


def forward_button_pressed():
    global drivingElapsedFlag
    global connectFlag
    if connectFlag == 1:
        if drivingElapsedFlag == 0:
            # Send data to server
            data = "7"
            clientSocket.send(data.encode())
            drivingElapsedFlag = 1
            time_elapsed('forward')


def speed50_button_pressed():
    # Send data to server
    global connectFlag
    if connectFlag == 1:
        data = "B"
        clientSocket.send(data.encode())
        CTkMessagebox(title="Note!", message="Speed changed to 50%")


def speed75_button_pressed():
    # Send data to server
    global connectFlag
    if connectFlag == 1:
        data = "C"
        clientSocket.send(data.encode())
        CTkMessagebox(title="Note!", message="Speed changed to 75%")


def speed100_button_pressed():
    # Send data to server
    global connectFlag
    if connectFlag == 1:
        data = "D"
        clientSocket.send(data.encode())
        CTkMessagebox(title="Note!", message="Speed changed to 100%")


# Show background using label
bg = ctk.CTkImage(dark_image=Image.open("background.png"), size=(1920,812))
label2 = ctk.CTkLabel(content, image=bg, text="")
label2.place(x=0, y=0)


# Add a button to switch between two frames
connectButtonText = ctk.StringVar()
connectButtonText.set("Connect to RC Car")
font1 = ctk.CTkFont(family='<Calibri>', size=15, weight='bold')
btn1 = ctk.CTkButton(header, textvariable=connectButtonText, font=font1, command=connect_function)
btn1.pack(pady=20)

# footer instructions
# setting image buttons
leftTriangle = ctk.CTkImage(dark_image=Image.open("left_triangle.png"))
leftButton = ctk.CTkButton(footer, text='Steer left!', image=leftTriangle, compound=ctk.LEFT, command=left_button_pressed)
leftButton.pack(padx=20, side=ctk.LEFT)

blackCircle = ctk.CTkImage(dark_image=Image.open("black_circle.png"))
middleButton = ctk.CTkButton(footer, text='Reset steering!', image=blackCircle, compound=ctk.LEFT, command=middle_button_pressed)
middleButton.pack(padx=20, side=ctk.LEFT)

rightTriangle = ctk.CTkImage(dark_image=Image.open("right_triangle.png"))
rightButton = ctk.CTkButton(footer, text='Steer right!', image=rightTriangle, compound=ctk.LEFT, command=right_button_pressed)
rightButton.pack(padx=20, side=ctk.LEFT)

upTriangle = ctk.CTkImage(dark_image=Image.open("up_triangle.png"))
forwardButton = ctk.CTkButton(footer, text='Move forwards!', image=upTriangle, compound=ctk.LEFT, command=forward_button_pressed)
forwardButton.pack(padx=20, side=ctk.RIGHT)

downTriangle = ctk.CTkImage(dark_image=Image.open("down_triangle.png"))
backButton = ctk.CTkButton(footer, text='Move backwards!', image=downTriangle, compound=ctk.LEFT, command=back_button_pressed)
backButton.pack(padx=20, side=ctk.RIGHT)


# speed buttons
font2 = ctk.CTkFont(family='<Calibri>', size=20, weight='bold')            # font used for speed buttons and footer text
radio_var = ctk.IntVar(value=2)                         # used to ensure that only one checkbox can be checked at a time
speed100Button = ctk.CTkRadioButton(footer, text="Speed: 100%", command=speed100_button_pressed,
                                    variable=radio_var, value=0, font=font2)
speed100Button.pack(side=ctk.BOTTOM)

speed75Button = ctk.CTkRadioButton(footer, text="Speed: 75%", command=speed75_button_pressed,
                                   variable=radio_var, value=1, font=font2)
speed75Button.pack(side=ctk.BOTTOM)

speed50Button = ctk.CTkRadioButton(footer, text="Speed: 50%", command=speed50_button_pressed,
                                   variable=radio_var, value=2, font=font2)
speed50Button.pack(side=ctk.BOTTOM)


label4 = ctk.CTkLabel(footer, text="Can also use arrow keys to move and steer RC Car", font=font2, text_color='red')
label4.pack(side=ctk.TOP)


window.bind('<Left>', lambda event: left_button_pressed())
window.bind('<space>', lambda event: middle_button_pressed())
window.bind('<Right>', lambda event: right_button_pressed())
window.bind('<Down>', lambda event: back_button_pressed())
window.bind('<Up>', lambda event: forward_button_pressed())

window.mainloop()
