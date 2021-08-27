# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 20:09:42 2021

@author: MK857
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 15:56:45 2021

@author: MK857
"""
# import required libraries and modules 
from tkinter import *
from tkinter import ttk
import warnings # to avoid warning 
from tkinter import filedialog
from tkinter.filedialog import askopenfilename,asksaveasfilename
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import os
root= Tk()
myStack = [] # stack variables created for undo and reset operations
root.geometry("800x800") # dimensions of gui  working window
#            GUI TITLE
root.title("IMAGE PROCESSING GUI")  # GUI title


#canvas is created for display of Image and placement 
canvas2 = Canvas(root, width="600", height="420", relief=RIDGE, bd=2)
canvas2.place(x=15, y=150)
             
       # DEFINING FUNCTION FOR LOADING IMAGE           
def selected():
    global img_path, img,imgr  #variables to store image path and images
    
    #opening local directory
    
    img_path = filedialog.askopenfilename(title="select a file",filetypes=(("png files", "*.jpg"),("all file", "*.*")))
    img = Image.open(img_path)#assign Img variable to loaded image  
   
    img1 = ImageTk.PhotoImage(img)#using pillow library 
    myStack.append('v') # add variable v onto stack upon running this command
    #using the created canvas for display purpose
    canvas2.create_image(300, 210, image=img1)
    canvas2.image=img1    
def undo():
    """# After every operation the output is 
    stored in the local directory stack variables are
    assigned in every function based on below conditions 
     the Images will be displayed"""
    
    
    global img_path, img,imgr
    myStack.pop()
    """# pop out top element to undo previous operation"""
    if(myStack[len(myStack)-1]=="a"):
        img = Image.open("hist.jpg")
    elif  myStack[len(myStack)-1]=="b":
        img = Image.open("log.jpg")
                
    elif myStack[len(myStack)-1]=="c":
        img = Image.open("gamma.jpg")
               
    elif myStack[len(myStack)-1]=="d":
        img = Image.open("blur.jpg")
                 
    elif myStack[len(myStack)-1]=="e":
        img = Image.open("sharp.jpg")
    elif myStack[len(myStack)-1]=="f":
        img = Image.open("sobel.jpg")
    elif myStack[len(myStack)-1]=="v":
        """To display the image on canvas same for all the functions """
        img = Image.open(img_path)
    img1 = ImageTk.PhotoImage(img)
    canvas2.create_image(300, 210, image=img1)
    canvas2.image=img1            
def reset():
    global img_path, img,imgr
    myStack.pop()
    """"Earlier assigned v variable for loading image we are using 
    it here"""
    if(myStack[0]=="v"):
        img = Image.open(img_path)   
    img1 = ImageTk.PhotoImage(img)
    canvas2.create_image(300, 210, image=img1)
    canvas2.image=img1 



       # histogram equilization of image 
 

def histogram_equilization():
    
    
    
    from IPython.display import display, Math, Latex
    import numpy as np
    import cv2
    import matplotlib.pyplot as plt
    from PIL import Image
    global img_path, img1, imgg,imgr
    #load the image 
    img = Image.open(img_path)
    # convert image to array
    img= np.asarray(img)
    def get_histogram(image, bins):
    # Take an array of size bins and take it with zeros 
     histogram = np.zeros(bins)
    
  # loop through pixels and sum up counts of pixels
     for pixel in image:
         histogram[pixel] += 1
    
    #  final histogram result
     return histogram
 #function for cumm sum or CDF
    def cumsum(a):
     a = iter(a)#recursive a 
     b = [next(a)]
     for i in a:
         b.append(b[-1] + i)
     return np.array(b)
    
    if(len(img.shape)<3):# check for grayscale
         
        flat = img.flatten()
     #Get the flatten histogram
  
        hist = get_histogram(flat, 256)
 
# calculate  the CDF OF HISTOGRAM  obtained
        cs = cumsum(hist)
 
