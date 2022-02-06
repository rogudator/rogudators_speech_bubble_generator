from PyQt5.QtGui import QColor, QFontMetrics, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QCheckBox, QColorDialog, QFontComboBox, QGroupBox, QLabel, QMainWindow, QPushButton, QRadioButton, QSlider, QSpinBox, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt
from krita import *



class BubbleCoordinates():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class RSBGDocker(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rogudator's speech bubble generator")
        mainLayout = QVBoxLayout()

        self.addOnPage = QPushButton("Add on Page")
        mainLayout.addWidget(self.addOnPage)

        previewLabel = QLabel("Preview")
        mainLayout.addWidget(previewLabel)

        self.preview = QSvgWidget(self)
        self.preview.setMinimumHeight(200)
        #self.preview.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        mainLayout.addWidget(self.preview)

        bubbleTypes = QGroupBox()
        bubbleTypes.setTitle("Bubble type")
        bubbleTypesLayout = QHBoxLayout()
        self.squareBubble = QRadioButton(self)
        self.squareBubble.setText("Square")
        bubbleTypesLayout.addWidget(self.squareBubble)
        self.roundBubble = QRadioButton(self)
        self.roundBubble.setText("Round")
        self.roundBubble.setChecked(True)
        bubbleTypesLayout.addWidget(self.roundBubble)
        bubbleTypes.setLayout(bubbleTypesLayout)
        self.bubbleColorButton = QPushButton(self)
        self.bubbleColor = QColor("white")
        bubbleColorImage = QPixmap(32,32)
        bubbleColorImage.fill(self.bubbleColor)
        bubbleColorIcon = QIcon(bubbleColorImage)
        self.bubbleColorButton.setIcon(bubbleColorIcon)
        self.bubbleColorButton.setFixedWidth(self.bubbleColorButton.height())
        bubbleTypesLayout.addWidget(self.bubbleColorButton)
        mainLayout.addWidget(bubbleTypes)

        outlineSize = QGroupBox("Outline")
        outlineSliderAndSpinBox = QHBoxLayout()
        self.outlineSlider = QSlider(self)
        self.outlineSlider.setMinimum(0)
        self.outlineSlider.setMaximum(10)
        self.outlineSlider.setValue(3)
        self.outlineSlider.setOrientation(Qt.Orientation.Horizontal)
        outlineSliderAndSpinBox.addWidget(self.outlineSlider)
        self.outlineSpinBox = QSpinBox(self)
        self.outlineSpinBox.setMinimum(0)
        self.outlineSpinBox.setValue(3)
        outlineSliderAndSpinBox.addWidget(self.outlineSpinBox)
        self.outlineColorButton = QPushButton(self)
        self.outlineColor = QColor("black")
        outlineColorImage = QPixmap(32,32)
        outlineColorImage.fill(self.outlineColor)
        outlineColorIcon = QIcon(outlineColorImage)
        self.outlineColorButton.setIcon(outlineColorIcon)
        self.outlineColorButton.setFixedWidth(self.outlineColorButton.height())
        outlineSliderAndSpinBox.addWidget(self.outlineColorButton)
        outlineSize.setLayout(outlineSliderAndSpinBox)
        mainLayout.addWidget(outlineSize)

        speechGroup = QGroupBox("Speech")
        speechGroupLayout = QVBoxLayout()

        fontRow = QHBoxLayout()

        self.speechFont = QFontComboBox(self) 
        fontRow.addWidget(self.speechFont)

        self.speechFontSize = QSpinBox(self)
        self.speechFontSize.setValue(14)
        self.speechFontSize.setMinimum(1)
        fontRow.addWidget(self.speechFontSize)

        self.currentFontColorButton = QPushButton(self)
        self.speechFontColor = QColor("black")
        fontColorImage = QPixmap(32,32)
        fontColorImage.fill(self.speechFontColor)
        fontColorIcon = QIcon(fontColorImage)
        self.currentFontColorButton.setIcon(fontColorIcon)
        self.currentFontColorButton.setFixedWidth(self.currentFontColorButton.height())
        fontRow.addWidget(self.currentFontColorButton)

        speechGroupLayout.addLayout(fontRow)

        self.bubbleText = QTextEdit("Rogudator's speech bubble generator!")
        speechGroupLayout.addWidget(self.bubbleText)

        self.autocenter = QCheckBox(self)
        self.autocenter.setText("Center automatically")
        self.autocenter.setChecked(True)
        speechGroupLayout.addWidget(self.autocenter)

        self.averageLineLength = QGroupBox()
        averageLineLengthSliderAndSpinBox = QHBoxLayout()
        self.averageLineLengthSlider = QSlider(self)
        self.averageLineLengthSlider.setMinimum(0)
        self.averageLineLengthSlider.setMaximum(100)
        self.averageLineLengthSlider.setOrientation(Qt.Orientation.Horizontal)
        averageLineLengthSliderAndSpinBox.addWidget(self.averageLineLengthSlider)
        self.averageLineLengthSpinBox = QSpinBox(self)
        self.averageLineLengthSpinBox.setMinimum(0)
        averageLineLengthSliderAndSpinBox.addWidget(self.averageLineLengthSpinBox)
        self.averageLineLength.setLayout(averageLineLengthSliderAndSpinBox)
        self.averageLineLength.setDisabled(True)
        speechGroupLayout.addWidget(self.averageLineLength)

        speechGroup.setLayout(speechGroupLayout)
        mainLayout.addWidget(speechGroup)

        tailSize = QGroupBox()
        tailSize.setTitle("Tail size")
        tailSliderAndSpinBox = QHBoxLayout()
        self.tailSlider = QSlider(self)
        self.tailSlider.setMinimum(0)
        self.tailSlider.setMaximum(self.speechFontSize.value()*10)
        self.tailSlider.setOrientation(Qt.Orientation.Horizontal)
        tailSliderAndSpinBox.addWidget(self.tailSlider)
        self.tailSpinBox = QSpinBox(self)
        self.tailSpinBox.setMinimum(0)
	self.tailSpinBox.setMaximum(self.speechFontSize.value()*10)
        tailSliderAndSpinBox.addWidget(self.tailSpinBox)
        tailSize.setLayout(tailSliderAndSpinBox)
        mainLayout.addWidget(tailSize)

        self.tailPositions = QGroupBox()
        self.tailPositions.setTitle("Tail position")
        tailPositionsLayout = QHBoxLayout()
        self.tailPosition = []
        for i in range(8):
            self.tailPosition.append(QRadioButton(self))
            self.tailPosition[i].setText(str(i+1))
            self.tailPosition[i].clicked.connect(self.updatePreview)
            tailPositionsLayout.addWidget(self.tailPosition[i])

        
        self.tailPositions.setLayout(tailPositionsLayout)
        self.tailPositions.setDisabled(True)
        mainLayout.addWidget(self.tailPositions)
        
        self.updatePreview()

        self.addOnPage.clicked.connect(self.addOnPageShape)
        self.squareBubble.clicked.connect(self.updatePreview)
        self.roundBubble.clicked.connect(self.updatePreview)
        self.bubbleColorButton.clicked.connect(self.changeBubbleColor)
        self.outlineSlider.valueChanged.connect(self.outlineSpinBoxUpdate)
        self.outlineSpinBox.valueChanged.connect(self.outlineSliderUpdate)
        self.outlineSpinBox.valueChanged.connect(self.updatePreview)
        self.outlineColorButton.clicked.connect(self.changeOutlineColor)
        self.bubbleText.textChanged.connect(self.updatePreview)
        self.speechFontSize.valueChanged.connect(self.updatePreview)
        self.speechFontSize.valueChanged.connect(self.tailSliderUpdateMaximum)
        self.currentFontColorButton.clicked.connect(self.changeFontColor)
        self.speechFont.currentFontChanged.connect(self.updatePreview)
        self.autocenter.stateChanged.connect(self.enableAverageLineLength)
        self.autocenter.clicked.connect(self.updatePreview)
        self.averageLineLengthSlider.valueChanged.connect(self.averageLineLengthSpinBoxUpdate)
        self.averageLineLengthSpinBox.valueChanged.connect(self.updatePreview)
        self.averageLineLengthSpinBox.valueChanged.connect(self.averageLineLengthSliderUpdate)
        self.tailSlider.valueChanged.connect(self.tailSpinBoxUpdate)
        self.tailSpinBox.valueChanged.connect(self.tailSliderUpdate)
        self.tailSpinBox.valueChanged.connect(self.updatePreview)

        self.scrollMainLayout = QScrollArea(self)
        self.scrollMainLayout.setWidgetResizable(True)
        self.scrollMainLayout.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.scrollMainLayout.setWidget(widget)
        self.setWidget(self.scrollMainLayout)
        self.show()

    
    def tailSliderUpdateMaximum(self):
        self.tailSlider.setMaximum(self.speechFontSize.value()*10)
        self.tailSpinBox.setMaximum(self.speechFontSize.value()*10)
    
    def changeBubbleColor(self):
        self.bubbleColor = QColorDialog.getColor(self.bubbleColor)
        colorImage = QPixmap(32,32)
        colorImage.fill(self.bubbleColor)
        colorIcon = QIcon(colorImage)
        self.bubbleColorButton.setIcon(colorIcon)
        self.updatePreview()
    
    def changeFontColor(self):
        self.speechFontColor = QColorDialog.getColor(self.speechFontColor)
        colorImage = QPixmap(32,32)
        colorImage.fill(self.speechFontColor)
        colorIcon = QIcon(colorImage)
        self.currentFontColorButton.setIcon(colorIcon)
        self.updatePreview()
    
    def changeOutlineColor(self):
        self.outlineColor = QColorDialog.getColor(self.outlineColor)
        colorImage = QPixmap(32,32)
        colorImage.fill(self.outlineColor)
        colorIcon = QIcon(colorImage)
        self.outlineColorButton.setIcon(colorIcon)
        self.updatePreview()

    def outlineSpinBoxUpdate(self):
        self.outlineSpinBox.setValue(self.outlineSlider.value())
    
    def outlineSliderUpdate(self):
        if self.outlineSpinBox.value() < 51:
            self.outlineSlider.setValue(self.outlineSpinBox.value())
    
    def tailSpinBoxUpdate(self):
        self.tailSpinBox.setValue(self.tailSlider.value())
        if self.tailSlider.value() == 0:
            self.tailPositions.setDisabled(True)
        else:
            self.tailPositions.setDisabled(False)

    def tailSliderUpdate(self):
        if self.tailSpinBox.value()<101:
            self.tailSlider.setValue(self.tailSpinBox.value())

    def enableAverageLineLength(self):
        if self.autocenter.isChecked():
            self.averageLineLength.setDisabled(True)
        else:
            self.averageLineLength.setDisabled(False)
    
    def averageLineLengthSpinBoxUpdate(self):
        self.averageLineLengthSpinBox.setValue(self.averageLineLengthSlider.value())
    
    def averageLineLengthSliderUpdate(self):
        if self.averageLineLengthSpinBox.value()<101:
            self.averageLineLengthSlider.setValue(self.averageLineLengthSpinBox.value())
    
    def getSpeechLines(self, text, lineLength):
        size = 0
        speach = ""
        lines = []
        if (lineLength>0):
            words = text.split(" ")
            for word in words:
                speach += word
                size += len(word)
                if size < lineLength:
                    speach += " "
                else:
                    size = 0
                    lines.append(speach)
                    speach = ""
            if (speach != "") and (speach != " "):
                lines.append(speach.strip())
        else:
            lines = text.split("\n")
        
        return lines

    def getPreview(self):


        lineLength = int((pow((len(self.bubbleText.toPlainText())), 1/2)) * 1.8)
        if not(self.autocenter.isChecked()):
            lineLength = self.averageLineLengthSpinBox.value()
        lines = self.getSpeechLines(self.bubbleText.toPlainText(), lineLength)

        biggestLine = ""
        for line in lines:
            if (len(line) > len(biggestLine)):
                biggestLine = line

        #Calculate text box size
        font = self.speechFont.currentFont()
        font.setPixelSize(int(self.speechFontSize.value()*1.3))
        fontSize = self.speechFontSize.value()
        textHeight = int(fontSize * (len(lines)) - (fontSize - QFontMetrics(font).capHeight()))
        textWidth = QFontMetrics(font).width(biggestLine)
        tailLength = self.tailSpinBox.value()

        framePadding = fontSize
        tailPadding = tailLength
        bubblePadding = int(fontSize*1.5)

        textTag = "<text x=\"{}\" y=\"{}\" style=\"font-size:{};font-family:{};fill:{};text-anchor:middle\" >{}</text>"
        text = ""
        textStartX = framePadding+tailPadding+bubblePadding+(int(textWidth/2))
        textStartY = framePadding+tailPadding+bubblePadding+QFontMetrics(font).capHeight()
        
        for line in lines:
            text += textTag.format(textStartX, textStartY, fontSize, font.family(), self.speechFontColor.name(), line)
            textStartY += fontSize

        bubbleCoordinatesX0=framePadding+tailPadding
        bubbleCoordinatesY0=framePadding+tailPadding
        bubbleCoordinatesXHalf=framePadding+tailPadding+bubblePadding+(int(textWidth/2))
        bubbleCoordinatesYHalf=framePadding+tailPadding+bubblePadding+(int(textHeight/2))
        bubbleCoordinatesX=framePadding+tailPadding+bubblePadding+textWidth+bubblePadding
        bubbleCoordinatesY=framePadding+tailPadding+bubblePadding+textHeight+bubblePadding
        bubbleCoordinates = []
        bubbleCoordinates.append(BubbleCoordinates(bubbleCoordinatesXHalf,bubbleCoordinatesY0))
        bubbleCoordinates.append(BubbleCoordinates(bubbleCoordinatesX,bubbleCoordinatesY0))
        bubbleCoordinates.append(BubbleCoordinates(bubbleCoordinatesX,bubbleCoordinatesYHalf))
        bubbleCoordinates.append(BubbleCoordinates(bubbleCoordinatesX,bubbleCoordinatesY))
        bubbleCoordinates.append(BubbleCoordinates(bubbleCoordinatesXHalf,bubbleCoordinatesY))
        bubbleCoordinates.append(BubbleCoordinates(bubbleCoordinatesX0,bubbleCoordinatesY))
        bubbleCoordinates.append(BubbleCoordinates(bubbleCoordinatesX0,bubbleCoordinatesYHalf))
        bubbleCoordinates.append(BubbleCoordinates(bubbleCoordinatesX0,bubbleCoordinatesY0))
        
        i=0
        bubbleCoordinatesString="M"
        bubbleCoordinatesStringEnd = str(bubbleCoordinates[0].x)+","+str(bubbleCoordinates[0].y)+"Z"
        while(i<8):
            if (self.roundBubble.isChecked()):
                
                if (self.tailSpinBox.value() > 0):
                    #for coordinates in center (even)
                    textWidth01 = int(pow(textWidth,1/2.8))
                    textHeight01 = int(pow(textHeight,1/2))
                    #for coordinates in the corner (odd)
                    x04=int((bubbleCoordinates[1].x-bubbleCoordinates[0].x)*0.4)
                    x06=int((bubbleCoordinates[1].x-bubbleCoordinates[0].x)*0.6)
                    y04=int((bubbleCoordinates[2].y-bubbleCoordinates[1].y)*0.4)
                    y06=int((bubbleCoordinates[2].y-bubbleCoordinates[1].y)*0.6)
                    if i == 0 and self.tailPosition[i].isChecked():
                        bubbleCoordinatesString+= str(bubbleCoordinates[0].x-textWidth01)+","+str(bubbleCoordinates[0].y)+" L"+str(bubbleCoordinates[0].x)+","+str(bubbleCoordinates[0].y - tailLength)+" "+str(bubbleCoordinates[0].x+textWidth01)+","+str(bubbleCoordinates[0].y)+" "
                        bubbleCoordinatesStringEnd = str(bubbleCoordinates[0].x-textWidth01)+","+str(bubbleCoordinates[0].y)+"Z"
                    elif i == 2 and self.tailPosition[i].isChecked():
                        bubbleCoordinatesString+=str(bubbleCoordinates[2].x)+","+str(bubbleCoordinates[2].y-textHeight01)+" L"+str(bubbleCoordinates[2].x+tailLength)+","+str(bubbleCoordinates[2].y)+" "+str(bubbleCoordinates[2].x)+","+str(bubbleCoordinates[2].y+textHeight01)+" "
                    elif i == 4 and self.tailPosition[i].isChecked():
                        bubbleCoordinatesString+= str(bubbleCoordinates[4].x+textWidth01)+","+str(bubbleCoordinates[4].y)+" L"+str(bubbleCoordinates[4].x)+","+str(bubbleCoordinates[4].y + tailLength)+" "+str(bubbleCoordinates[4].x-textWidth01)+","+str(bubbleCoordinates[4].y)+" "
                    elif i == 6 and self.tailPosition[i].isChecked():
                        bubbleCoordinatesString+=str(bubbleCoordinates[6].x)+","+str(bubbleCoordinates[6].y+textHeight01)+" L"+str(bubbleCoordinates[6].x-tailLength)+","+str(bubbleCoordinates[6].y)+" "+str(bubbleCoordinates[6].x)+","+str(bubbleCoordinates[6].y-textHeight01)+" "
                    elif i == 1 and self.tailPosition[i].isChecked():
                        bubbleCoordinatesString+="Q"+str(bubbleCoordinates[1].x-x06)+","+str(bubbleCoordinates[1].y)+" "+str(int((bubbleCoordinates[1].x+bubbleCoordinates[1].x-x06)/2))+","+str(int((bubbleCoordinates[1].y+y04+bubbleCoordinates[1].y)/2))+" L"+str(bubbleCoordinates[1].x+tailLength)+","+str(bubbleCoordinates[1].y-tailLength)+" "+str(int((bubbleCoordinates[1].x+bubbleCoordinates[1].x-x04)/2))+","+str(int((bubbleCoordinates[1].y+y06+bubbleCoordinates[1].y)/2))+" Q" +str(bubbleCoordinates[1].x)+","+str(bubbleCoordinates[1].y+y06)+" "
                    elif i == 3 and self.tailPosition[i].isChecked():
                        bubbleCoordinatesString+="Q"+str(bubbleCoordinates[3].x)+","+str(bubbleCoordinates[3].y-y06)+" "+str(int((bubbleCoordinates[3].x+bubbleCoordinates[3].x-x04)/2))+","+str(int((bubbleCoordinates[3].y-y06+bubbleCoordinates[3].y)/2))+" L"+str(bubbleCoordinates[3].x+tailLength)+","+str(bubbleCoordinates[3].y+tailLength)+" "+str(int((bubbleCoordinates[3].x+bubbleCoordinates[3].x-x06)/2))+","+str(int((bubbleCoordinates[3].y-y04+bubbleCoordinates[3].y)/2))+" Q"+str(bubbleCoordinates[3].x-x06)+","+str(bubbleCoordinates[3].y)+" "
                    elif i == 5 and self.tailPosition[i].isChecked():
                        bubbleCoordinatesString+="Q"+str(bubbleCoordinates[5].x+x06)+","+str(bubbleCoordinates[5].y)+" "+str(int((bubbleCoordinates[5].x+bubbleCoordinates[5].x+x06)/2))+","+str(int((bubbleCoordinates[5].y-y04+bubbleCoordinates[5].y)/2))+" L"+str(bubbleCoordinates[5].x-tailLength)+","+str(bubbleCoordinates[5].y+tailLength)+" "+str(int((bubbleCoordinates[5].x+bubbleCoordinates[5].x+x04)/2))+","+str(int((bubbleCoordinates[5].y-y06+bubbleCoordinates[5].y)/2))+" Q" +str(bubbleCoordinates[5].x)+","+str(bubbleCoordinates[5].y-y06)+" "
                    elif i == 7 and self.tailPosition[i].isChecked():
                        bubbleCoordinatesString+="Q"+str(bubbleCoordinates[7].x)+","+str(bubbleCoordinates[7].y+y06)+" "+str(int((bubbleCoordinates[7].x+bubbleCoordinates[7].x+x04)/2))+","+str(int((bubbleCoordinates[7].y+y06+bubbleCoordinates[7].y)/2))+" L"+str(bubbleCoordinates[7].x-tailLength)+","+str(bubbleCoordinates[7].y-tailLength)+" "+str(int((bubbleCoordinates[7].x+bubbleCoordinates[7].x+x06)/2))+","+str(int((bubbleCoordinates[7].y+y04+bubbleCoordinates[7].y)/2))+" Q"+str(bubbleCoordinates[7].x+x06)+","+str(bubbleCoordinates[7].y)+" "
                    else:
                        if (i % 2 == 0):
                            bubbleCoordinatesString += str(bubbleCoordinates[i].x)+","+str(bubbleCoordinates[i].y)+" "
                        else:
                            bubbleCoordinatesString +="Q"+ str(bubbleCoordinates[i].x)+","+str(bubbleCoordinates[i].y)+" "
                else:
                        if (i % 2 == 0):
                            bubbleCoordinatesString += str(bubbleCoordinates[i].x)+","+str(bubbleCoordinates[i].y)+" "
                        else:
                            bubbleCoordinatesString +="Q"+ str(bubbleCoordinates[i].x)+","+str(bubbleCoordinates[i].y)+" "
            elif (self.squareBubble.isChecked()):
                bubbleCoordinatesString += str(bubbleCoordinates[i].x)+","+str(bubbleCoordinates[i].y)+" "
            i+=1
        bubbleCoordinatesString += bubbleCoordinatesStringEnd
        pathStyle = "style=\"fill:{};stroke:{};stroke-width:{};stroke-linejoin:round\"".format(self.bubbleColor.name(),self.outlineColor.name(),self.outlineSpinBox.value())
        bubble = "<path "+ pathStyle +" d=\""+ bubbleCoordinatesString +"\"/>"

        frameWidth = framePadding+tailPadding+bubblePadding+textWidth+bubblePadding+tailPadding+framePadding
        frameHeight = framePadding+tailPadding+bubblePadding+textHeight+bubblePadding+tailPadding+framePadding

        result = "<svg width=\"{}\" height=\"{}\" >{}{}</svg>".format(frameWidth, frameHeight, bubble, text)
        
        return result
    
    def updatePreview(self):
        result = self.getPreview()
        resultBytes = bytearray(result,encoding='utf-8')
        self.preview.renderer().load(resultBytes)
    
    def addOnPageShape(self):
        result = self.getPreview()
        d = Krita.instance().activeDocument()
        root = d.rootNode()
        l3 = d.createVectorLayer(self.bubbleText.toPlainText()[:16])
        root.addChildNode(l3, None)
        l3.addShapesFromSvg(result)
        pass

    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("Rogudator's Speech Bubble Generator", DockWidgetFactoryBase.DockRight, RSBGDocker))