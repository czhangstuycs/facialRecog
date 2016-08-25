import numpy as np
import cv2
import sys


eigenfaces = np.load("savedeigenfaces.npy")
avgFace = np.load("savedavgface.npy")
u = np.load("savedeigenvector.npy")
#print eigenfaces

image = cv2.imread(sys.argv[1])
faceCascade = cv2.CascadeClassifier(sys.argv[2])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


facevector = []
def addfaces(img):
    img = np.reshape(img,img.shape[0]*img.shape[1])
    facevector.append(img)
#print str(img.size
# Detect faces in the image
def detect(scale,img,origX,origY):
    imgH = img.shape[0]
    imgW = img.shape[1]
#    print str(imgW)
#    print str(imgH)

#    print img
    # Multiscale detection
    faces = faceCascade.detectMultiScale(
        img,
        scaleFactor=scale,
        minNeighbors=1,
        minSize=(20, 20),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )

    for (x,y,w,h) in faces:

        cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
        addfaces(cv2.resize(gray[y:y+h,x:x+w],(20,20)))
    
detect(1.1,gray,0,0)

#print u.shape[1]

i=0
while i < len(facevector):
#    print str(i)
 #   cv2.imshow("faces",facevector[i])
  #  cv2.waitKey(0)
    arr = np.subtract(facevector[i],avgFace)
    facevector[i] = arr
    i+=1
#    i = facevector.index(arr)
#    print i
    #print str(np.sum(np.square(temparr)))
    #cv2.imshow(str(np.sum(np.square(temparr))),np.reshape(arr,(20,20)))
    #cv2.waitKey(0)
'''
    if np.sum(np.square(arr))>1000000:
        del facevector[i]
    else:
        i+=1
'''

omega = np.dot(np.transpose(u),np.transpose(facevector))
#print eigenfaces.shape[1]
MinIndex = []

for i in range(omega.shape[1]):
    temp = []
    face = omega[:,i]
    for j in range(eigenfaces.shape[1]):
        eigenface = eigenfaces[:,j]
        temp.append(np.sum(np.square(face - eigenface)))
    MinIndex.append(np.argmin(temp))
    print temp[np.argmin(temp)]
print MinIndex
