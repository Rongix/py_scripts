
import pandas as pd
import os
import fnmatch
import numpy as np
import matplotlib.pyplot as plt


interactive = False
AngleDataFrames = []
ForceDataFrames = []

DictColumns = {
    "Sample": "Cykl chodu [%]",
    "RAFE": "Zgięcie w stawie skokowym (P)",
    "RAIE": "Ułożenie stopy w pł. czołowej (P)",
    "RKFE": "Zginanie i prostowanie kolana (P)",
    "RKAA": "Przywodzenie-odwodzenie kolana (P)",
    "RKIE": "Rotacja wewnętrzna zewnętrzna kolana (P)",
    "RHPFE": "Zginanie i prostowanie biodra (P)",
    "RHPAA": "Przywodzenie-odwodzenie biodra (P)",
    "RHPIE": "Rotacja wewnętrzna zewnętrzna biodra (P)",
    "RPTILT": "Pochylenie miednicy w płaszczyźnie strzałkowej (P)",
    "RPOBLI": "Pochylenie miednicy w płaszczyźnie czołowej (P)",
    "RPROT": "Rotacja miednicy (P)",
    "LAFE": "Zgięcie w stawie skokowym (L)",
    "LAIE": "Ułożenie stopy w pł. czołowej (L)",
    "LKFE": "Zginanie i prostowanie kolana (L)",
    "LKAA": "Przywodzenie-odwodzenie kolana (L)",
    "LKIE": "Rotacja wewnętrzna zewnętrzna kolana (L)",
    "LHPFE": "Zginanie i prostowanie biodra (L)",
    "LHPAA": "Przywodzenie-odwodzenie biodra (L)",
    "LHPIE": "Rotacja wewnętrzna zewnętrzna biodra (L)",
    "LPTILT": "Pochylenie miednicy w płaszczyźnie strzałkowej (L)",
    "LPOBLI": "Pochylenie miednicy w płaszczyźnie czołowej (L)",
    "LPROT": "Rotacja miednicy (L)",
    "fRGR.M.X": "Reakcja podłoża X (P)",
    "fRGR.M.Y": "Reakcja podłoża Y (P)",
    "fRGR.M.Z": "Reakcja podłoża Z (P)",
    "fLGR.M.X": "Reakcja podłoża X (L)",
    "fLGR.M.Y": "Reakcja podłoża Y (L)",
    "fLGR.M.Z": "Reakcja podłoża Z (L)",
}


def listOfFiles(regexExpression):
    filelist = []
    for files in os.listdir(os.curdir):
        if fnmatch.fnmatch(files, regexExpression):
            filelist.append(files)
    return filelist


def emtGetHeaderNData(
        fileToOpen,
        startingRow,
        filterRegex,
        startSliceIndex,
        endSliceIndex,
        preserveString,
        separator='\t'):
    data = pd.read_csv(fileToOpen, skiprows=startingRow,
                       sep=separator)
    data = data[data.columns.drop(list(data.filter(regex=filterRegex)))]
    data = data.rename(columns=lambda x: x.strip())
    # Remove unnecesary characters from string, preserve wanted strings
    data = data.rename(
        columns=lambda x: x[startSliceIndex:endSliceIndex] if (x != preserveString) else(x))
    return data.columns, data


def meanOfDataFrames(listOfFrames):
    # columnList = listOfFrames[0].columns
    # length = len(listOfFrames)
    # average = np.full_like(listOfFrames[0], 0)
    # for data in listOfFrames:
    #     average = average + data.to_numpy()
    # average = arrayDivisionByConst(average, length)
    # # Return pandas frame back
    # return pd.DataFrame(data=average, columns=columnList)

    # NEW IMPLEMENTATION LOLO
    columnList = listOfFrames[0].columns
    arrAverage = np.zeros(
        (listOfFrames[0].shape[0], listOfFrames[0].shape[1], len(listOfFrames)))
    for i, data in enumerate(listOfFrames):
        arrAverage[:, :, i] = data
    return pd.DataFrame(data=np.nanmean(arrAverage, axis=2), columns=columnList)


def arrayDivisionByConst(array, number):
    return array / number


def plotAll(df, paramDictionary, unit='', scaleAxis=False, tickStep=1, interactive=False, dpi=200, prefixText="", ext=".jpeg"):
    columnList = df.columns
    for column in columnList:
        plt.figure(dpi=dpi)
        plt.plot(df[columnList[0]], df[column])
        plt.title(paramDictionary[column])
        plt.xlabel(paramDictionary[columnList[0]])
        plt.ylabel(column + unit)

        if scaleAxis:
            plt.axis('scaled')
        plt.grid(linewidth=0.5, alpha=0.3, markeredgewidth=2)
        plt.savefig(prefixText + paramDictionary[column] + ext,
                    bbox_inches='tight', dpi=dpi)
        # DEBUG TEXT:
        print("Saving: {}{} to {}".format(
            prefixText, paramDictionary[column],  ext))
        if interactive:
            plt.tight_layout()
            plt.show()


def minmax(df):
    maximumangle = df.max().rename("Max")
    minimumangle = df.min().rename("Min")
    max_loc = df.idxmax().rename("Max index")
    min_loc = df.idxmin().rename("Min index")
    return pd.concat([maximumangle, max_loc,
                      minimumangle, min_loc], axis=1).T


### FORCE FILES ###

# List of files of Angle something... .emt
AngleFiles = listOfFiles('[Angle]*.emt')
print(AngleFiles)

# Creata data to hold all .emt arrays
for file in AngleFiles:
    columns, data = emtGetHeaderNData(
        file, 7, '(Unnamed)|(\.S$)', 1, -2, 'Sample')
    AngleDataFrames.append(data)

# Make mean array from data
MeanAngleArray = meanOfDataFrames(AngleDataFrames)

# DEBUG
print(MeanAngleArray)

# EXPORT
plotAll(MeanAngleArray, DictColumns, unit=' [°]', scaleAxis=False,
        tickStep=2, interactive=False, prefixText="S_Angle_")

plotAll(MeanAngleArray, DictColumns, unit=' [°]', scaleAxis=True,
        tickStep=2, interactive=False, prefixText="S_Angle_SCALED_")

# DEBUG
print(minmax(MeanAngleArray))

minmax(MeanAngleArray).to_excel('S_Angle_MinMax.xlsx')


### FORCE FILES ###

# List of files of Force something... .emt
ForceFiles = listOfFiles('[Force]*.emt')
print(ForceFiles)

# Creata data to hold all .emt arrays
for file in ForceFiles:
    columns, data = emtGetHeaderNData(
        file, 7, '(Unnamed)|(\.S\.)', 0, 8, 'Sample')
    ForceDataFrames.append(data)

# Make mean array from data
MeanForceArray = meanOfDataFrames(ForceDataFrames)

# DEBUG
print(MeanForceArray.columns)

# EXPORT
plotAll(MeanForceArray, DictColumns, unit=' [N]', scaleAxis=False,
        tickStep=2, interactive=False, prefixText="T_Force_")

plotAll(MeanForceArray, DictColumns, unit=' [N]', scaleAxis=True,
        tickStep=2, interactive=False, prefixText="T_Force_SCALED_")

# DEBUG
print(minmax(MeanForceArray))

minmax(MeanForceArray).to_excel('T_Force_MinMax.xlsx')
