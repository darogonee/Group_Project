age = 15
weight = 67
height = 1.75
sex = "male"
goals = []
bmi = weight/(height**2)
# inputs

if age < 18:
    if bmi < 25:
        if sex == "male":
            eer = 113.5 - 61.9*age + (26.7 * weight + 903 * height)
        elif sex == "female":
            eer = 160.3 - 30.8*age  + (10 * weight + 934 * height)
    elif bmi > 25:
        pass




# Ages 9 to 18
# Male
# EER = 113.5 - 61.9*age (years) + PAL * (26.7 * weight (kg) + 903 * height (m)), where PAL = 1 if sedentary, 1.13 if low active, 1.26 if active, and 1.42 if very active.
# Female
# EER = 160.3 - 30.8*age (years) + PAL * (10 * weight (kg) + 934 * height (m)), where PAL = 1 if sedentary, 1.16 if low active, 1.31 if active, and 1.56 if very active.
# Ages 19 or older
# Male
# EER = 661.8 - 9.53*age (years) + PAL*(15.91* weight (kg) + 539.6* height (m)), where PAL = 1 if sedentary, 1.11 if low active, 1.25 if active, and 1.48 if very active.
# Female
# EER = 354.1 - 6.91*age (years) + PAL*(9.36* weight (kg) + 726* height (m)), where PAL = 1 if sedentary, 1.12 if low active, 1.27 if active, and 1.45 if very active.
# BMI more than 25 kg/m2
# Ages 9 to 18
# Male
# EER = -114.1-50.9*age (years) + PAL * (19.5*weight (kg) + 1161.4*height (m)), where PAL = 1 if sedentary, 1.12 if low active, 1.24 if active, and 1.45 if very active.
# Female
# EER = 389.2 - 41.2*age (years) + PAL * (15 * weight (kg) + 701.6 * height (m)), where PAL = 1 if sedentary, 1.18 if low active, 1.35 if active, and 1.60 if very active.
# Ages 19 or older
# Male
# EER = 1085.6 - 10.08*age (years) + PAL*(13.7* weight (kg) + 416* height (m)), where PAL = 1 if sedentary, 1.12 if low active, 1.29 if active and 1.59 if very active.
# Female
# EER = 447.6 - 7.95*age (years) + PAL*(11.4* weight (kg) + 619* height (m)), where PAL = 1 if sedentary, 1.16 if low active, 1.27 if active and 1.44 if very active.

if 