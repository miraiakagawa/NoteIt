### 15-112 Fundamentals of Programming
### F11 Term Project
### Name: MIRAI AKAGAWA
### andrewid: makagawa
### Section: D
### Mentor: Xiao Bo Zhao


### main program
### multiTouch is a imported module that is originally taken from the internet,
### but edited by me.
### original by Ludvig Ericson
### reference: http://blog.sendapatch.se/2009/november/macbook-multitouch-in-
### python.html

try:
    import time
    from multiTouch import * # modified module from internet
    from Tkinter import * 
    import Image as PIL, ImageDraw
    import ImageTk
    import shutil
except:
    print "one or more modules are missing. please install or relocate"

###############################################################################
### INIT ###
###############################################################################

def init():
    # initialise multiTouch - configure device, etc.
    canvas.data.device = initMT()
    initColors() # initialize colors for PIL
    canvas.data.writeMode = canvas.data.drawMode = False # used for write/draw
    canvas.data.start = False # used to know whether to start multitouch
    canvas.data.wordImage = None
    canvas.data.drawingImage = None
    canvas.data.docImage = None
    canvas.data.penSize = 4 # pen size for Tkinter
    canvas.data.scaleFactor = 4 # PIL size
    canvas.data.delay = 1 # timerFired refresh
    canvas.data.topHalf = True # initially writing on top half
    canvas.data.margin = canvas.data.width/10 # margin on the doc
    canvas.data.skipWord = False
    tk_rgb = "#%02x%02x%02x" % (0, 0, 0)
    canvas.data.color = tk_rgb
    initCanvas() # start screen for canvas
    initToolbar() # start screen for toolbar
    initDoc() # start screen for document

### initialize some color names for PIL to use
def initColors():
    canvas.data.white = (255, 255, 255)
    canvas.data.black = (0, 0, 0)

### start screen for doc
def initDoc():
    width, height = canvas.data.width, canvas.data.height # save canvas dimens
    canvas.data.initScreen = PIL.open('notebook.png') # start screen
    canvas.data.initScreen = ImageTk.PhotoImage(canvas.data.initScreen)
    doc.create_image(width/2, height/2+150, image=canvas.data.initScreen)

### start screen for the canvas, pehaps make it more entertaining...?
def initCanvas():
    width, height = canvas.data.width, canvas.data.height
    # for startup, want to display the instructions on the canvas.
    canvas.delete(ALL)
    canvas.data.canvasInit = PIL.open('instructions.png') # start screen
    canvas.data.canvasInit = ImageTk.PhotoImage(canvas.data.canvasInit)
    # display the image on the canvas
    canvas.create_image(width/2, height/2, image=canvas.data.canvasInit)
    # during the program, when the user wants to display the instructions,
    # it will go in a new window

### starts the toolbar!
### create various buttons for the user to use. display the shortcut key
### in the button
### using gridding to adjust the positions of the buttons
def initToolbar():
    width = canvas.data.width
    # buttom for quitting program
    b = Button(toolbar, text="Quit (q)", width=10, command=quitProgram)
    b.grid(row=1, column=0, columnspan= 2, padx=2, pady=2)
    # buttom for reset
    b = Button(toolbar, text="Reset (r)", width=10, command=clearAll)
    b.grid(row=1, column=6, columnspan= 2, padx=2, pady=2)
    # button for New File
    b = Button(toolbar, text="New File (n)", width=10, command=newFile)
    b.grid(row=2, column=0, padx=2, pady=2, columnspan=2)
    # button for Save File
    b = Button(toolbar, text="Save File (s)", width=10, command=saveFile)
    b.grid(row=2, column=2, padx=2, pady=2, columnspan =2)
    # button for Instructions 
    b = Button(toolbar, text="Instructions (i)", 
                                            width=10, command=drawInstructions)
    b.grid(row=2, column=6, padx=2, pady=2, columnspan =2)
    # button for Clear Screen
    b = Button(toolbar, text="Paste (p)", width=10, command=pasteDrawing)
    b.grid(row=2, column=4, padx=2, pady=2, columnspan=2)
    # button for Write Mode
    b = Button(toolbar,text="Write Mode (w)", width=24, command=writeMode)
    b.grid(row=3, column=0, padx=2, pady=2,columnspan=4)
    # button for Draw Mode
    b = Button(toolbar, text="Draw Mode (d)", width=24,command=drawMode)
    b.grid(row=3, column=4, padx=2, pady=2, columnspan=4)
    drawCurrent() # gets updated as colors or pensize change
    drawColorPick() # asks user input for colors
    drawPenSizePick() # asks user input for pensize

