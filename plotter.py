import serial
import sys
from collections import deque
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

PORT = "/dev/ttyACM0"
BAUDRATE = 115200

serialPort = serial.Serial(PORT, BAUDRATE, timeout=0.1)

app = QtWidgets.QApplication(sys.argv)
win = pg.GraphicsLayoutWidget(title="Plotter")
plot = win.addPlot()
curve = plot.plot(pen=pg.mkPen(width=2), symbol="o", symbolSize=6, symbolBrush="c")

plot.showGrid(x=True, y=True)

data = deque(maxlen=2000)

def update():
    try:
        line = serialPort.readline().decode("utf-8").rstrip()
        line = line.split(":")
        if line[0]==">RollFused":
            data.append(float(line[1]))
            curve.setData(data)
    except ValueError:
        pass

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)

win.show()
sys.exit(app.exec_())