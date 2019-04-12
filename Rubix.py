from pynput.keyboard import Key, KeyCode, Listener
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
from collections import deque
from time import sleep
import CubieClass as Rubix
import numpy as np
import sys
pg.mkQApp()

class Visualizer():
    def __init__(self):
        self.traces = {}
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 15
        self.w.setGeometry(30, 30, 1080, 720)
        self.w.showFullScreen()
        self.w.show()
        self.phi = 0

        # gx = gl.GLGridItem()
        # gy = gl.GLGridItem()
        # gy.rotate(90, 0, 1, 0)
        # gz = gl.GLGridItem()
        # gz.rotate(90, 1, 0, 0)
        # gl.GLSurfacePlotItem(drawEdges = True)
        # self.w.addItem(gx)
        # self.w.addItem(gy)
        # self.w.addItem(gz)

        for cubie in Cubies.flatten():
          for face in cubie.faces.keys():
            cubie.faces[face].translate(-1.5,-1.5,-1.5)
            self.w.addItem(cubie.faces[face])

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self, cubie, xx, yx, xy, yy, zx, zy, xz, yz, zz1, zz2):
      cubie.faces['D'].setData(xz, yz, zz1)
      cubie.faces['U'].setData(xz, yz, zz2)
      cubie.faces['B'].setData(xx, yx, zx)
      cubie.faces['F'].setData(xx + 1, yx, zx)
      cubie.faces['L'].setData(xy, yy, zy)
      cubie.faces['R'].setData(xy, yy + 1, zy)

    def update(self):
      for cubie in Cubies.flatten():
        self.set_plotdata(cubie, *cubie.data)

    def rotate(self, Cubes, check, direction):
      while abs(self.phi) < 90:
        for cubie in Cubes.flatten():
          for face in cubie.faces.values():
            face.rotate((-1 + check), *direction)
        sleep(0.003)
        self.phi += 1
      self.phi = 0

    def rotateU(self, check, layers):
      layer = [k for k,v in enumerate(layers) if v]
      self.rotate(Cubies[:, :, layer[0]], check, (0, 0, 1))
      Cubies[:, :, layer[0]] = np.rot90(Cubies[:, :, layer[0]], 3 - check)

    def rotateR(self, check, layers):
      layer = [k for k,v in enumerate(layers) if v]
      self.rotate(Cubies[:, layer[0], :], check, (0, 1, 0))
      Cubies[:, layer[0], :] = np.rot90(Cubies[:, layer[0], :], 1 + check)

    def rotateF(self, check, layers):
      layer = [k for k,v in enumerate(layers) if v]
      self.rotate(Cubies[layer[0], :, :], check, (1, 0, 0))
      Cubies[layer[0], :, :] = np.rot90(Cubies[layer[0], :, :], 3 - check)

    def animation(self):
      timer = QtCore.QTimer()
      timer.timeout.connect(self.update)
      timer.start(20)
      self.start()

def on_press(key):
  check = 0 if keys.pop() != Key.shift else 2
  if key == KeyCode(char = '1'):
    v.rotateF(check, [True, False, False]) #Back Face
  elif key == KeyCode(char = '2'):
    v.rotateF(check, [False, True, False]) #MiddleX Face
  elif key == KeyCode(char = '3'):
    v.rotateF(check, [False, False, True]) #Front Face
  elif key == KeyCode(char = '4'):
    v.rotateR(check, [True, False, False]) #Left Face
  elif key == KeyCode(char = '5'):
    v.rotateR(check, [False, True, False]) #MiddleY Face
  elif key == KeyCode(char = '6'):
    v.rotateR(check, [False, False, True]) #Right Face
  elif key == KeyCode(char = '7'):
    v.rotateU(check, [True, False, False]) #Top Face
  elif key == KeyCode(char = '8'):
    v.rotateU(check, [False, True, False]) #MiddleZ Face
  elif key == KeyCode(char = '9'):
    v.rotateU(check, [False, False, True]) #Bottom Face
  keys.append(key)
  if key == Key.esc:
    pg.exit()

    # Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
  keys = deque([''])
  Cubies = np.empty(shape = (3, 3, 3), dtype = object)
  Rubix.make_cube(Cubies)
  with Listener(on_press = on_press) as listener:
    v = Visualizer()
    v.animation()
    listener.join()
