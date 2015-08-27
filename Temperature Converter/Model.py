from Notify import notify, NotifyPropertyChangedBase
from threading import Lock

class Model(object):
    @staticmethod
    def convert_celsius_to_fahrenheit(celsius):
        try:
            return str((float(celsius) * 9/5) + 32)
        except ValueError:
            return ''
    @staticmethod
    def convert_fahrenheit_to_celsius(fahrenheit):
        try:
            return str((float(fahrenheit) - 32) * 5/9)
        except ValueError:
            return ''

class ViewModel(NotifyPropertyChangedBase):
    _celsius = 0.0
    _fahrenheit = Model.convert_celsius_to_fahrenheit(0)
    _lock = Lock()

    @notify
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        self._celsius = value
        if not self._lock.acquire(False): return
        self.fahrenheit = Model.convert_celsius_to_fahrenheit(value)
        self._lock.release()

    @notify
    def fahrenheit(self):
        return self._fahrenheit

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._fahrenheit = value
        if not self._lock.acquire(False): return
        self.celcius = Model.convert_fahrenheit_to_celsius(value)
        self._lock.release()