# Normalize the cdf for Equilization
        nj = (cs - cs.min()) * 255
        N = cs.max() - cs.min()
        cs = nj / N
      
      #convert NORMALIZED CDF datatype to uint8
    
        cs = cs.astype('uint8')
        img_new = cs[flat] #flat the cdf and give to image_new variable
        img_new = np.reshape(img_new, img.shape)# reshape to original size
        img_new=Image.fromarray(img_new)#get image from array
        imgg=img_new #use imgg to display on canvas 
        img1 = ImageTk.PhotoImage(imgg)
        myStack.append('a')  # add variable a onto stack upon running this command
        imgr = imgg.save("hist.jpg")# saving in local directory for undo
        canvas2.create_image(300, 210, image=img1)
        canvas2.image=img1
    else:#same as above works for colour image
        #covert rgb image to HSV IMAGE and take v_channel
        HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        v_channel = HSV_img[:,:,2]
        img = np.asarray(v_channel)
        flat = img.flatten()
        hist = get_histogram(flat, 256)
        cs = cumsum(hist) 
        #normalize the cdf
        nj = (cs - cs.min()) * 255
        N = cs.max() - cs.min()
        cs = nj / N
        # cast it back to uint8 since we can't use floating point values in images
        cs = cs.astype('uint8')
        img_new = cs[flat]
        img_new = np.reshape(img_new, img.shape)
         
        #GETTING HSV IMAGE FROM V_CHANNEL
        v_channel=img_new
        HSV_img[:,:,2]=v_channel
        #GETTING RGB IMAGE FROM HSV
        rgbimg = cv2.cvtColor(HSV_img, cv2.COLOR_HSV2BGR)
        rgbimg=Image.fromarray(rgbimg)
        imgg=rgbimg #Give  rgbimg to imgg for display on canvas
        myStack.append('a') 
        imgr = imgg.save("hist.jpg")
        print(myStack)
        img1 = ImageTk.PhotoImage(imgg) 
        canvas2.create_image(300, 210, image=img1)
        canvas2.image=img1
        
        
        
        
        
def  logtransform():
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    global img_path, img1, imgg,imgr
    
    warnings.filterwarnings("ignore")
    # Load  the image and convert it to arrays for operations.
    img = Image.open(img_path)
    img= np.asarray(img)
    if(len(img.shape)<3):#check grayscale
    #Apply log transform formula
      c = 255/(np.log(1 + np.max(img)))  
      log_transformed = c * np.log(1 + img1)
        
      # Specify the data type.
      log_transformed = np.array(log_transformed, dtype = np.uint8) 
      #Get the image from array
      log_transformed=Image.fromarray(log_transformed)
      imgg=log_transformed #assign log transform image to imgg variable for display
      myStack.append('b') 
      imgr = imgg.save("log.jpg")
      #print(myStack)
      img1 = ImageTk.PhotoImage(imgg)
      canvas2.create_image(300, 210, image=img1)
      canvas2.image=img1
    else:# works for colour image
        #convert rgb image to HSV image  
        # take v_channel for manipulation
      HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
      v_channel = HSV_img[:,:,2]
      img1=v_channel# assign v_channel to img1 variable
  
   # Apply log transform.
      c = 255/(np.log(1 + np.max(img1)))
      log_transformed = c * np.log(1 + img1)
  
# Specify the data type.
      log_transformed = np.array(log_transformed, dtype = np.uint8)
      #GETTING HSV IMAGE FROM V_CHANNEL
      v_channel=log_transformed
      HSV_img[:,:,2]=v_channel 
      #GETTING RGB IMAGE FROM HSV
      rgbimg = cv2.cvtColor(HSV_img, cv2.COLOR_HSV2BGR)
      rgbimg=Image.fromarray(rgbimg)
      imgg=rgbimg#assign the output rgb image to imgg variable for display
      myStack.append('b') 
      imgr = imgg.save("log.jpg")
      #print(myStack)
      img1 = ImageTk.PhotoImage(imgg) 
      canvas2.create_image(300, 210, image=img1)
      canvas2.image=img1
 
    
 
    
