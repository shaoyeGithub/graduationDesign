from graduation.diagnosis import testclassify
from graduation.page.client import preprocess
from  PIL import Image
import numpy as np
import  cv2
import matplotlib.pyplot as plt
from skimage import measure,draw
import  dicom
import  datetime
getpt = dicom.read_file("D:/FILE/python_code/graduation/page/client/data1/bojingyi/src/PT/PT_006")
print(getpt.PatientBirthDate)
age = int(datetime.datetime.now().year) - int(getpt.PatientBirthDate[:4])

print(age)
