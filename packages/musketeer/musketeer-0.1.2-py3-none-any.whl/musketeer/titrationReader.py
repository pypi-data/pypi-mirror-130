import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd

import csv
import numpy as np
import os
import re
from pkg_resources import packaging

from .titration import Titration

# need to tell matplotlib to use the tkinter backend, otherwise the scale
# of figures can get messed up if it would default to a different backend
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt   # noqa
from matplotlib.backends.backend_tkagg import (  # noqa
    NavigationToolbar2Tk, FigureCanvasTkAgg
)
from matplotlib.backend_bases import key_press_handler  # noqa

universalCsvVersion = packaging.version.parse("1.0.0")
padding = 10


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def getFileReader():
    fileType = askFileType()
    if fileType == "":
        return None
    return fileReaders[fileType]


def askFileType():
    fileType = tk.StringVar()
    askFileTypeDialog(fileType)
    return fileType.get()


def askFileTypeDialog(stringVar):
    popup = tk.Toplevel()
    popup.title("Select input file type")
    popup.grab_set()

    frame = ttk.Frame(popup, padding=padding)
    frame.pack(expand=True, fill="both")

    label = ttk.Label(frame, text="Select input file type:")
    label.pack()

    fileTypes = fileReaders.keys()
    optionMenu = ttk.OptionMenu(
        frame, stringVar, None, *fileTypes, style="Outline.TMenubutton"
    )
    optionMenu.pack(fill="x", pady=padding)

    button = ttk.Button(frame, text="Select", command=popup.destroy)
    button.pack()
    popup.wait_window(popup)


def getFilePath():
    # On Windows, askopenfilename can hang for a while after the file is
    # selected. This seems to only happen if the script has been run before,
    # and disabling all internet connections seems to fix it. ???
    filePath = fd.askopenfilename(
        title="Select input file",
        filetypes=[("csv files", "*.csv"), ("all files", "*.*")]
    )
    return filePath


# gets the volume in litres from string
def getVolumeFromString(string):
    searchResult = re.search(r"([0-9.]+) ?([nuμm]?)[lL]", string)
    if not searchResult:
        return None
    volume, prefix = searchResult.group(1, 2)
    volume = float(volume)
    if not prefix:
        return volume
    elif prefix == "m":
        return volume / 1e3
    elif prefix == "u" or prefix == "μ":
        return volume / 1e6
    elif prefix == "n":
        return volume / 1e9
    else:
        return None


def readUV(filePath):
    titration = Titration()
    titration.title = os.path.basename(filePath)
    # set default parameters for UV-Vis titrations
    titration.continuous = True
    titration.yQuantity = "Abs"
    titration.yUnit = "AU"
    titration.xQuantity = "λ"
    titration.xUnit = "nm"
    titration.contributorQuantity = "ε"
    titration.contributorUnit = "$M^{-1} cm^{-1}$"

    with open(filePath, "r", newline='') as inFile:

        reader = csv.reader(inFile)

        titleRow = next(reader)[::2]
        # the title row can contain an extra blank entry, this gets rid of it
        if not titleRow[-1]:
            titleRow.pop(-1)

        wavelengths = []
        absorbances = []
        # skip the column name row
        next(reader)
        for row in reader:
            if not row or not row[0]:
                break
            wavelengths.append(row[0])
            absorbances.append(row[1::2])

    titration.additionTitles = np.array(titleRow)
    titration.signalTitles = np.array(wavelengths, dtype=float)
    averageStep = abs(np.average(np.diff(titration.signalTitles)))
    titration.signalTitlesDecimals = int(-np.rint(np.log10(averageStep)))
    titration.signalTitles = np.round(titration.signalTitles,
                                      titration.signalTitlesDecimals)
    # transpose data so that the column is the wavelength
    titration.rawData = np.array(absorbances, dtype=float).T

    return [titration]


