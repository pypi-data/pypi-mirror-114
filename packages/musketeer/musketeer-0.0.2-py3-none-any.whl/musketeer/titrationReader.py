import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd

import csv
import numpy as np
import re
import sys
from pkg_resources import packaging

from .titration import Titration

# need to tell matplotlib to use the tkinter backend, otherwise the scale
# of figures can get messed up if it would default to a different backend
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt  # noqa
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # noqa
from .navigationToolbar2Tk import NavigationToolbar2Tk # noqa
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
        sys.exit("No filetype selected.")
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
    if filePath == "":
        sys.exit("No input file selected.")
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
    # set default parameters for UV-Vis titrations
    titration.continuous = True
    titration.contributors = "both"
    titration.labelX = "λ (nm)"
    titration.labelY = "Abs (AU)"
    titration.legendSuffix = "nm"

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

    titration.additionTitles = titleRow
    # TODO: use appropriate number of significate figures (affects spinbox and
    # discrete-from-continuous legend)
    titration.signalTitles = np.array(wavelengths, dtype=np.float)
    # transpose data so that the column is the wavelength
    titration.rawData = np.array(absorbances, dtype=np.float).T
    titration.rowFilter = np.ones(titration.rawData.shape[0], dtype=bool)
    titration.columnFilter = np.ones(titration.rawData.shape[1], dtype=bool)

    return [titration]


def readNMR(filePath):
    # TODO: proof of concept works, convert to class
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
        titration.continuous = False
        titration.additionTitles = np.array(additionTitles)

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
            titration.rawData = np.array(signals, dtype=np.float).T
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


def readCustom(filePath):
    # TODO: decide on standard format & implement
    raise NotImplementedError


fileReaders = {
    "UV-Vis csv file": readUV,
    "NMR peak list": readNMR,
    "Universal csv file": readCustom
}