### shows the current color and pensize
### updated whenever set is pressed
def drawCurrent():
    label = Label(toolbar, text="Current Color:")
    label.grid(row=4, column=0, columnspan=2, sticky=E)
    # fills in the background with the current color.
    label = Label(toolbar, width=5, height=2, bg=canvas.data.color)
    label.grid(row=4, column=2, columnspan=2)
    label = Label(toolbar, text="Current Pen Size:")
    label.grid(row=4, column=4, columnspan=2, sticky=E)
    # pensize is actually drawn onto the toolbar canvas, using redrawAll

### buttons and entries for the colors
def drawColorPick():
    label = Label(toolbar, width=5, text="Color:")
    label.grid(row=5, column=0, sticky=E)
    # ask for RGB values from 0~255
    label = Label(toolbar, width=5, text="R:")
    label.grid(row=5, column=1, sticky=E)
    # need to store data to retrieve the entry later
    canvas.data.colorR = Entry(toolbar, width=5)
    canvas.data.colorR.grid(row=5, column=2, sticky=W)
    label = Label(toolbar, width=5, text="G:")
    label.grid(row=5, column=3, sticky=E)
    canvas.data.colorG = Entry(toolbar, width=5)
    canvas.data.colorG.grid(row=5, column=4, sticky=W)
    label = Label(toolbar, width=5, text="B:")
    label.grid(row=5, column=5, sticky=E)
    canvas.data.colorB = Entry(toolbar, width=5)
    canvas.data.colorB.grid(row=5, column=6, sticky=W)
    # buttom for setting color
    # data in the entries at the time of button press will be stored
    b = Button(toolbar, text="Set",command=readColor)
    b.grid(row=5, column=7, padx=2, pady=2)

### same, but for pen size
def drawPenSizePick():
    label = Label(toolbar, text="Pen Size:")
    label.grid(row=6, column=0, sticky=E)
    canvas.data.penSizeEntry = Entry(toolbar, width=5)
    canvas.data.penSizeEntry.grid(row=6, column=2, sticky=W)
    b = Button(toolbar, text="Set",command=readPenSize)
    b.grid(row=6, column=3, padx=2, pady=2)

### reads the color values of the entires
def readColor():
    # .get() converts the information in the entries to a string
    strR = canvas.data.colorR.get()
    strG = canvas.data.colorG.get()
    strB = canvas.data.colorB.get()
    # if the string is not a number, it will crash when converting to int.
    # if the entry is left open, make it mean 0
    try: 
        colorR = 0 if strR == "" else int(strR)
        colorG = 0 if strG == "" else int(strG)
        colorB = 0 if strB == "" else int(strB)
        # it is an integer, but out of rance
        if (colorR < 0 or colorG < 0 or colorB < 0 or 
            colorR > 255 or colorG > 255 or colorB > 255):
            text = "Please enter integer values between 0 and 255"
            error(text)
        else:
            # conversion to hexadecimal string
            tk_rgb = "#%02x%02x%02x" % (colorR, colorG, colorB)
            canvas.data.color = tk_rgb
            drawCurrent()
    # in which case show an error message
    except: 
        text = "Please enter integer values between 0 and 255"
        error(text)

### same for pen size.
def readPenSize():
    strPenSize = canvas.data.penSizeEntry.get()
    try: 
        # default pen size is 4.
        penSize = 4 if strPenSize == "" else int(strPenSize)
        if 0 < penSize < 51:
            canvas.data.penSize = penSize
            drawCurrent()
        else: # too big is a burden for the program -__-
            text = "Please enter an integer value between 1 and 50"
            error(text)
    except: 
        text = "Please enter an integer value between 1 and 50"
        error(text)