class CSVPopup(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        self.aborted = True
        super().__init__(*args, **kwargs)
        frame = ttk.Frame(self, padding=15)
        frame.pack(expand=True, fill="both")

        self.additionTitlesCheckbutton = ttk.Checkbutton(
            frame, text="Addition titles")
        self.signalTitlesCheckbutton = ttk.Checkbutton(
            frame, text="Signal titles")
        self.additionsRowsRadiobutton = ttk.Radiobutton(
            frame, value=0, text="Rows are additions, columns are signals")
        self.additionsColumnsRadiobutton = ttk.Radiobutton(
            frame, value=1, text="Rows are signals, columns are additions")
        self.continueButton = ttk.Button(
            frame, text="Continue", command=self.continueCommand)

        self.additionTitlesCheckbutton.pack(pady=2.5)
        self.signalTitlesCheckbutton.pack(pady=2.5)
        self.additionsRowsRadiobutton.pack(pady=2.5)
        self.additionsColumnsRadiobutton.pack(pady=2.5)
        self.continueButton.pack(pady=2.5, side='bottom')

        self.additionTitlesCheckbutton.invoke()
        self.signalTitlesCheckbutton.invoke()
        self.additionsRowsRadiobutton.invoke()

        # TODO: add a dropdown for "type of data", being one of UV, NMR,
        # continuous, or discrete. Add six entries below it (for quantities
        # and units), and have the UV and NMR options autofill them.

    def continueCommand(self):
        self.aborted = False
        self.hasSignalTitles = self.signalTitlesCheckbutton.instate(
            ["selected"])
        self.hasAdditionTitles = self.additionTitlesCheckbutton.instate(
            ["selected"])
        self.needTranspose = self.additionsColumnsRadiobutton.instate(
            ["selected"])
        self.destroy()


def readCSV(filePath):
    popup = CSVPopup()
    popup.wait_window(popup)
    if popup.aborted:
        return []

    titration = Titration()
    titration.title = os.path.basename(filePath)
    titration.continuous = False
    # TODO: remove placeholder
    titration.yQuantity = "δ"
    titration.yUnit = "ppm"

    with open(filePath, "r", newline='') as inFile:
        data = np.genfromtxt(inFile, dtype=str, delimiter=",")
        if popup.needTranspose:
            data = data.T
        if popup.hasAdditionTitles and popup.hasSignalTitles:
            titration.additionTitles = data[1:, 0]
            titration.signalTitles = data[0, 1:]
            titration.rawData = data[1:, 1:].astype(float)
        elif popup.hasAdditionTitles:
            titration.additionTitles = data[:, 0]
            titration.signalTitles = np.array(
                ["Signal " + str(i) for i in data.shape[1]])
            titration.rawData = data[:, 1:].astype(float)
        elif popup.hasSignalTitles:
            titration.additionTitles = np.array(
                ["Addition " + str(i) for i in data.shape[0]])
            titration.signalTitles = data[0, :]
            titration.rawData = data[1:, :].astype(float)
        else:
            titration.additionTitles = np.array(
                ["Addition " + str(i) for i in data.shape[0]])
            titration.signalTitles = np.array(
                ["Signal " + str(i) for i in data.shape[1]])
            titration.rawData = data

    return [titration]


def readNMR(filePath):
    # reads an MNova 1D peaks list
    additionTitles = []
    frequencies = []
    intensities = []
    plotFrequencies = []
    plotIntensities = []

    with open(filePath, "r", newline='') as inFile:
        reader = csv.reader(inFile, delimiter="\t")
        for row in reader:
            if not row or not row[0]:
                break
            additionTitles.append(row[1])
            currentFrequencies = [float(f) for f in row[2::2]]
            currentIntensities = [float(i) for i in row[3::2]]
            numSignals = len(currentFrequencies)
            # TODO: check that file is valid

            frequencies.append(currentFrequencies)
            intensities.append(currentIntensities)
            currentPlotFrequencies = [0]
            currentPlotFrequencies.extend(
                # append each frequency three times to create peak
                f for f in currentFrequencies for _ in range(3)
            )
            currentPlotFrequencies.append(0)
            plotFrequencies.append(currentPlotFrequencies)

            currentPlotIntensities = [0] * (numSignals * 3 + 2)
            # link the intensity to the middle of the three times it's present
            currentPlotIntensities[2::3] = currentIntensities
            plotIntensities.append(currentPlotIntensities)

        maxF = max(max(frequencies, key=max))
        minF = min(min(frequencies, key=min))

        numRows = len(frequencies)
        fig, axList = plt.subplots(
            numRows, 1, sharex=True, sharey=True,
            gridspec_kw={'hspace': 0, 'wspace': 0}
        )
        axList = np.flip(axList)
        axList[0].invert_xaxis()
        for ax, x, y in zip(axList, plotFrequencies, plotIntensities):
            x[0] = maxF + (0.1 * (maxF - minF))
            x[-1] = minF - (0.1 * (maxF - minF))
            ax.plot(x, y, color="black")
            ax.axes.yaxis.set_visible(False)
        fig.tight_layout()

        signals = []
        titles = []
        currentSignal = np.full(numRows, None)
        plottedPoints = np.copy(currentSignal)
        cycler = plt.rcParams['axes.prop_cycle'].by_key()['color']

        titration = Titration()
        titration.title = os.path.basename(filePath)
        titration.continuous = False
        titration.additionTitles = np.array(additionTitles)
        titration.yQuantity = "δ"
        titration.yUnit = "ppm"

        popup = tk.Toplevel()
        popup.title("Pick signals")

        frame = ttk.Frame(popup)
        frame.pack()

        entry = ttk.Entry(frame)
        entry.insert(0, "Signal title")

        def onClick(e):
            # click outside of plot area
            if e.inaxes is None:
                return
            # zoom/pan click
            if toolbar.mode != "":
                return
            i = np.where(axList == e.inaxes)[0][0]

            if e.button == 3:
                # left click
                if plottedPoints[i] is None:
                    return
                plottedPoints[i].remove()
                currentSignal[i] = None
                plottedPoints[i] = None
                canvas.draw()
                canvas.flush_events()
                return

            x = find_nearest(frequencies[i], e.xdata)
            y = intensities[i][frequencies[i].index(x)]
            currentSignal[i] = x
            if plottedPoints[i] is not None:
                # remove previous point
                plottedPoints[i].remove()
                pass

            plottedPoints[i] = e.inaxes.plot(x, y, 'o', color=cycler[0])[0]
            canvas.draw()
            canvas.flush_events()

        def next():
            signals.append(np.copy(currentSignal))
            titles.append(entry.get())

            currentSignal.fill(None)
            plottedPoints.fill(None)

            entry.delete(0, 'end')
            entry.insert(0, "Signal title")
            cycler.pop(0)

        def save():
            titration.rawData = np.array(signals, dtype=float).T
            titration.signalTitles = np.array(titles)
            popup.destroy()

        btn1 = ttk.Button(frame, text="Save signal", command=next)
        btn2 = ttk.Button(
            frame, text="Submit", style="success.TButton", command=save
        )
        for widget in (entry, btn1, btn2):
            widget.pack(side='left', padx=2, pady=5)

        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.draw()
        canvas.mpl_connect("button_press_event", onClick)
        canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(
            canvas, popup, pack_toolbar=False
        )
        toolbar.update()
        toolbar.pack(side="left", padx=padding)

        for ax in axList:
            # prevent zoom reset when adding points
            ax.autoscale(False)

        popup.wait_window(popup)
        plt.close("all")

        return [titration]

        # plt.show()


fileReaders = {
    "UV-Vis csv file": readUV,
    "NMR peak list": readNMR,
    "Universal csv file": readCSV
}