def click():
    """Created this  function for taking
          gamma value"""

    # Creating entry widget and getting the input from user
    val = myentry.get()

    try:
        # converting string to float
        val = float(val)
        
        return val
    except ValueError:
        
        return val
    # Clearing  the entry widget if it is wrong 
    myentry.delete(0, END)

 

   
def gammacorrection():
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    global img_path, img1, imgg,imgr
    # Loading the image  and convert to array for operations .
    img = Image.open(img_path)
    img= np.asarray(img)
    if(len(img.shape)<3):# checking for  grayscale
        
        
           
         #placement of entry widget  created earlier
        mylabel.place(x=370, y=8)
        myentry.place(x=460, y=15)
        gamma=click()# taking user gamma value
         
	# Apply gamma correction formula  to the Image.
        gamma_corrected = np.array(255*(img / 255) ** gamma, dtype = 'uint8')
        gamma_corrected=Image.fromarray(gamma_corrected)
        imgg= gamma_corrected
        """#add variable c to stack upon executing this command """
        myStack.append('c') 
       
        imgr = imgg.save("gamma.jpg")
        """display the result on canvas"""
        img1 = ImageTk.PhotoImage(imgg)
        canvas2.create_image(300, 210, image=img1)
        canvas2.image=img1 
        print("GAMMA CORRECTION DONE")
    else:      # works for  colour image
        
          
         #placement of entry widget  created earlier
         mylabel.place(x=370, y=8)
         myentry.place(x=460, y=35)
          
         gamma=click()# taking user gamma value
          
   
	# Apply gamma correction formula to the Image .
         gamma_corrected = np.array(255*(img / 255) ** gamma, dtype = 'uint8')
         """convert RGB TO HSV and take v_channel for manipulation"""
         HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
         v_channel = HSV_img[:,:,2]
         """do the manipulations to v_channel  """
         gamma_corrected = np.array(255*(v_channel / 255) ** gamma, dtype = 'uint8')
         v_channel= gamma_corrected
         HSV_img[:,:,2]=v_channel   
         """get the RGB IMAGE FROM HSV"""
         rgbimg = cv2.cvtColor(HSV_img, cv2.COLOR_HSV2BGR)
         rgbimg=Image.fromarray(rgbimg)
         imgg=rgbimg #assigning rgbimg variable to imgg for display
         myStack.append('c') 
         imgr = imgg.save("gamma.jpg")
         img1 = ImageTk.PhotoImage(imgg) 
         canvas2.create_image(300, 210, image=img1)
         canvas2.image=img1
         #print("GAMMA CORRECTION DONE")
        # print(myStack)






def blurring(event):
     
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    from skimage.io import imshow, imread
    from skimage.color import rgb2yuv, rgb2hsv, rgb2gray, yuv2rgb, hsv2rgb
    from scipy.signal import convolve2d # using convolve function for convolution
    """# this function does the convolution 
    of filter and image with no of iterations as input"""
    def multi_convolver(image, kernel, iterations):
        for i in range(iterations):
            image = convolve2d(image, kernel, 'same', boundary = 'fill',
                           fillvalue = 0)
        return image
    """Gaussian blur using low pass filtering """
    # Gaussian Blur Matrix
    gaussian = (1 / 16.0) * np.array([[1., 2., 1.],
                                  [2., 4., 2.],
                                  [1., 2., 1.]])
    global img_path, img1, imgg,imgr
    #  Load the image and convert to array for operations
    img = Image.open(img_path)
    img= np.asarray(img)
    if(len(img.shape)==3):#checking for colour image
        for k in range(0, v1.get()+1):
            """k is the no of iterations into 
            conolve functions taken from control scale 
            with variable v1"""
            """convert rgb to hsv and take v channel """
            HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            v_channel = HSV_img[:,:,2]
            output=multi_convolver(v_channel, gaussian, k)
            v_channel=  output# give the output to v_channel
            HSV_img[:,:,2]=v_channel
            #GETTING RGB IMAGE FROM HSV
            rgbimg = cv2.cvtColor(HSV_img, cv2.COLOR_HSV2BGR)
            rgbimg=Image.fromarray(rgbimg)
            imgg=rgbimg# assigning rgb image to imgg for display 
            myStack.append('d') # add variable d to stack upon executing the code
            imgr = imgg.save("blur.jpg")
            img1 = ImageTk.PhotoImage(imgg) 
            canvas2.create_image(300, 210, image=img1)
            canvas2.image=img1   
    else:
        
        for k in range(0, v1.get()+1):
            
            """k is the no of iterations into conolve 
            functions taken from control scale 
            with variable v1"""
            output=multi_convolver(img, gaussian,k)
            output=Image.fromarray(output)#getting the image from array
            imgg=output
            myStack.append('d') 
            imgr = imgg.save("blur.jpg")
            img1 = ImageTk.PhotoImage(imgg) 
            canvas2.create_image(300, 210, image=img1)
            canvas2.image=img1  
    