##############################################################################
## USING MULTITOUCH DEVICE ###:
##############################################################################

### starts the multitouch device and draws the points on canvas
### simultaneously, it will save the points on PIL, which will be saved as .png
def writeInput():
    width, height = canvas.data.width, canvas.data.height 
    device = canvas.data.device # refers to the multiTouch device on hardware
    MTDeviceStart(device) # device starts taking data
    time.sleep(1.0/1000) # stopping after 1ms
    points = returnMTPos() # points will be returned in a set
    for point in points: # iterate through points:
        # floating point value is adjusted to fit Tkinter canvas
        x, y = int(round(point[0] * width)),int(round(point[1] * height))
        # want to keep track of right most and left most pixel to crop the
        # word at the end
        # nasty bug! when there is just one point on the multitouch,
        # e.g. for indent, leftbound = rightbound, and the cropped image
        # actually becomes a line. to prevent that, add 1 to x
        # when creating right bound
        leftBound, rightBound = canvas.data.boundaries
        if x < leftBound: leftBound = x # narrowing down bounds!
        if x > rightBound: rightBound = x
        canvas.data.boundaries = leftBound, rightBound # store!
        topHalf = canvas.data.topHalf # which half of the trackpad are we on?
        # checks if you started writing on the other half of the trackpad 
        if ((topHalf == True and y > height/2) or 
            (topHalf == False and y < height/2)):
            # if so, want to go to new word
            newWord(x,y)
        # displays the points on the Tkinter canvas
        drawTkinter(x, y)
        # draws the points on PIL (invisible to user)
        drawPIL(x, y, "write")

### once you start writing on other half of the trackpad, it means a new word
### is started. hence the following procedures are taken:
def newWord(x,y, options=None):
    width, height = canvas.data.width, canvas.data.height
    canvas.data.topHalf = not canvas.data.topHalf # writing on other half
    # delete function
    if x < 5: # want to ignore the current word
        canvas.data.skipWord = True
    if canvas.data.skipWord == False:
        cropImage() # crops the image into just its word
        drawDocPIL() # converts to the master file by pasting into file
    if options == None:
        initPIL("write") # need to start new image for new word
    # if the user touches the top edge or the bottom edge of the trackpad, 
    # depending on whether writing on the top half or the bottom half, it 
    # means new line.
    canvas.delete(ALL) # clear the screen
    # cropping is done by narrowing down boundaries - 
    # initially, width and 0
    canvas.data.boundaries = width, 0
    doc.delete(ALL)
    drawDoc()
    # if the user touches the top or bottom edges of the trackpad,
    # it means new line
    if y < 5 or y > height-5:
        newLine()
    # if the user touches the right edge of the trackpad it means indent
    elif x > width-5:
        indent()
    elif 5 < y < height-5 and 5 < x < width -5:
        # now we don't want to skip this word! so untrigger skip word.
        canvas.data.skipWord = False

### adds and indentation to whichever line you are on
def indent():
    width = canvas.data.width
    clearMTPos() # clear the data on the multitouch device for next use
    # add half a magin size to the x position of the next word
    canvas.data.dx += canvas.data.margin
    # because we don't want to save this "image" - just a dot, trigger skip 
    # word and next time around we won't save the image on the document
    canvas.data.skipWord = True

### adds a new line from whichever line you are on
def newLine():
    clearMTPos()
    # add the amount of spacing to the next line to the y value of the next
    # word
    spacing = canvas.data.height/(2*canvas.data.scaleFactor)
    canvas.data.dy += spacing + canvas.data.spacing
    # reset the x value to just the margin
    canvas.data.dx = canvas.data.margin
    canvas.data.skipWord = True

