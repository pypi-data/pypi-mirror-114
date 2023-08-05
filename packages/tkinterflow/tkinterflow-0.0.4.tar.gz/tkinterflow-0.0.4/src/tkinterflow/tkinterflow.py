from tkinter import Button, Canvas, Checkbutton, Entry, Frame, Label, Listbox, \
    Menubutton, Message, Radiobutton, Scale, Scrollbar, Text, Spinbox, \
    LabelFrame, PanedWindow


def _reorganizeWidgets(self):
    names = []
    for name in self.master.children:
        names.append(name)
    rowNumber = 0
    columnNumber = 0
    width = 0
    i = 0
    while i < len(self.master.children):
        width += self.master.children[names[i]].winfo_width()
        if i == 0:
            self.master.children[names[i]].grid(
                row=rowNumber, column=columnNumber)
        elif width > self.master.winfo_width():
            rowNumber = rowNumber+1
            columnNumber = 0
            width = self.master.children[names[i]].winfo_width()
        else:
            columnNumber = columnNumber+1
        self.master.children[names[i]].grid(row=rowNumber, column=columnNumber)
        i += 1


def _errorMessage():
    print("cannot be used at root level.  Put frame in root level and use frame")


def _flow(self, cnf={}, **kw):
    if (str(self.master) == "."):
        _errorMessage()
        return
    self.tk.call(
        ('grid', 'configure', self._w)
        + self._options(cnf, kw))
    self.master.bind("<Configure>", lambda event: _reorganizeWidgets(self))


class FlowButton(Button):
    def __init__(self, *args, **kwargs):
        super(FlowButton, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super(FlowCanvas, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowCheckbutton(Checkbutton):
    def __init__(self, *args, **kwargs):
        super(FlowCheckbutton, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowEntry(Entry):
    def __init__(self, *args, **kwargs):
        super(FlowEntry, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowFrame(Frame):
    def __init__(self, *args, **kwargs):
        super(FlowFrame, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowLabel(Label):
    def __init__(self, *args, **kwargs):
        super(FlowLabel, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowListbox(Listbox):
    def __init__(self, *args, **kwargs):
        super(FlowListbox, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowMenubutton(Menubutton):
    def __init__(self, *args, **kwargs):
        super(FlowMenubutton, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowMessage(Message):
    def __init__(self, *args, **kwargs):
        super(FlowMessage, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowRadiobutton(Radiobutton):
    def __init__(self, *args, **kwargs):
        super(FlowRadiobutton, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowScale(Scale):
    def __init__(self, *args, **kwargs):
        super(FlowScale, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowScrollbar(Scrollbar):
    def __init__(self, *args, **kwargs):
        super(FlowScrollbar, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowText(Text):
    def __init__(self, *args, **kwargs):
        super(FlowText, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowSpinbox(Spinbox):
    def __init__(self, *args, **kwargs):
        super(Spinbox, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowLabelFrame(LabelFrame):
    def __init__(self, *args, **kwargs):
        super(FlowLabelFrame, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


class FlowPanedWindow(PanedWindow):
    def __init__(self, *args, **kwargs):
        super(FlowPanedWindow, self).__init__(*args, **kwargs)

    def flow(self, cnf={}, **kw):
        _flow(self, cnf={}, **kw)


Button = FlowButton
Canvas = FlowCanvas
Checkbutton = FlowCheckbutton
Entry = FlowEntry
Frame = FlowFrame
Label = FlowLabel
Listbox = FlowListbox
Menubutton = FlowMenubutton
Message = FlowMessage
Radiobutton = FlowRadiobutton
Scale = FlowScale
Scrollbar = FlowScrollbar
Text = FlowText
Spinbox = FlowSpinbox
LabelFrame = FlowLabelFrame
PanedWindow = FlowPanedWindow
