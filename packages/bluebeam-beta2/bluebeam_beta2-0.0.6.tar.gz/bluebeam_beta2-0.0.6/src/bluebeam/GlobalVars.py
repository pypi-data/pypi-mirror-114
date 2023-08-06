class GlobalVars:

    def __init__(self):
        self._tick_rate = -1
        self._delta_time = -1
        self._instid = 100000
        self._boss1_death = 0

    @property
    def screen_size(self):
        return self._screen_size

    @screen_size.setter
    def screen_size(self, sz):
        self._screen_size = sz

    @property
    def tick_rate(self):
        return self._tick_rate

    @tick_rate.setter
    def tick_rate(self, tr):
        self._tick_rate = tr

    @property
    def delta_time(self):
        return self._delta_time

    @delta_time.setter
    def delta_time(self, dt):
        self._delta_time = dt

    @property
    def instid(self):
        return self._instid

    @instid.setter
    def instid(self, id):
        self._instid = id

    def getid(self):
        self._instid += 1
        return self._instid - 1

    def set_FX_vol(self, volume):
        self.FXVol = volume

    def set_music_vol(self, volume):
        self.musicVol = volume

    def get_FX_vol(self):
        return self.FXVol
    
    def get_music_vol(self):
        return self.musicVol