# starts the multitouch device and draws the points on canvas
# simultaneously, it will save the points on PIL, which will be saved as .png
def drawInput():
    width, height = canvas.data.width, canvas.data.height 
    device = canvas.data.device # refers to the multiTouch device on hardware
    MTDeviceStart(device)
    time.sleep(1.0/1000)
    points = returnMTPos()
    for point in points:
        # adjusted to the Tkinter canvas
        x, y = int(round(point[0] * width)),int(round(point[1] * height))
        # displays points on Tkinter canvas
        drawTkinter(x, y)
        # on PIL
        drawPIL(x, y, "draw")

###############################################################################
### DRAWING on TKINTER CANVAS / PIL ###
###############################################################################

### given the center of the trackpad position, draws a point on the canvas
def drawTkinter(x,y):
    # r for radius
    r = canvas.data.penSize
    canvas.create_oval(x-r, y-r, x+r, y+r, fill=canvas.data.color,
                                           outline=canvas.data.color)

### draws the given pixel at x,y on PIL (invisible)
def drawPIL(x,y, mode):
    r = canvas.data.penSize
    width, height = canvas.data.width, canvas.data.height
    if mode == "write": # depending on mode, different image
        image = canvas.data.wordImage
        draw = canvas.data.drawWord
    if mode == "draw":
        image = canvas.data.drawingImage
        draw = canvas.data.drawDrawing
    # height divided by 2 because there are two halves of the screen for 
    # writingand we want to put every word in the same location.
    height = height/2 if mode == "write" else height
    coords = [x-r, y%(height)-r, x+r, y%(height)+r]
    draw.ellipse(coords, canvas.data.color)
    # PIL drawing function 

### master document keeps all the words that have been written, and compiles
### them into a sentence.
def drawDocPIL():
    # takes the image drawn on the canvas
    image = canvas.data.wordImage
    # the image for the actual document
    doc = canvas.data.docImage
    # want to resize it
    scaleFactor = canvas.data.scaleFactor
    # returns the size of the image
    imageWidth, imageHeight = image.size
    resize = imageWidth/scaleFactor, imageHeight/scaleFactor
    # resized image: antialias preserves quality
    image = image.resize(resize, PIL.ANTIALIAS)
    # want to fit it on to the doc, so if the word exceeds the margin size,
    # go to new line
    if (canvas.data.dx+resize[0]+canvas.data.margin > canvas.data.docWidth):
        canvas.data.dx = canvas.data.margin
        canvas.data.dy += resize[1] + canvas.data.spacing
    # location of the image to be posted on doc
    dx, dy = canvas.data.dx, canvas.data.dy
    box = (dx, dy)
    # pastes image on to the doc
    doc.paste(image, box)
    # save the doc back to the variable
    canvas.data.docImage = doc
    # add a space before the next word
    canvas.data.dx += resize[0] + canvas.data.spacing

### paste existing drawing into the document
def pasteDrawing():
    width = canvas.data.width
    if canvas.data.docImage != None:
        # retrieve the document
        doc = canvas.data.docImage
    else:
        text = "Haven't created document yet!"
        error(text)
        return
    if canvas.data.drawingImage != None:
        # retrieve the drawing
        drawing = canvas.data.drawingImage
    else:
        text = "Haven't created drawing yet!"
        error(text)
        return
    # put the image on a new line...
    newLine()
    # need to resize it so that it fits in the margins, and give it some space
    # on the sides.
    resizeWidth = width-(3*canvas.data.margin)
    # need to adjust the height proportionally
    scale = resizeWidth/float(width)
    # here is the height, used float because interger division = lame here.
    resizeHeight = int(canvas.data.height * scale)
    resize = (resizeWidth, resizeHeight)
    # resized image: antialias preserves quality
    drawing = drawing.resize(resize, PIL.ANTIALIAS)
    # location of the image to be posted on doc
    dx, dy = canvas.data.dx, canvas.data.dy
    box = (dx, dy)
    # pastes image on to the doc
    doc.paste(drawing, box)
    # save the doc back to the variable
    canvas.data.docImage = doc
    # want to move the cursor location to the bottom of the image
    while (canvas.data.dy < dy + resizeHeight):
        newLine()
    # as cursor is top left corner, we need one more!
    #newLine()
    drawDoc()

