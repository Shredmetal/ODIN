# Problem Statement

## BACKGROUND

Air warfare is the business of maintaining a higher situational awareness than the enemy. See: https://csbaonline.org/uploads/documents/Air-to-Air-Report-.pdf

This has been a fact since the earliest days of war in the air.

"The enemy must be surprised and attached at a disadvantage, if possible with superior numbers so the initiative was with the patrol... the combat must continue until the enemy has admitted his inferiority, by being shot down or running away."

Oswald Boelcke in the "Dicta Boelcke", a World War 1 era flight combat manual.

German aces of World War 2, such as Erich Hartmann (352 kills) and Gerd Barkhorn (302 kills) stressed what they referred to as "ambush tactics" in Europe. In the Pacific, American aces such as Richard Bong (40 kills) and Tommy McGuire (38 kills) developed virtually identical tactics.

A detailed analysis of 112 air combat engagements during the Vietnam War conducted by the US Air Force concluded that 80% of aircrew shot down were unaware of the impending attack. 

"Despite vast changes in aircraft, sensor, communication, and weapon capabilities over the past century, the fundamental goal of air combat has remained constant: leverage superior [Situational Awareness] SA, to sneak into firing position, destroy the opposing aircraft, and depart before other enemy aircraft can react."

Trends in Air-to-air combat - Implications for Future Air Superiority, John Stillon, CSBA report.

Modern sensors primarily focus on radar detection of hostile aircraft, with a dearth of ground-based optical sensors.

## PROBLEM:

There are several problems intended to be solved by this project:

1. In order to avoid being surprised by radar guided munitions, modern military aircraft usually come equipped with a radar warning receiver. This set of antennae and processing equipment passively "listen" for radio waves used by radar and provide the pilot with warnings on (i) the presence of a radar, (ii) when the radar is tracking the aircraft, and (iii) when the radar is guiding a missile onto aircraft. 

Radars cannot be kept on indefinitely. Imagine a dark room. Turning the radar on is the equivalent of turning on a torch in the said dark room. Anti radiation missiles can home in on the radar emissions. Certain aircraft are also specially equipped to triangulate the position of an emitting radar to provide coordinates to other precision guided munitions (see: AN/ASQ-213 HARM targeting system)

Combining radar detection with other, passive sensors, permit greater SA than radar systems alone.

2. Missiles rockets do not burn the entire time of flight. They usually only have a few seconds of fuel before the missile relies on momentum to coast to the target (exceptions such as the MBDA Meteor exist, but that is an exception). This means that missiles can be kinematically defeated by simply turning in the other direction. The further away the target is when launch occurs, the more reaction time the pilot has.

A passive sensor would permit the radars to remain off until the target enters the no escape zone (where the missile will still catch the target if it turns and runs and there is accordingly a high Pk (kill probability)).

3. No sensor net is perfect, additional passive sensors that can be acquired cheaply (cameras and consumer GPUs) offers a capability boost with a small expenditure of resources. 

## OBJECTIVES:

1. Build a model which detects military aircraft from an image.

2. Build a second model to identify the type of aircraft detected by the first model.

3. Integrate both models into a program which take in (i) coordinates of camera, (ii) elevation of camera, (iii) altitude of camera, and (iv) information from the models, and return (i) type of aircraft, (ii) estimated coordinates of aircraft, and (iii) estimated altitude of aircraft.

## SCOPE:

1. Use the data to feed various machine learning models to achieve the objectives.

2. Select the best detection model based on precision/recall, and the best classification model based on accuracy. 

3. Develop program to satisfy the requirements of objective 3.

## DATA:

1. Military aircraft detection dataset. https://www.kaggle.com/datasets/a2015003713/militaryaircraftdetectiondataset

## METHODS AND TOOLS:

1. Neural networks including (i) ConvNext, (ii) EfficientNet, (iii) YOLOv8, (iv) RT-DETR.

## SUCCESS METRICS:

1. Accuracy.

2. Precision/Recall.

# Hardware and related requirements

CUDA compatible GPU: https://developer.nvidia.com/cuda-gpus

