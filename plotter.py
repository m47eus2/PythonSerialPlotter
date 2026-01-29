import serial
import numpy as np
import sys
from collections import deque
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

PORT = "/dev/ttyACM0"
#PORT = "COM5"
BAUDRATE = 115200

serialPort = serial.Serial(PORT, BAUDRATE, timeout=0.01)

app = QtWidgets.QApplication(sys.argv)
win = pg.GraphicsLayoutWidget(title="Plotter")
plot = win.addPlot()
curve1 = plot.plot(pen=pg.mkPen(width=2), symbol="o", symbolSize=6, symbolBrush="c")
curve2 = plot.plot(pen=pg.mkPen(width=2), symbol="o", symbolSize=6, symbolBrush="y")

legend = plot.addLegend()
legend.addItem(curve1, "Angle")
legend.addItem(curve2, "Set Value")

plot.showGrid(x=True, y=True)

data1 = deque(maxlen=300)
data2 = deque(maxlen=300)

angle_log = []

def getData():
    while serialPort.in_waiting:
        try:
            line = serialPort.readline().decode("utf-8").rstrip()
            line = line.split(":")

            # if line[0]==">RollFused":
            #     data.append(float(line[1]))

            # if line[0]==">RollGyro":
            #     data.append(float(line[1]))

            # if line[0]==">RollAcc":
            #     data.append(float(line[1]))

            if line[0]==">Angle":
                angle = float(line[1])
                angle_log.append(angle)
                data1.append(angle)

            if line[0]==">Encoder":
                data2.append(int(line[1]))

        except ValueError:
            pass

    curve1.setData(data1)
    curve2.setData(data2)

def closeEvent(event):
    np.save("angle_log.npy", np.array(angle_log))
    serialPort.close()
    event.accept()

win.closeEvent = closeEvent

dataTimer = pg.QtCore.QTimer()
dataTimer.timeout.connect(getData)
dataTimer.start(10)

win.show()
sys.exit(app.exec_())