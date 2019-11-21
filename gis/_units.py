class TileIndex():
    def __init__(self, x:int, y:int, zoom:int):
        self._data=[x,y,zoom]

    @property
    def x(self):
        return self._data[0]

    @property
    def y(self):
        return self._data[1]

    @property
    def zoom(self):
        return self._data[2]

    def __getitem__(self, i):
        return self._data[i]