### draws the document on Tkinter so user can see
def drawDoc():
    width, height = canvas.data.width, canvas.data.height
    # ImageTk module converts image to photoimage
    canvas.data.photo = ImageTk.PhotoImage(canvas.data.docImage)
    # put it on the canvas
    doc.create_image(0,0, image=canvas.data.photo, anchor=NW)
    
### the appearance of the Tkinter canvas when write mode is on
def drawWritingCanvas():
    width, height = canvas.data.width, canvas.data.height
    # add center line to know where the middle is
    canvas.create_line(0,height/2, width, height/2)
    # add guidance lines
    lines = 8
    lineSpacing = height/lines
    for i in xrange(lines):
        y = lineSpacing * i
        if i != lines/2:
            canvas.create_line(0,y,width,y, fill="grey")

### the appearaoce of the Tkinter canvas when draw mode is on
def drawDrawingCanvas():
    width, height = canvas.data.width, canvas.data.height
    # let the user know of the extent of the canvas
    canvas.create_rectangle(3,3,width,height, width=2)

### want some lines on the document so it looks nicer
def drawDocLines(options=None):
    # left, right bound of line are the margins
    left = canvas.data.margin
    right = canvas.data.docWidth - canvas.data.margin
    # lines is drawn on 3/4 of the image, so that letters like g go under the 
    # line. need to scale it so it fits the particular size though, so:
    scaleFactor = canvas.data.scaleFactor
    spacing = canvas.data.height/(2*scaleFactor)
    y = canvas.data.margin + spacing*3/4
    # until we hit the end of the page
    while y < canvas.data.docHeight-canvas.data.margin:
        if options == None: doc.create_line(left,y,right,y, fill="grey")
        elif options == "PIL":
            canvas.data.drawDocument.line([left,y,right,y], (102,102,102))
        y += spacing + canvas.data.spacing

# during the program, when the user wants to display the instructions,
# it will go in a new window
def drawInstructions():     
        # stop the multiTouch device so that there is no malinput
        canvas.data.start = False
        # new popup window
        instructionsWindow = Toplevel()
        instructionsWindow.title("Instructions")
        canvas.data.instructionsWindow = instructionsWindow
        # label is used to put images
        label = Label(instructionsWindow, image=canvas.data.canvasInit)
        label.pack()
        # button to confirm done
        button = Button(instructionsWindow, 
                     text="DONE", width=10, command=quitInstructions)
        button.pack()

### restarts the device as soon as its done.
def quitInstructions():
    clearMTPos()
    canvas.data.instructionsWindow.destroy() # get rid of window
    if canvas.data.writeMode == True or canvas.data.drawMode == True:
        canvas.data.start = True # only restart if in certain mode

### error message, takes a text and displays an error message with it
def error(text):
    canvas.data.start = False # pause device
    errorWindow = Toplevel() # create new window
    errorWindow.title("Error!")
    canvas.data.errorWindow = errorWindow # store it so that it can be closed
    label = Label(errorWindow, text=text) # display the text
    label.grid(row=0, column=0) # not necessary, but good organisation
    button = Button(errorWindow,text="OK", width=10, command=quitWindow)
    button.grid(row=1, column= 0) # button to confirm OK

### destroys the window, and restarts the device
def quitWindow():
    clearMTPos()
    # only if we were in a certain mode though
    if canvas.data.writeMode == True or canvas.data.drawMode == True:
        canvas.data.start = True
    errorWindow = canvas.data.errorWindow
    errorWindow.destroy()

