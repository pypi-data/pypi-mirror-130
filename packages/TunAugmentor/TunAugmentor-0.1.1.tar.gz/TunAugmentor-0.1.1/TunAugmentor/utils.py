import cv2
import glob


def read_images(path):
    images=[]
    files = glob.glob (path+"/*.jpg")
    for myFile in files:
        image = cv2.imread(myFile)
        images.append(image)
    return images

def read_image(path):
    image=[cv2.imread(path)]
    return image
def export(images,path):
    i=0
    res=True
    for im in images:
        i+=1
        img_name='/img'+str(i)+'.jpg'
        res=cv2.imwrite(path+img_name,im) and res
    return res