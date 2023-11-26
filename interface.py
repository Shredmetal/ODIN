import json
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from models import Models
from pos_calcs import PositionCalculator


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

        cam_lat_instruction4 = Label(text="Camera Latitude Hemisphere (N / S): ")
        cam_lat_instruction4.grid(row=8, column=0, sticky=W, pady=10)

        self.cam_lat_h = Entry(width=50)
        self.cam_lat_h.grid(row=8, column=1, columnspan=2, pady=10, sticky=W)

        cam_lon_instruction = Label(text="Camera Longitude Degrees: ")
        cam_lon_instruction.grid(row=9, column=0, sticky=W, pady=10)

        self.cam_lon_d = Entry(width=50)
        self.cam_lon_d.grid(row=9, column=1, columnspan=2, pady=10, sticky=W)

        cam_lon_instruction2 = Label(text="Camera Longitude Minutes: ")
        cam_lon_instruction2.grid(row=10, column=0, sticky=W, pady=10)

        self.cam_lon_m = Entry(width=50)
        self.cam_lon_m.grid(row=10, column=1, columnspan=2, pady=10, sticky=W)

        cam_lon_instruction3 = Label(text="Camera Longitude Seconds: ")
        cam_lon_instruction3.grid(row=11, column=0, sticky=W, pady=10)

        self.cam_lon_s = Entry(width=50)
        self.cam_lon_s.grid(row=11, column=1, columnspan=2, pady=10, sticky=W)

        cam_lon_instruction4 = Label(text="Camera Longitude Hemisphere (E / W): ")
        cam_lon_instruction4.grid(row=12, column=0, sticky=W, pady=10)

        self.cam_lon_h = Entry(width=52)
        self.cam_lon_h.grid(row=12, column=1, columnspan=2, pady=10, sticky=W)

        cam_elev_instruction = Label(text="Camera Elevation in Degrees: ")
        cam_elev_instruction.grid(row=13, column=0, sticky=W, pady=10)

        self.cam_elev = Entry(width=50)
        self.cam_elev.grid(row=13, column=1, columnspan=2, pady=10, sticky=W)

        cam_az_instruction = Label(text="Camera Azimuth: ")
        cam_az_instruction.grid(row=14, column=0, sticky=W, pady=10)

        self.cam_az = Entry(width=50)
        self.cam_az.grid(row=14, column=1, columnspan=2, pady=10, sticky=W)

        cam_alt_instruction = Label(text="Camera altitude in Feet: ")
        cam_alt_instruction.grid(row=15, column=0, sticky=W, pady=10)

        self.cam_alt = Entry(width=50)
        self.cam_alt.grid(row=15, column=1, columnspan=2, pady=10, sticky=W)

        process_image_button = Button(text="Process Image", width=20, command=self.process_button)
        process_image_button.grid(row=16, column=2, sticky=E)

        self.lat_d = None
        self.lat_m = None
        self.lat_s = None
        self.lat_h = None
        self.lon_d = None
        self.lon_m = None
        self.lon_s = None
        self.lon_h = None
        self.elev = None
        self.az = None
        self.alt = None
        self.img_path = None

        self.models = Models()
        self.pos_calc = PositionCalculator()

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
        self.img_path = self.window.filename
        self.img_path_label = Label(text=f"Selected file: {self.window.filename}")
        self.img_path_label.grid(row=2, column=0, columnspan=2, sticky=W, pady=10)

    def process_button(self):

        self.lat_d = float(self.cam_lat_d.get())
        self.lat_m = float(self.cam_lat_m.get())
        self.lat_s = float(self.cam_lat_s.get())
        self.lat_h = self.cam_lat_h.get()
        self.lon_d = float(self.cam_lon_d.get())
        self.lon_m = float(self.cam_lon_m.get())
        self.lon_s = float(self.cam_lon_s.get())
        self.lon_h = self.cam_lon_h.get()
        self.elev = float(self.cam_elev.get())
        self.az = float(self.cam_az.get())
        self.alt = float(self.cam_alt.get())

        self.models.det_clf(self.img_path)
        self.pos_calc.sns_data_input(lat_d=self.lat_d,
                                     lat_m=self.lat_m,
                                     lat_s=self.lat_s,
                                     lat_h=self.lat_h,
                                     lon_d=self.lon_d,
                                     lon_m=self.lon_m,
                                     lon_s=self.lon_s,
                                     lon_h=self.lon_h,
                                     elev=self.elev,
                                     az=self.az,
                                     alt=self.az,
                                     ac_type=self.models.ac_type,
                                     x_ctr=self.models.x_ctr,
                                     y_ctr=self.models.y_ctr,
                                     x_sz=self.models.x_sz,
                                     y_sz=self.models.y_sz,
                                     box_left=self.models.box_left,
                                     box_right=self.models.box_right,
                                     box_bottom=self.models.box_bottom,
                                     box_top=self.models.box_top,
                                     )
        self.pos_calc.tgt_pos_calc()

        tgt_pos_dict = {"Coordinates": self.pos_calc.tgt_coords, "Altitude": self.pos_calc.tgt_alt}

        with open(f"preds/{self.models.pred_ref}.json", "w") as file:
            json.dump(tgt_pos_dict, file)

        print(tgt_pos_dict)
        print(self.models.ac_type)


ui = Interface()
