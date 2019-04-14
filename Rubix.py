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
      self.w = gl.GLViewWidget()
      self.w.opts['distance'] = 15
      self.w.opts['fov'] = 70
      self.w.opts['elevation'] = 25
      self.w.opts['azimuth'] = 210
      self.w.setGeometry(30, 30, 1080, 720)
      # self.w.showFullScreen()
      self.w.setBackgroundColor('w')
      self.w.show()
      self.phi = 0

      # gx = gl.GLGridItem()
      # gy = gl.GLGridItem()
      # gz = gl.GLGridItem()
      # gy.rotate(90, 0, 1, 0)
      # gz.rotate(90, 1, 0, 0)
      # self.w.addItem(gx)
      # self.w.addItem(gy)
      # self.w.addItem(gz)

      for cubie in Cubies.flatten():
        for face in cubie.faces.keys():
          cubie.faces[face].translate(-1.5,-1.5,-1.5)
          # if not cubie.face_show[face]:
          self.w.addItem(cubie.faces[face])

    @staticmethod
    def start():
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
        sleep(1/animation_speed)
        self.phi += 1
      self.phi = 0

    def rotateU(self, check, layer):
      self.rotate(Cubies[:, :, layer], check, (0, 0, 1))
      Cubies[:, :, layer] = np.rot90(Cubies[:, :, layer], 3 - check)

    def rotateR(self, check, layer):
      self.rotate(Cubies[:, layer, :], check, (0, 1, 0))
      Cubies[:, layer, :] = np.rot90(Cubies[:, layer, :], 1 + check)

    def rotateF(self, check, layer):
      self.rotate(Cubies[layer, :, :], check, (1, 0, 0))
      Cubies[layer, :, :] = np.rot90(Cubies[layer, :, :], 3 - check)

    def animation(self):
      self.update()
      # timer = QtCore.QTimer()
      # timer.timeout.connect(self.update)
      # timer.start()
      self.start()

def on_press(key):
  check = 0 if keys.pop() != Key.shift else 2
  if key == KeyCode(char = 'b'):
    v.rotateF(check, 0) #Back Face
  elif key == KeyCode(char = 'f'):
    v.rotateF(check, 2) #Front Face
  elif key == KeyCode(char = 'l'):
    v.rotateR(check, 0) #Left Face
  elif key == KeyCode(char = 'r'):
    v.rotateR(check, 2) #Right Face
  elif key == KeyCode(char = 'd'):
    v.rotateU(check, 0) #Down Face
  elif key == KeyCode(char = 'u'):
    v.rotateU(check, 2) #Up Face
  keys.append(key)
  if key == Key.space:
    # randomize(30)
    algo()
  if key == Key.enter:
    v.w.opts['fov'] = 70
    v.w.opts['elevation'] = 25
    v.w.opts['azimuth'] = 210
    v.update()
  if key == Key.esc:
    pg.exit()

def algo():
  for move in ['u','r','shift','u','shift','r']:
    key = KeyCode(char = move) if move != 'shift' else Key.shift
    on_press(key)
  if not np.array_equal(Cubies, Original_Cube):
    algo()

def randomize(n = 20):
  from random import choice
  random_moves = deque([])
  for _ in range(n):
    key = choice(['u','d','r','l','f','b','shift'])
    random_moves.append(KeyCode(char = key)) if key != 'shift' else random_moves.append(Key.shift)
  for n,move in enumerate(random_moves):
    on_press(move)

    # Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
  animation_speed = 250
  keys = deque([''])
  Cubies = np.empty(shape = (3, 3, 3), dtype = object)
  Rubix.make_cube(Cubies)
  Original_Cube = np.copy(Cubies)
  with Listener(on_press = on_press) as listener:
    v = Visualizer()
    v.animation()
    listener.join()