def sharpening(event):
     
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    from skimage.io import imshow, imread
    from skimage.color import rgb2yuv, rgb2hsv, rgb2gray, yuv2rgb, hsv2rgb
    from scipy.signal import convolve2d # using convolve function for convolution
    """# this function does the convolution 
    of filter and image with no of iterations as input"""
    def multi_convolver(image, kernel, iterations):
        for i in range(iterations):
            image = convolve2d(image, kernel, 'same', boundary = 'fill',
                           fillvalue = 0)
        return image
    """Sharpening  using Laplacian filtering """
    
    # Laplacian Matrix
    sharpen = np.array([[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]])
    global img_path, img1, imgg,imgr
    # Load the image and convert it to array .
    img = Image.open(img_path)
    img= np.asarray(img)
    if(len(img.shape)==3):# checking for rgb images
        """k is the no of iterations into conolve 
            functions taken from control scale 
            with variable v2"""
        for k in range(0, v2.get()+1):
             #convert rgb image to HSV and take v_channel for operations
            HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            v_channel = HSV_img[:,:,2]
            output=multi_convolver(v_channel, sharpen, k)
            v_channel=  output
            HSV_img[:,:,2]=v_channel
            #GETTING RGB IMAGE FROM HSV
            rgbimg = cv2.cvtColor(HSV_img, cv2.COLOR_HSV2BGR)
            rgbimg=Image.fromarray(rgbimg) #get the image back from array
            imgg=rgbimg# give  the rgbimg to imgg for displaying
            myStack.append('e') # add variable e to stack upon executing the code
            imgr = imgg.save("sharp.jpg")
            img1 = ImageTk.PhotoImage(imgg) 
            canvas2.create_image(300, 210, image=img1)
            canvas2.image=img1   
    else: #works for grayscale image 
        for k in range(0, v2.get()+1):
            #k=int(input("Enter your blur  value : "))
            output=multi_convolver(img, sharpen,k)
            output=Image.fromarray(output)
            imgg=output
            myStack.append('e') 
            imgr = imgg.save("sharp.jpg")
            img1 = ImageTk.PhotoImage(imgg) 
            canvas2.create_image(300, 210, image=img1)
            canvas2.image=img1  
def save():
    global img_path, imgg, img1
     #opening local directory for image storage
    ext = img_path.split(".")[-1]
    file=asksaveasfilename(defaultextension =f".{ext}",filetypes=[("All Files","*.*"),("PNG file","*.png"),("jpg file","*.jpg")])
    if file: 
            if canvas2.image==img1:
                imgg.save(file)    
       