CUDA >= 11.8

# Detector Notebook Requirements

cv2                 4.8.1
matplotlib          3.7.2
numpy               1.25.2
pandas              2.1.0
sklearn             1.3.0
tqdm                4.66.1
ultralytics         8.0.207
yaml                6.0.1

# Classifier Notebook Requirements:

keras               2.14.0
keras-core           0.1.7
#matplotlib          3.7.2
numpy               1.25.2

# Function testing and development Notebook Requirements:

cv2                 4.8.1
geographiclib       2.0
keras_core          0.1.7
matplotlib          3.7.2
numpy               1.25.2
pandas              2.1.0
ultralytics         8.0.207

# Model Performance

## Detector

| Model        | Epochs | Precision | Recall    | mAP50      | Remarks                                    |
|--------------|--------|-----------|-----------|------------|--------------------------------------------|
|Yolov8        |300     |0.229      |0.171      |0.122       |Wholly unacceptable                         |
|RT-DETR       |100     |0.762      |0.756      |0.753       |Optimiser - SGD                             |  
|RT-DETR       |200     |0.751      |0.742      |0.708       |Optimiser - SGD                             |
|RT-DETR       |300     |0.754      |0.727      |0.745       |Optimiser - SGD                             |
|RT-DETR       |100     |0.767      |0.7        |0.728       |Cos LR Scheduler                            |
|RT-DETR       |200     |0.754      |0.692      |0.719       |Cos LR Scheduler                            |
|RT-DETR       |100     |0.468      |0.401      |0.363       |Cos LR Scheduler + extra mixup augmentation |
|RT-DETR       |200     |0.649      |0.614      |0.517       |Cos LR Scheduler + extra mixup augmentation |
|RT-DETR       |300     |0.712      |0.652      |0.662       |Cos LR Scheduler + extra mixup augmentation |
|RT-DETR       |400     |0.713      |0.683      |0.687       |Cos LR Scheduler + extra mixup augmentation |
|RT-DETR       |100     |0          |0          |0           |Optimiser - Adamax                          |
|RT-DETR       |100     |nan        |nan        |nan         |Optimiser - AdamW                           |
|RT-DETR       |200     |0.758      |0.759      |0.759       |Optimiser - SGD + extra augmentation        |
|RT-DETR       |300     |0.751      |0.737      |0.715       |Optimiser - SGD + extra augmentation        |

## Classifier

| Model        | Optimiser | Train Acc | Train Loss | Val Acc | Val Loss |Fit time     |
|--------------|-----------|-----------|------------|---------|----------|-------------|
|ConvNext Base |AdamW      |0.9811     |0.0647      |0.7831   |1.1933    |58m 29s      |
|ConvNext Base |RMSProp    |0.9760     |0.0702      |0.7766   |1.3348    |51m 11s      |
|ConvNext Base |Adam       |0.9761     |0.0743      |0.7724   |1.1510    |50m 41s      |
|ConvNext Base |Adamax     |0.9981     |0.0330      |0.8031   |0.8546    |1hr 12m 39s  |
|ConvNext Base |SGD        |0.9620     |0.2507      |0.7802   |0.8217    |12hr 17m 2s  |
|ConvNext Base |Adadelta   |0.9978     |0.0091      |0.9100   |0.5438    |76m 13s      |
|ConvNext Base |Adagrad    |0.0362     |15.5349     |0.0384   |15.5020   |52m 52s      |
|ConvNext Base |Nadam      |0.5144     |1.6397      |0.1886   |4.7987    |1hr 59m 7s   |
|ConvNext Base |Ftrl       |0.0619     |3.6134      |0.0553   |3.6123    |2hr 47m 16s  | 

# Program

The above has been consolidated into a single program with a GUI > run from interface.py.

Test images can be found in Assets.

A video of the program working can be found here: 
https://www.youtube.com/watch?v=MkIymKNswYQ

# Conclusions and recommendations

1. The optical distributed IADs Network component system is theoretically feasible and successfully detected and located target aircraft.
2. It can be used to supplement traditional detection mechanisms to provide greater air defence coverage.

