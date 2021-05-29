import os
import numpy as np
import cv2
import pymysql as mdb
import time
import sys
import os
import cv2
import numpy as np
import time
import pickle
import skimage
import numpy as np
from skimage.morphology import watershed
from skimage.feature import peak_local_max
from scipy import ndimage 
import scipy
res=['Not detect','Detected']
filename = 'finalized_model.sav'
clf=pickle.load(open(filename, 'rb'))
def update(disease, ids):
    mydb = mdb.connect(
      host="127.0.0.1",
      user="root",
      passwd="",
      database="370project"
    )
    mycursor = mydb.cursor()
    sql = "UPDATE disease SET disease = %s WHERE id = %s"
    val = (disease, ids)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
while True:
    mydb = mdb.connect(
          host="127.0.0.1",
          user="root",
          passwd="",
          database="370project"
        )
    mycursor = mydb.cursor()
    sql = "SELECT id,pic,disease FROM disease"
    mycursor.execute(sql)
    fine=0
    myresult = mycursor.fetchall()
    mydb.close()
    for x in myresult:
      ids= str(x[0])
      pic=str(x[1])
      fl=str(x[2])
      if fl=='1':
        x_dataset=[]
        time.sleep(2)
        pic1=pic
        pic='imgsent/process/images/'+pic
        pic2='imgsent/process/images/A'+pic1
        print(pic2)
        
        image=cv2.imread(pic,0)
        image=cv2.GaussianBlur(image,(5,5),0)
        
        r, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
      
        distance = ndimage.distance_transform_edt(image)
        local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)), labels=image)
        markers = skimage.morphology.label(local_maxi)
        x = skimage.morphology.watershed(-distance, markers, mask=image)
        cv2.imwrite(pic2, x)  
        x=np.array(x,dtype='float32')
        
        x=x/255.0
        x=cv2.resize(x,(224,224))
        x_dataset.append(x)
        X_dataset=np.array(x_dataset)
        nsamples, nx, ny = X_dataset.shape
        X_dataset = X_dataset.reshape((nsamples,nx*ny))
        y_pred=(clf.predict(X_dataset))
        Y_predict=int(y_pred)
        result=(res[Y_predict]) 
        print(result)
        update(result, ids)    
        

          