def sobel(event):
     
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    from skimage.io import imshow, imread
    from skimage.color import rgb2yuv, rgb2hsv, rgb2gray, yuv2rgb, hsv2rgb
    from scipy.signal import convolve2d # using convolve function for convolution
    """# this function does the convolution 
    of filter and image with no of iterations as input"""
    def multi_convolver(image, kernel, iterations):
        for i in range(iterations):
            image = convolve2d(image, kernel, 'same', boundary = 'fill',
                           fillvalue = 0)
        return image
 
    # sobel matrix 
    sobel=np.array([[-1, -2, -1],
                    [0, 0, -0],
                    [1, 2, 1]])
    global img_path, img1, imgg,imgr
  # Load the image and convert it to array .
    img = Image.open(img_path)
    img= np.asarray(img)
    if(len(img.shape)==3):#checking for colour image
        for k in range(0, v3.get()+1):
            """k is the no of iterations into conolve 
            functions taken from control scale 
            with variable v3"""
          #convert rgb image to HSV and take v_channel for operations
            HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            v_channel = HSV_img[:,:,2]
            output=multi_convolver(v_channel, sobel, k)
            v_channel=  output
            HSV_img[:,:,2]=v_channel
            #GETTING RGB IMAGE FROM HSV
            rgbimg = cv2.cvtColor(HSV_img, cv2.COLOR_HSV2BGR)
            rgbimg=Image.fromarray(rgbimg) #get the image from array
            imgg=rgbimg# give  the rgbimg to imgg for displaying
            myStack.append('f')  # add variable f to stack upon executing the code
            imgr = imgg.save("sobel.jpg")
            img1 = ImageTk.PhotoImage(imgg) 
            canvas2.create_image(300, 210, image=img1)
            canvas2.image=img1   
    else:# works for grayscale image 
        """k is the no of iterations into conolve 
            functions taken from control scale 
            with variable v3"""
        for k in range(0, v2.get()+1):
            
            output=multi_convolver(img, sobel,k)
            output=Image.fromarray(output)
            imgg=output
            myStack.append('f') 
            imgr = imgg.save("sobel.jpg")
            img1 = ImageTk.PhotoImage(imgg) 
            canvas2.create_image(300, 210, image=img1)
            canvas2.image=img1  
 
#for CREATING   buttons and placing in  GUI SCREEN  
                
#Image loading button creation  and  placement
btn1 = Button(root, text="Select Image", bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=selected)
btn1.place(x=20, y=595)



#Histogram Equilization button creation  and  placement
btn2 = Button(root, text="Histogram Equilize", bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=histogram_equilization)
btn2.place(x=160, y=595)



##Log Transform button creation  and  placement
btn3=Button(root, text="Logtransform", bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=logtransform)
btn3.place(x=355, y=595)






#Entry widget creation for taking gamma value from user
myentry = Entry(bg='black', fg='gold')
mylabel=Label(root,text="ENTER GAMMA VALUE AND CLICK GAMMA CORRECTION",bg='black', fg='gold')



#Gamma correct  button creation  and  placement
btn4=Button(root, text="Gamma_correct", bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=gammacorrection)
btn4.place(x=505, y=595)



#save button creation  and  placement
btn5= Button(root, text="Save", width=12, bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=save)
btn5.place(x=675, y=595)




#undo button creation  and  placement
btn6= Button(root, text="Undo", width=12, bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=undo)
btn6.place(x=675, y=200)




#reset button creation  and  placement
btn7= Button(root, text="Reset", width=12, bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=reset)
btn7.place(x=675, y=300)





# blurring layout scale creation  and  placement
v1 = IntVar()
scale1 = ttk.Scale(root, from_=0, to=10, variable=v1, orient=HORIZONTAL, command=blurring) 
scale1.place(x=150, y=10)
blurr = Label(root, text="Blur:", font=("ariel 17 bold"), width=9, anchor='e')

blurr.place(x=15, y=8)






### sharpening layout scale creation  and  placement
v2 = IntVar() 
scale2 = ttk.Scale(root, from_=0, to=10, variable=v2, orient=HORIZONTAL, command=sharpening) 
scale2.place(x=150, y=55)
sharp = Label(root, text="Sharpness:", font=("ariel 17 bold"))
sharp.place(x=8, y=50)






#sobel operation scale creation  and  placement
v3 = IntVar() 
scale3 = ttk.Scale(root, from_=0, to=10, variable=v3, orient=HORIZONTAL, command=sobel) 
scale3.place(x=150, y=100)
sobel = Label(root, text="Sobel:", font=("ariel 17 bold"))
sobel.place(x=35, y=92)



# creation of exit button and placement of exit button
btn8 = Button(root, text="Exit", width=12, bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=root.destroy)# creation of exit button
btn8.place(x=675, y=450)


root.mainloop()