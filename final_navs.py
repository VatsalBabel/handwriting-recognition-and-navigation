import cv2
import json
import urllib2
import numpy as np
import pytesseract
from urllib import urlencode
import urllib as urr
from PIL import Image,ImageEnhance,ImageFilter
import webbrowser

#Extracting the location related information
f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)
str_pos = str(location['latitude'])+","+str(location['longitude'])
for_route = str(location['city'])+", "+str(location['region_name'])+", "+str(location['country_code'])
city_state = "+"+for_route+"/@"
loc = []

#Capturing the image from camera
cam = cv2.VideoCapture(0)

try:
    while True:
            ret, frame = cam.read()
            #Converting image to gray
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            #Applying Threshold
            thresh = cv2.threshold(gray,70,230,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
            #Setting the kernel
            kernel = np.ones((5,5),np.uint8)
            #Dilating
            thresh_dilated = cv2.dilate(thresh, kernel, iterations=0)   
            #Displaying the window for camera
            cv2.imshow('window',thresh_dilated)
            #Saving the image
            cv2.imwrite('capture.png',thresh_dilated)
            #Reading the image
            im=Image.open('capture.png')
            #Filtering the noise and enhancing the image
            im=im.filter(ImageFilter.MedianFilter())
            enhancer=ImageEnhance.Contrast(im)
            im=enhancer.enhance(5)
            im=im.convert('1')
            #Saving the image
            im.save('final.jpg')
            #Reading the image
            toString_image = Image.open('final.jpg')
            #Getting the text from the image using pytesseract
            recogs = pytesseract.image_to_string(toString_image)
            print(recogs)
            loc.append(recogs)
            loc = list(filter(None, loc))
            if len(loc)>10:
                #Finding the route direction using the googleapis
                if((loc[0]==loc[1] and loc[1]==loc[2]) and len(loc)!=0):
                    start = loc[1]+str(for_route)
                    finish = "adhoc networks,malviya nagar,jaipur"
                    url = 'http://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((('origin', start),('destination', finish)))
                    s=urr.urlopen(url)
                    ur=s.read() 
                    result = json.loads(ur.decode('utf-8'))
                    for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
                        j = result['routes'][0]['legs'][0]['steps'][i]['html_instructions']
                        print("............................................")
                        route=j.replace('<b>',' ').replace('</b>',' ').replace('</div>',' ').replace('<div style="font-size:0.9em">',' ')
                        print(route)
                    #Opening the path navigations on google maps
                    webbrowser.open_new_tab("https://www.google.co.in/maps/dir/"+loc[1]+"/"+finish+"/@"+loc[1])
                    break
                break
            #'q' for exit
            if cv2.waitKey(1) &0xFF == ord('q'):
                break
except:
    pass
finally:
    #Exiting
    cam.release()
    cv2.destroyAllWindows()