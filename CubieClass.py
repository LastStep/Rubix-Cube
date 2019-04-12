import numpy as np
from itertools import product
import pyqtgraph.opengl as gl

class Cubie:

  def __init__(self, index, data):
    self.index = index
    self.data = data
    self.faces = {}
    self.face_show = {
                      'B':True,
                      'F':True,
                      'U':True,
                      'D':True,
                      'R':True,
                      'L':True
                     }
    self.colors = {
                    'B':(0, 0, 1, 0),
                    'F':(1, 1, 1, 0),
                    'U':(1, 1, 0, 0),
                    'D':(0, 1, 0, 0),
                    'R':(1, 0.5, 1, 0),
                    'L':(1, 0, 0, 0)
                  }

def check_faces(cube, Cubies):
  x, y, z = cube.index
  try:
    Cubies[x+1][y][z]
    cube.face_show['F'] = False
  except IndexError:
    pass
  # try:
  #   Cubies[x-1][y][z]
  #   cube.face_show['B'] = False
  # except IndexError:
  #   pass
  try:
    Cubies[x][y+1][z]
    cube.face_show['R'] = False
  except IndexError:
    pass
  # try:
  #   Cubies[x][y-1][z]
  #   cube.face_show['L'] = False
  # except IndexError:
  #   pass
  try:
    Cubies[x][y][z+1]
    cube.face_show['U'] = False
  except IndexError:
    pass
  # try:
  #   Cubies[x][y][z-1]
  #   cube.face_show['D'] = False
  # except IndexError:
  #   pass

def cubie_data(index):
  i, j, k = index
  xz = np.array([0, 1])+i
  yz = np.array([0, 1])+j
  zz1 = np.array([[0, 0], [0, 0]])+k
  zz2 = np.array([[1, 1], [1, 1]])+k
  xx = np.array([0, 0])+i
  yx = np.array([0, 1])+j
  xy = np.array([0, 1])+i
  yy = np.array([0, 0])+j
  zx = np.array([[0, 0], [1, 1]])+k
  zy = np.array([[0, 1], [0, 1]])+k
  return xx, yx, xy, yy, zx, zy, xz, yz, zz1, zz2

def make_cube(Cubies):
  for i,j,k in product([0,1,2],[0,1,2],[0,1,2]):
    index = (i,j,k)
    data = cubie_data(index)
    Cubies[i][j][k] = Cubie(index, data)

  for i, j, k in product([0, 1, 2], [0, 1, 2], [0, 1, 2]):
    cube = Cubies[i][j][k]
    xx, yx, xy, yy, zx, zy, xz, yz, zz1, zz2 = cube.data

    check_faces(cube, Cubies)

    for face, value in Cubies[i][j][k].face_show.items():
      if not value:
        Cubies[i][j][k].colors[face] = (0, 0, 0, 0)

    cube.faces['B'] = gl.GLSurfacePlotItem(
        x = xx, y = yx, z = zx, color = cube.colors['B'], edgeColor = (0, 0, 0, 0), drawEdges = True, shader = None)
    cube.faces['F'] = gl.GLSurfacePlotItem(
        x = xx + 1, y = yx, z = zx, color = cube.colors['F'], edgeColor = (0, 0, 0, 0), drawEdges = True, shader = None)

    cube.faces['L'] = gl.GLSurfacePlotItem(
        x = xy, y = yy, z = zy, color = cube.colors['L'], edgeColor = (0, 0, 0, 0), drawEdges = True, shader = None)
    cube.faces['R'] = gl.GLSurfacePlotItem(
        x = xy, y = yy + 1, z = zy, color = cube.colors['R'], edgeColor = (0, 0, 0, 0), drawEdges = True, shader = None)

    cube.faces['U'] = gl.GLSurfacePlotItem(
        x = xz, y = yz, z = zz1, color = cube.colors['U'], edgeColor = (0, 0, 0, 0), drawEdges = True, shader = None)
    cube.faces['D'] = gl.GLSurfacePlotItem(
        x = xz, y = yz, z = zz2, color =cube.colors['D'], edgeColor = (0, 0, 0, 0), drawEdges = True, shader = None)

