# tkinterflow

This is a project to add the functionality of a 'flow' layout to Python Tkinter graphical user interface module.

tkinter has the Pack, Grid, and Place geometry managers.

This module adds a Flow option to the geometry managers.

To implement the module, install it first with:
```
pip install tkinterflow
```
then use the following import statements IN THIS ORDER (Very important!)
```
from tkinter import *
from tkinterflow import *
```
Now additional methods can be used.  If you are used to using statements like:
```
button1.pack()
```
#### you can use
```
button1.flow()
```
to add the widgets to a frame.
#### you can use
```
button1.destroy()
```
to remove the button from the frame.

The widgets should flow inside the parent frame like typical flow geometry, like in typical html or just regular text flow like word-wrapping.

You cannot use the flow geometry manager in the root widget, but can use it in any frame below root.

#### So if you only have one root window, pack a frame into the root window, then use flow to add widgets to that frame.  You'll want to make that frame stick to the parent root window so it expands with the root window.

The flow behavior is a subset of the grid geometry manager.

#### Like pack, grid, and place, you should not mix geometry managers.  Likewise with the flow geometry manager.

-If you are flowing into a frame, only use flow, don't try to mix and match geometry managers.

### Here are a few examples:

##### Example 1:
```
from tkinter import *
from tkinterflow import *       # ! Very important, put this right after import of tkinter functions

root = Tk()              
myFrame = Frame(root)                 # Very Important!, you cannot use .flow() methods in root
myFrame.pack(fill=BOTH, expand=True)  # Very Important!, frame must stick to parent container walls

button1 = Button(myFrame, text="----Button1---")
button1.flow(sticky="")

button2 = Button(myFrame, text="Button2")
button2.flow(sticky="")

button3 = Button(myFrame, text="----Button3---")
button3.flow(sticky="")

button4 = Button(myFrame, text="Button4")
button4.flow(sticky="")

root.mainloop()
```

##### Example 2:
```
from tkinter import *
from tkinterflow import *       # ! Very important, put this right after import of tkinter functions

root = Tk()              
myFrame = Frame(root)                 # Very Important!, you cannot use .flow() methods in root
myFrame.pack(fill=BOTH, expand=True)  # Very Important!, frame must stick to parent container walls

button1 = Button(myFrame, text="--Button1--")
button1.flow(sticky=NSEW)

button2 = Button(myFrame, text="Button2")
button2.flow(sticky=NSEW)

button3 = Button(myFrame, text="--Button3--")
button3.flow(sticky=NSEW)

button4 = Button(myFrame, text="Button4")
button4.flow(sticky=NSEW)

button5 = Button(myFrame, text="--Button5--")
button5.flow(sticky=NSEW)

button6 = Button(myFrame, text="Button6")
button6.flow(sticky=NSEW)

button7 = Button(myFrame, text="--Button7--")
button7.flow(sticky=NSEW)

root.mainloop()
```

##### Example 3:
```
from tkinter import *
from tkinterflow import *       # ! Very important, put this right after import of tkinter functions

def unstickyWidgets():
    button1.grid_configure(sticky="")
    label.grid_configure(sticky="")
    entry.grid_configure(sticky="")
    radioButton.grid_configure(sticky="")
    checkButton.grid_configure(sticky="")
    scale_widget.grid_configure(sticky="")
    button2.grid_configure(sticky="")
    button3.grid_configure(sticky="")
    root.update()

def stickyWidgets():
    button1.grid_configure(sticky="NSEW")
    label.grid_configure(sticky="NSEW")
    entry.grid_configure(sticky="NSEW")
    radioButton.grid_configure(sticky="NSEW")
    checkButton.grid_configure(sticky="NSEW")
    scale_widget.grid_configure(sticky="NSEW")
    button2.grid_configure(sticky="NSEW")
    button3.grid_configure(sticky="NSEW")
    root.update()

root = Tk()              
myFrame = Frame(root)                 # Very Important!, you cannot use .flow() methods in root
myFrame.pack(fill=BOTH, expand=True)  # Very Important!, frame must stick to parent container walls

button1 = Button(myFrame, text="---Button1---")
button1.flow(sticky=NSEW)

label = Label(myFrame, text="Label")
label.flow(sticky=NSEW)

entry = Entry(myFrame)
entry.flow(sticky=NSEW)

radioButton = Radiobutton(myFrame, text="radio button")
radioButton.flow(sticky=NSEW)

checkButton = Checkbutton(myFrame, text="CheckButton")
checkButton.flow(sticky=NSEW)

scale_widget = Scale(myFrame, from_=0, to=100, orient=HORIZONTAL)
scale_widget.flow(sticky=NSEW)

button2 = Button(myFrame, text="---sticky Widgets/see effect--", command=stickyWidgets)
button2.flow(sticky=NSEW)

button3 = Button(myFrame, text="---unsticky Widgets---", command=unstickyWidgets)
button3.flow(sticky=NSEW)

root.mainloop()
```

##### Update Notes:
The tkinterflow module 0.0.4 has been changed significantly in the way it works.  Instead of modifying tkinters `__init__.py` file to achieve adding the .flow method to widgets, I use inheritence to make a child from each widget (except the Menu widget).  Then I add the flow method to the child.  Then I reassign the name of the parent to the child.  This relies on you first importing tkinter, then importing tkinterflow as noted this order is important.  I did this because I did not want to edit my package everytime someone makes a change to tkinters initialization file.
