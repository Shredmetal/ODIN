import os
os.environ["KERAS_BACKEND"] = "torch"

import keras_core
import cv2
import numpy as np
import datetime
from ultralytics import RTDETR


class Models:

    def __init__(self):

        self.clf_list = ['A10',
                         'A400M',
                         'AG600',
                         'AV8B',
                         'B1',
                         'B2',
                         'B52',
                         'Be200',
                         'C130',
                         'C17',
                         'C2',
                         'C5',
                         'E2',
                         'E7',
                         'EF2000',
                         'F117',
                         'F14',
                         'F15',
                         'F16',
                         'F18',
                         'F22',
                         'F35',
                         'F4',
                         'J20',
                         'JAS39',
                         'MQ9',
                         'Mig31',
                         'Mirage2000',
                         'P3',
                         'RQ4',
                         'Rafale',
                         'SR71',
                         'Su34',
                         'Su57',
                         'Tornado',
                         'Tu160',
                         'Tu95',
                         'U2',
                         'US2',
                         'V22',
                         'Vulcan',
                         'XB70',
                         'YF23',
                         ]
        self.clf_model = keras_core.saving.load_model("models/ac_ident_model_adadelta.keras",
                                                      custom_objects=None,
                                                      compile=True,
                                                      safe_mode=True)
        self.det_model = RTDETR(model="models/rtdetr.pt")
        self.x_ctr = None
        self.y_ctr = None
        self.x_sz = None
        self.y_sz = None
        self.box_left = None
        self.box_right = None
        self.box_bottom = None
        self.box_top = None
        self.ac_type = None
        self.crop_img = None

        self.pred_ref = None  # use this to name files related to this prediction

    def det_clf(self, img_path):

        det_pred = self.det_model(img_path)

        for r in det_pred:
            self.x_ctr = r.boxes.xywh[0][0]
            self.y_ctr = r.boxes.xywh[0][1]
            self.x_sz = r.boxes.xywh[0][2]
            self.y_sz = r.boxes.xywh[0][3]
            self.box_left = int(np.round(r.boxes.xyxy[0][0].cpu()))
            self.box_right = int(np.round(r.boxes.xyxy[0][2].cpu()))
            self.box_bottom = int(np.round(r.boxes.xyxy[0][1].cpu()))
            self.box_top = int(np.round(r.boxes.xyxy[0][3].cpu()))

        img = cv2.imread(img_path)
        self.crop_img = img[self.box_bottom:self.box_top, self.box_left:self.box_right]
        time_now = datetime.datetime.now()

        dt_str = time_now.strftime("%Y%m%d_%H%M%S")

        if not os.path.exists("preds"):
            os.makedirs("preds")

        cv2.imwrite(f"preds/{dt_str}.jpg", self.crop_img)

        crop_load = keras_core.utils.load_img(f"preds\{dt_str}.jpg",
                                              color_mode="rgb",
                                              target_size=(256, 256),
                                              interpolation="nearest",
                                              keep_aspect_ratio=False,
                                              )

        input_arr = keras_core.utils.img_to_array(crop_load)
        input_arr = np.array([input_arr])
        cls_pred = self.clf_model.predict(input_arr)
        cls_num = cls_pred.argmax()
        self.ac_type = self.clf_list[cls_num]
        self.pred_ref = dt_str
