from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


class Interface:

    def __init__(self):
        self.window = Tk()
        self.window.title("ODIN Demo")
        self.window.config(padx=20, pady=20)
        canvas = Canvas(width=500, height=280)
        canvas.grid(row=0, column=0, columnspan=2)
        tomcat = PhotoImage(file="Assets/rsz_mig_chomper.png")
        canvas.create_image(250, 140, image=tomcat)

        file_open_button = Button(text="Open Image", width=20, command=self.open_file)
        file_open_button.grid(row=1, column=0, sticky=W)

        self.img_path_label = Label(text="Select an image file using the button above.")
        self.img_path_label.grid(row=2, column=0, columnspan=2, sticky=W, pady=10)

        line_label = Label(text="--------------------------------------------------------------------------------------"
                                "---------------------")
        line_label.grid(row=3, column=0, columnspan=3, pady=10)

        instruction_label1 = Label(text="Enter the required information below:")
        instruction_label1.grid(row=4, column=0, columnspan=2, sticky=W, pady=10)

        cam_lat_instruction = Label(text="Camera Latitude Degrees: ")
        cam_lat_instruction.grid(row=5, column=0, sticky=W, pady=10)

        self.cam_lat_d = Entry(width=50)
        self.cam_lat_d.focus()
        self.cam_lat_d.grid(row=5, column=1, columnspan=2, pady=10, sticky=W)

        cam_lat_instruction2 = Label(text="Camera Latitude Minutes: ")
        cam_lat_instruction2.grid(row=6, column=0, sticky=W, pady=10)

        self.cam_lat_m = Entry(width=50)
        self.cam_lat_m.grid(row=6, column=1, columnspan=2, pady=10, sticky=W)

        cam_lat_instruction3 = Label(text="Camera Latitude Seconds: ")
        cam_lat_instruction3.grid(row=7, column=0, sticky=W, pady=10)

        self.cam_lat_s = Entry(width=50)
        self.cam_lat_s.grid(row=7, column=1, columnspan=2, pady=10, sticky=W)

        cam_lon_instruction = Label(text="Camera Longitude Degrees: ")
        cam_lon_instruction.grid(row=8, column=0, sticky=W, pady=10)

        self.cam_lon_d = Entry(width=50)
        self.cam_lon_d.grid(row=8, column=1, columnspan=2, pady=10, sticky=W)

        cam_lon_instruction2 = Label(text="Camera Longitude Minutes: ")
        cam_lon_instruction2.grid(row=9, column=0, sticky=W, pady=10)

        self.cam_lon_m = Entry(width=50)
        self.cam_lon_m.grid(row=9, column=1, columnspan=2, pady=10, sticky=W)

        cam_lon_instruction3 = Label(text="Camera Longitude Seconds: ")
        cam_lon_instruction3.grid(row=10, column=0, sticky=W, pady=10)

        self.cam_lon_s = Entry(width=50)
        self.cam_lon_s.grid(row=10, column=1, columnspan=2, pady=10, sticky=W)

        cam_elev_instruction = Label(text="Camera Elevation in Degrees: ")
        cam_elev_instruction.grid(row=11, column=0, sticky=W, pady=10)

        self.cam_elev = Entry(width=50)
        self.cam_elev.grid(row=11, column=1, columnspan=2, pady=10, sticky=W)

        cam_az_instruction = Label(text="Camera Azimuth: ")
        cam_az_instruction.grid(row=12, column=0, sticky=W, pady=10)

        self.cam_az = Entry(width=50)
        self.cam_az.grid(row=12, column=1, columnspan=2, pady=10, sticky=W)

        cam_alt_instruction = Label(text="Camera altitude in Feet: ")
        cam_alt_instruction.grid(row=13, column=0, sticky=W, pady=10)

        self.cam_alt = Entry(width=50)
        self.cam_alt.grid(row=13, column=1, columnspan=2, pady=10, sticky=W)

        process_image_button = Button(text="Process Image", width=20, command=self.process_button_tester)
        process_image_button.grid(row=14, column=2, sticky=E)

        self.window.mainloop()

    def open_file(self):
        self.window.filename = filedialog.askopenfilename(initialdir="Assets/test_imgs",
                                                          title="Select a file",
                                                          filetypes=(("jpg files", "*.jpg"),
                                                                     ("png files", "*.png"),
                                                                     ("all files", "*.*"),
                                                                     ),
                                                          )
        self.img_path_label.destroy()
        self.img_path_label = Label(text=f"Selected file: {self.window.filename}")
        self.img_path_label.grid(row=2, column=0, columnspan=2, sticky=W, pady=10)

    def process_button_tester(self):
        print(self.cam_lat_d.get())
        print(self.cam_lat_m.get())
        print(self.cam_lat_s.get())
        print(self.cam_lon_d.get())
        print(self.cam_lon_m.get())
        print(self.cam_lon_s.get())
        print(self.cam_elev.get())
        print(self.cam_az.get())
        print(self.cam_alt.get())


ui = Interface()
