from bokeh.io import output_file, show, curdoc
from bokeh.layouts import widgetbox,row, column
from bokeh.models.widgets import Div

from clockerV2 import countup
cc = countup()

refreshRate = 100

class clocker:
	def __init__(self):
		self.setupGui()
		self.updateClockWithCurrentTime()

	def setupGui(self):
		figHeight = 20
		figWidth = 150

		nowTitleDiv = Div(text = "Now", height = figHeight,width = figWidth)
		nowDiv = Div(text = "",height = figHeight,width = figWidth,name = "now")

		errorTitleDiv = Div(text = "Error", height = figHeight, width = figWidth)
		errorDiv = Div(text = "",height = figHeight,width = figWidth,name = "error")

		clockTitleDiv = Div(text= "Reduced time: ",height = figHeight,width = figWidth)
		clockDiv = Div(text="",width=400, height=figHeight,name = "clock")

		self.gui = column(
			row(nowTitleDiv,nowDiv),
			row(clockTitleDiv,clockDiv),
			row(errorTitleDiv,errorDiv),
			)

	def showGui(self):
		show(self.gui)
		curdoc().add_root(self.gui)
		curdoc().add_periodic_callback(self.updateClockWithCurrentTime,refreshRate)

	def updateClockWithCurrentTime(self):
		newReading,error,currentTime = cc.getModdedTime()
		self.updateClock(newReading)
		self.updateNow(str(currentTime))
		self.updateError(str(error))

	def updateDiv(self,divName,newValue):
		div = self.gui.select_one({"name":divName})
		div.text = newValue

	def updateNow(self,newTime):
		self.updateDiv("now",newTime)

	def updateError(self,newError):
		self.updateDiv("error",newError)

	def updateClock(self,newValue):
		self.updateDiv("clock",newValue)

clock = clocker()
clock.showGui()