### redraws all Tkinter canvases
def redrawAll():
    width, height = canvas.data.width, canvas.data.height
    # refresh toolbar
    toolbar.delete(ALL)
    # display the current size of the pen on the toolbar
    r = canvas.data.penSize
    x, y = canvas.data.width/4*3 ,115 # physical location
    # create one oval with radius pensize
    toolbar.create_oval(x-r, y-r, x+r, y+r, fill=canvas.data.color,
                                                outline=canvas.data.color)
    # because when write mode is turned on, it asks the user to create a new
    # file, this takes much longer than timerFired refresh rate. so, added
    # a data.start which is triggered only when user finishes entering the 
    # file name
    if canvas.data.writeMode == True and canvas.data.start == True:
        drawWritingCanvas() # displays the writing canvas
        drawDocLines() # want lines on the doc
        writeInput() # STARTS DEVICE configured for writing
        toolbar.create_text(width/2-20,16, text="Current Mode: WRITE MODE", 
        font="system 16", fill= "red") # notify the user of mode
    # same deal for draw...
    elif canvas.data.drawMode == True and canvas.data.start == True:
        drawDrawingCanvas()
        drawInput() # STARTS DEVICE configured for drawing
        toolbar.create_text(width/2-20,16, text="Current Mode: DRAW MODE", 
                                                font= "system 16",fill= "red") 
    # nothing happening here...
    else: 
        toolbar.create_text(width/2-20,16, text="Current Mode: Not Selected!", 
                                                font= "system 16",fill= "red") 

##############################################################################
### EVENTS ###
##############################################################################

### whenever these keys are pressed, its like a shortcut
def keyPressed(event):
    if (event.char == "w"): # enter writing mode, start recording device.
        writeMode()
    elif (event.char == "d"): # enter drawing mode, start recording device
        drawMode()
    elif (event.char == "q"): # quit the program and save the master file
        quitProgram()
    elif (event.char == "s"): # its not that hard to figure out is it.
        saveFile()
    elif (event.char == "n"):
        newFile()
    elif (event.char == "r"):
        clearAll()
    elif (event.char == "p"):
        pasteDrawing()
    elif (event.char == "i"):
        drawInstructions()

def clearAll():
    stopDevice() # stops recording data from device
    canvas.delete(ALL) # clears all 3 canvases
    doc.delete(ALL)
    toolbar.delete(ALL)
    init()

### trigger the write mode to start
def writeMode():
    clearMTPos() # clear the contents of the multitouch device just in case
    # draw mode is on, so we don't want to start write mode
    if canvas.data.drawMode == True:
        text = "Draw Mode is on. Please exit Draw Mode before using Write Mode"
        error(text)
    # change the status of the mode, from on to off or off to on
    else: canvas.data.writeMode = not canvas.data.writeMode
    # if there is no docImage present, it means we need to create a new one
    if canvas.data.writeMode == True and canvas.data.docImage == None:
        newFile()
    # a doc file already exists, so just keep editing that one.
    elif canvas.data.writeMode == True: 
        canvas.data.start = True
        initPIL("write") # still need a PIL image to edit though.
    # stopping writing...
    else:
        # last word, so don't need to create a new image, hence the option
        newWord(canvas.data.width/2, canvas.data.height/2, "end")
        canvas.data.start = False # not in on mode
        stopDevice() # stop recording the device
    canvas.delete(ALL) # clear the canvas

### trigger the draw mode to start
def drawMode():
    clearMTPos()
    # same as write mode, when other mode is on, display error message
    if canvas.data.writeMode == True:
        text ="Write Mode is on. Please exit Write Mode before using Draw Mode"
        error(text)
    # change the status of the mode
    else: canvas.data.drawMode = not canvas.data.drawMode
    # if no image exists, need to create a new one.
    if canvas.data.drawMode == True and canvas.data.drawingImage == None:
        canvas.delete(ALL)
        newFile()
    # a file already exists, so just keep drawing on that one
    elif canvas.data.drawMode == True:
        canvas.data.start = True
    else: # stopping draw mode
        canvas.data.start = False
        stopDevice()

### exits the program
def quitProgram():
    # want to save the file differently depending on mode
    if canvas.data.writeMode == True: # in case of write mode
        cropImage()
        drawDocPIL() # save the remaining contents onto the doc before save
        saveFile()
    if canvas.data.drawMode == True: # in case of draw mode
        saveFile()
    # quit program
    root = Tk()
    root.quit()
    
### stops the device from recording data. prevents taking data while in off
### modes.
def stopDevice():
    MTDeviceStop(canvas.data.device)

