
class MapRange:
    def __init__(self):
        self.center = '113.325055,23.137806'
        self.radiu = 5000
        self.bounds = None
        self.bound_corners = None

    def set_center(self, center:str):
        self.center_value = list(eval(self.center.value))
        lngmin, latmin = Transfer.mercator_to_lnglat(
            [- self.radiu.value] * 2,
            self.center_value
        )
        lngmax, latmax = Transfer.mercator_to_lnglat(
            [self.radiu.value] * 2,
            self.center_value
        )
        self.bounds = [lngmin, latmin, lngmax, latmax]
        self.bound_corners = [
            (lngmin, latmin),
            (lngmax, latmin),
            (lngmax, latmax),
            (lngmin, latmax)
        ]



