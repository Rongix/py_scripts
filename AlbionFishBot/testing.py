from PIL import ImageGrab, Image
import numpy as np
import cv2
import time
import pyautogui
import random


# Minigame bar width region of recognition ~= 12.5 % Safe area: ~10.5%
# Minigame bar height region of recognition ~= 7.5%
# For 2560/1440px region of recognition from the center point is:

def now():
    return time.time()*1000.0


def recordScreenBox(x, y, width, height):
    screenshoot = ImageGrab.grab(bbox=(x, y, width+x, height+y))
    return np.array(screenshoot)


def recordScreenBoxFromPoint(x, y, width, height):
    # Screenshots are made from left down corner to right top corner
    left = x - width / 2
    top = y - height / 2
    right = x + width / 2
    bottom = y + height / 2
    screenshoot = ImageGrab.grab(
        bbox=(left, top, right, bottom))
    return np.array(screenshoot)


def imageProcessing(image):
    imageprocessing = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # imageprocessing = cv2.Canny(
    #     imageprocessing, threshold1=200, threshold2=300)
    return imageprocessing


def loadTemplate(path, scale=1):
    template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    width = int(template.shape[1] * scale)
    height = int(template.shape[0] * scale)
    dim = (width, height)
    template = cv2.resize(template, dim, interpolation=cv2.INTER_AREA)
    w, h = template.shape[::-1]
    return template, w, h


def setScaling(monitorsize, windowsize):
    return windowsize / monitorsize


def fishingstart():
    pyautogui.mouseDown(button='left')
    time.sleep(2)
    pyautogui.mouseUp(button='left')


def playfishingminigame():
    PlayMiniGame = True
    timeNow = time.time()*1000.0

    while (PlayMiniGame):

        continue

    pass


############################################################################
# % of the screen that bar takes (approx)
barArea = 0.1
monitorWidth = 2560
monitorHeigth = 1440
windowWidth = 2560/2
windowHeigth = 1440/2
scale = windowWidth/monitorWidth

# Minigame bar size example: (128, 72) 128 - 100% = fail |  0 - 0% = fail
minigameBar = imageProcessing(recordScreenBoxFromPoint(
    windowWidth / 2, windowHeigth / 2, windowWidth * barArea, windowHeigth * barArea))
print(minigameBar.shape[::-1])
minigameBarWidth = minigameBar.shape[::-1][0]
print(minigameBarWidth)


template, w, h = loadTemplate('SplawikNew.jpg', scale=0.6)
threshold = 0.8

time.sleep(3)


""" MAIN """
while (True):
    """ Quit if pressed Q key """
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break

    """ Starting fishing """
    pyautogui.mouseDown(button='left')
    time.sleep(2)
    pyautogui.mouseUp(button='left')

    average = 0
    sumOfAll = 0
    count = 0
    sum = 0
    lastAverageImg = 0
    averageImg = 0
    while (True):
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
        x, y = pyautogui.position()
        # print(x, y)
        # img = recordScreenBoxFromPoint(x, y, 100, 100)
        # img = imageProcessing(img)
        # img = cv2.Canny(
        #     img, threshold1=100, threshold2=320)
        # count = count + 1
        # mean = np.abs(np.mean(img))
        # sumOfAll = sumOfAll + mean
        # average = sumOfAll/count
        # print(average, average - mean)
        # cv2.imshow("test", img)
        # if (average - mean >= 0.5) and count >= 15:
        #     time.sleep(1)
        #     break
        # time.sleep(0.01)

        # TEMPORAL DETECTION
        # print(x, y)
        img = recordScreenBoxFromPoint(x, y, 70, 70)
        img = imageProcessing(img)
        img = cv2.Canny(
            img, threshold1=60, threshold2=80)
        averageImg = np.average(img)
        count = count + 1
        sum = sum + averageImg
        average = sum / count
        cv2.imshow("test", img)
        if count >= 15:
            print(np.abs(averageImg/average)/np.abs(lastAverageImg/average))
            if(np.abs(averageImg/average)/np.abs(lastAverageImg/average) >= 1.3):
                time.sleep(0.1 + random.random())
                break
        lastAverageImg = averageImg

    cv2.destroyAllWindows()
    pyautogui.click()

    """ Fishing minigame """
    time_last = now()
    while (now() - time_last <= 500):
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
        img = recordScreenBoxFromPoint(
            windowWidth / 2, windowHeigth / 2 + 60, windowWidth * barArea, windowHeigth * barArea)
        img = imageProcessing(img)
        # TODO DEBUG
        # print("fishin fishin")

        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
            time_last = now()
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            x = pt[0]/minigameBarWidth
            # print(x)
            if x < 0.65:
                pyautogui.mouseDown(button='left')
            else:
                pyautogui.mouseUp(button='left')
            cv2.imshow("test", img)
        time.sleep(0.02)

    print("FinishedMiniGame")
    pyautogui.mouseUp(button='left')
    time.sleep(2)

    """ Prepare for fishing """
    # Get mouse cords


cv2.destroyAllWindows()