###############################################################################
### EDITING IMAGES ON PIL ###
###############################################################################

### create an image to draw on for PIL - not visible from Tkinter
def initPIL(mode):
    width, height = canvas.data.width, canvas.data.height
    # create a new PIL image file to draw on
    if mode == "write": # for write, we want half the canvas size for PIL 
        canvas.data.wordImage = PIL.new("RGB", 
                                       (width, height/2), canvas.data.white)
        canvas.data.drawWord = ImageDraw.Draw(canvas.data.wordImage)
        # used to crop images to just their width!
        canvas.data.boundaries = width, 0
    elif mode == "draw": # for drawing, want to use the full canvas
        canvas.data.drawingImage = PIL.new("RGB", 
                                         (width, height), canvas.data.white)
        canvas.data.drawDrawing = ImageDraw.Draw(canvas.data.drawingImage)

### master PIL file, which acts as a document which holds all the words
### constructed into sentences
def initDocPIL():
    width, height = canvas.data.width, canvas.data.height
    # separate changable document width and height
    docWidth = width # widht is the same as canvas
    docHeight = int(1.6* docWidth) # golden ratio
    canvas.data.docWidth, canvas.data.docHeight = docWidth, docHeight
    canvas.data.docImage = PIL.new("RGB", (docWidth, docHeight), 
                                                     canvas.data.white)
    canvas.data.drawDocument = ImageDraw.Draw(canvas.data.docImage)
    # keeps track of the number of words written so that it can be incremented
    # and put in the right position on the master file
    canvas.data.wordCount = 0
    # displacement of the word from the top left of the document
    canvas.data.dx = canvas.data.margin
    canvas.data.dy = canvas.data.margin
    # adds spaces automatically
    canvas.data.spacing = docWidth/(canvas.data.scaleFactor*10)
    #drawDocLines("PIL")

### crops the image into the desired size
def cropImage():
    width, height = canvas.data.width, canvas.data.height
    image = canvas.data.wordImage # image on the canvas
    # boundaries are the left and right most pixels of the word
    left, right = canvas.data.boundaries
    # PIL crops are kinda harsh, so lets give it a little space
    leeway = canvas.data.penSize+1
    # cropping dimensions
    # because left bound and right bound give the center of the point that we
    # want to draw, in order to accomodate the whole point we need to add the
    # pensize. However, if adjusting the bounds by adding or subtracting the 
    # leeway exceeds the image width, it will just draw a straight line
    # which we don't want. in this case, just use the dimensions of the image
    # as the boundaries.
    left = 0 if left - leeway < 0 else left-leeway
    right = width if right + leeway > width else right+leeway
    box = (left, 0, right, height/2)
    # crop the image!
    image = image.crop(box)
    # save it back to the variable
    canvas.data.wordImage = image

###############################################################################
### CREATING/SAVING FILES
###############################################################################

### creates a new file to work on
def newFile():
    window = Toplevel() # new window
    window.title("New File")
    message = Message(window, text="New File", width=40)
    canvas.data.window = window
    label = Label(message, text="Enter File Name:")
    label.grid(row=1, column=0, sticky=E)
    fileName = Entry(message) # actual entry
    fileName.grid(row=1, column=1)
    canvas.data.fileName = fileName # save it so we can retrieve data
    # once button is pressed, the text inside the entries get saved
    button = Button(message, text="Create",command=create)
    button.grid(row=2, columnspan=2)
    message.pack()

### after user finishes putting the data, need to save it and start working!
def create():
    window = canvas.data.window
    # gets whats inside the entries
    canvas.data.fileName = canvas.data.fileName.get()
    # this means the user pressed "New File" and not a select mode. thats ok.
    # just need to ask which mode the user wants.
    if canvas.data.writeMode == False and canvas.data.drawMode == False:
        canvas.delete(ALL)
        choiceWindow = Toplevel() # haha 3rd screen omg
        choiceWindow.title("Choose Mode")
        canvas.data.choiceWindow = choiceWindow
        label = Label(choiceWindow, text="Please Choose Mode")
        label.grid(row=0, column=0, columnspan = 2)
        # argh, should use functional programming here... but this still works
        button = Button(choiceWindow,text="WRITE", width=10, command=callWrite)
        button.grid(row=1, column= 0)
        button = Button(choiceWindow, text="DRAW", width=10, command=callDraw)
        button.grid(row=1, column= 1)
    startWorking()
    window.destroy()

