import numpy as np
from itertools import product
import pyqtgraph.opengl as gl
import OpenGL.GL.shaders as shaders

class Cubie:

  def __init__(self, index, data):
    self.index = index
    self.data = data
    self.faces = {
      'B':None,
      'F':None,
      'U':None,
      'D':None,
      'R':None,
      'L':None
    }    
    self.alpha = 0.8
    self.shader = 'balloon'
    self.glOptions = 'translucent'
    self.edgeColor = (0, 0, 0, 0.1)
    self.drawEdges = True
    self.plasticColor = (0, 0, 0, 1)
    self.brightness = 0.9
    self.face_show = {
      'B':True,
      'F':True,
      'U':True,
      'D':True,
      'R':True,
      'L':True
    }
    self.colors = {
      'B':(0, 0, self.brightness, self.alpha),
      'F':(self.brightness, self.brightness, self.brightness, self.alpha),
      'U':(self.brightness, self.brightness, 0, self.alpha),
      'D':(0, self.brightness, 0, self.alpha),
      'R':(self.brightness, 0.6, 0.4, self.alpha),
      'L':(self.brightness, 0, 0, self.alpha)
    }


def check_faces(cube, Cubies):
  x, y, z = cube.index
  for i,j,k in zip([x - 1, x + 1],[y - 1, y + 1],[z - 1, z + 1]):
    if 0 <= i <= 3:
      try:
        Cubies[i][y][z]
        if i == x - 1:
          cube.face_show['B'] = False
        else:
          cube.face_show['F'] = False
      except IndexError:
        pass
    if 0 <= j <= 3:
      try:
        Cubies[x][j][z]
        if j == y - 1:
          cube.face_show['L'] = False
        else:
          cube.face_show['R'] = False
      except IndexError:
        pass
    if 0 <= k <= 3:
      try:
        Cubies[x][y][k]
        if k == z - 1:
          cube.face_show['D'] = False
        else:
          cube.face_show['U'] = False
      except IndexError:
        pass

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

def get_faces(cube, face, x, y, z):
  return gl.GLSurfacePlotItem(
          x = x, y = y, z = z, color = cube.colors[face], edgeColor = cube.edgeColor, drawEdges = cube.drawEdges, shader = cube.shader, glOptions = cube.glOptions)

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
        Cubies[i][j][k].colors[face] = cube.plasticColor

    cube.faces['B'] = get_faces(cube, 'B', xx    , yx    , zx )
    cube.faces['F'] = get_faces(cube, 'F', xx + 1, yx    , zx )
    cube.faces['L'] = get_faces(cube, 'L', xy    , yy    , zy )
    cube.faces['R'] = get_faces(cube, 'R', xy    , yy + 1, zy )
    cube.faces['U'] = get_faces(cube, 'U', xz    , yz    , zz1)
    cube.faces['D'] = get_faces(cube, 'D', xz    , yz    , zz2)



