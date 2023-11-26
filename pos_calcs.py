import pandas as pd
from math import sin, cos, tan, pi
from geographiclib.geodesic import Geodesic

# Horizontal Field of view of camera
FOV = 78
# Get degrees per pixel
DPP = (FOV / 2560)
# vertical pixel count
VPIX = 1440
# horizontal pixel count
HPIX = 2560

df = pd.read_csv("Assets/type_data.csv")


class PositionCalculator:

    def __init__(self):

        # initialise all sensor information
        self.sns_lat = None
        self.sns_lat_d = None
        self.sns_lat_m = None
        self.sns_lat_s = None
        self.sns_lon = None
        self.sns_lon_d = None
        self.sns_lon_m = None
        self.sns_lon_s = None
        self.sns_elev = None
        self.sns_az = None
        self.sns_alt = None
        self.sns_lat_h = None
        self.sns_lon_h = None

        # initialise aircraft database
        self.df = pd.read_csv("Assets/type_data.csv")

        # Initialise attributes to be populated by the models
        self.x_ctr = None
        self.y_ctr = None
        self.x_sz = None
        self.y_sz = None
        self.box_left = None
        self.box_right = None
        self.box_bottom = None
        self.box_top = None
        self.ac_type = None  # get this from the models class

        # Initialise attributes to be calculated
        self.tgt_coords = None
        self.tgt_alt = None

    def sns_data_input(self, lat_d, lat_m, lat_s, lat_h, lon_d, lon_m, lon_s, lon_h, elev, az, alt, ac_type, x_ctr,
                       y_ctr, x_sz, y_sz, box_left, box_right, box_bottom, box_top):

        # populate attributes with sensor data
        self.sns_lat_d = lat_d
        self.sns_lat_m = lat_m
        self.sns_lat_s = lat_s
        self.sns_lat_h = lat_h
        self.sns_lon_d = lon_d
        self.sns_lon_m = lon_m
        self.sns_lon_s = lon_s
        self.sns_lon_h = lon_h
        self.sns_elev = elev
        self.sns_az = az
        self.sns_alt = alt
        self.ac_type = ac_type

        # populate attributes with modelling results

        self.x_ctr = x_ctr
        self.y_ctr = y_ctr
        self.x_sz = x_sz
        self.y_sz = y_sz
        self.box_left = box_left
        self.box_right = box_right
        self.box_bottom = box_bottom
        self.box_top = box_top

    def tgt_pos_calc(self):

        abs_dist = self.get_distance(self.df, self.ac_type, self.x_sz)
        hz_dist = self.get_horizontal_distance(abs_dist, self.sns_elev, self.y_ctr)
        azimuth = self.get_azimuth(self.sns_az, self.x_ctr)
        self.sns_lat = self.dms_to_dd(self.sns_lat_d, self.sns_lat_m, self.sns_lat_s, self.sns_lat_h)
        self.sns_lon = self.dms_to_dd(self.sns_lon_d, self.sns_lon_m, self.sns_lon_s, self.sns_lon_h)

        self.tgt_coords = self.get_tgt_coords(hz_dist, azimuth, self.sns_lat, self.sns_lon)
        self.tgt_alt = self.get_altitude(abs_dist, self.sns_elev, self.sns_alt, self.y_ctr)

        pass

    def get_distance(self, type_df, ac_type, pix_width, dpp=DPP):
        spanxlength = type_df.loc[type_df["type"] == ac_type, "spanxlength"].iloc[0]
        trg_opp = (spanxlength / 2)
        width = float(pix_width.cpu())
        trg_theta = ((width * dpp) / 2)
        trg_adj = (trg_opp / (tan((trg_theta * pi) / 180)))
        return trg_adj

    def get_altitude(self, distance, cam_elev, cam_alt, y_ctr, ypix=VPIX, dpp=DPP):
        y_ctr = (float(y_ctr.cpu()) * dpp)
        bottom_y_cam = cam_elev - ((ypix / 2) * dpp)
        trg_theta = bottom_y_cam + y_ctr
        trg_hyp = distance
        trg_opp = (trg_hyp * (sin((trg_theta * pi) / 180)))
        return (trg_opp * 3.28084) + cam_alt

    def get_horizontal_distance(self, distance, cam_elev, y_ctr, ypix=VPIX, dpp=DPP):
        y_ctr = (float(y_ctr.cpu()) * dpp)
        bottom_y_cam = cam_elev - ((ypix / 2) * dpp)
        trg_theta = bottom_y_cam + y_ctr
        trg_hyp = distance
        trg_adj = (trg_hyp * (cos((trg_theta * pi) / 180)))
        return trg_adj

    def get_azimuth(self, cam_az, x_ctr, xpix=HPIX, dpp=DPP):
        x_ctr = (float(x_ctr.cpu()) * dpp)
        left_x_cam = cam_az - ((xpix / 2) * dpp)
        tgt_az = (left_x_cam + x_ctr) % 360
        return tgt_az

    def dms_to_dd(self, d, m, s, NE):
        dd = d + float(m) / 60 + float(s) / 3600
        if NE == "S" or NE == "W":
            dd *= -1
        return dd

    def get_tgt_coords(self, hz_dst, az, cam_lat, cam_long):
        geo_obj = Geodesic.WGS84.Direct(cam_lat, cam_long, az, hz_dst)
        tgt_lat = geo_obj["lat2"]
        tgt_lon = geo_obj["lon2"]
        return tgt_lat, tgt_lon