def startWorking():
    # initialise an image to draw one
    if canvas.data.drawMode == True:
        initPIL("draw")
    # only want doc if we are in write mode
    elif canvas.data.writeMode == True:
        initPIL("write")
        initDocPIL()
        doc.delete(ALL)
        drawDocLines()
    # now we can start the device
    canvas.data.start = True

### just turns on the mode, and calls create again.
def callWrite():
    canvas.data.choiceWindow.destroy()
    canvas.data.writeMode = True
    startWorking()

### same deal
def callDraw():
    canvas.data.choiceWindow.destroy()
    canvas.data.drawMode = True
    startWorking()

### saves the file!
def saveFile():
    try:
        # this means we are working on a document
        if canvas.data.wordImage != None:
            image = canvas.data.docImage
            drawDocLines("PIL")
        # this means we are working on a drawing
        elif canvas.data.drawingImage != None:
            image = canvas.data.drawingImage
        # either way, save it to the given name
        # if no name was entered, its file.png
        if canvas.data.fileName == "": filename = "file.png"
        else: filename = str(canvas.data.fileName) + ".png"
        image.save(filename)
    except: # even if we can't save, don't crash. just means no file!
        text = "There is no file to save!"
        error(text)

###############################################################################
### TIMER FIRED ###
###############################################################################

### does what it says.
def timerFired():
    redrawAll()
    delay = canvas.data.delay
    canvas.after(delay, timerFired)

###############################################################################
### RUN PROGRAM ###
###############################################################################

def run():
    global canvas # using global variable to store data
    global toolbar # canvas for the toolbar at the top
    global doc # to show document window
    root = Tk() # Tkinter root window
    root.resizable(width=FALSE, height=FALSE) 
    root.title("NoteIt - v3.1")
    width = 540
    height = int(7.8*width/10.6) # dimensions of trackpad
    frame = Frame(root, bg= "grey")
    # create the three canvases
    toolbar = createToolbar(frame, width, height)
    canvas = createCanvas(frame, width, height)
    doc = createDocument(frame, width, height)
    #set outside frame
    frame.pack()
    # store data in a class
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width, canvas.data.height = width, height
    init() 
    root.bind("<Key>", keyPressed) # used for keyboard shortcuts
    timerFired()
    root.mainloop()

# main canvas for showing trackpad positions and draws points
def createCanvas(frame, w, h):
    # create a frame which contains the canvas
    canvasFrame = Frame(frame, bd=2, relief=RAISED)
    canvasFrame.grid(pady=10, padx=10, row=1, column=0, sticky=N)
    # create the canvas
    canvas = Canvas(canvasFrame, width=w, height=h)
    Label(canvasFrame, text="TRACKPAD DISPLAY").pack()
    canvas.pack()
    return canvas

# creates the toolbar at the top
def createToolbar(frame, w, h):
    toolbarFrame = Frame(frame, bd=2, relief=RAISED)
    toolbarFrame.grid(pady=10, padx=10, row=0, column=0,sticky=W+E+N+S)
    toolbar = Canvas(toolbarFrame, width=w, height=100, bg="white")
    Label(toolbarFrame, text="TOOLBAR").pack()
    toolbar.pack()
    return toolbar

# document at the side of the screen
def createDocument(frame, width, height):
    docFrame = Frame(frame, bd=2, relief=RAISED)
    docFrame.grid(pady=10, padx=10, row=0, column=1, rowspan=3, sticky=W+E+N+S)
    doc = Canvas(docFrame, width=width, height=int(width*1.3))
    Label(docFrame, text="DOCUMENT").pack()
    doc.pack()
    return doc

run()
