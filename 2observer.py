#!/usr/bin/env python3

import abc
import datetime
import random

print('\nDesign pattens')

print('1 separate permanent and incapsulate flexible data/algorithms')
print('2 programm on the interface (abstract) level not realization')
print('3 composition better than inheritance')
print('4 Weak references')

print('\nObserver')
print('When state of one object changed related object has been notified')

print('\nSimple example - concrete realization')

class CurrentConditionDisplay:
    def update(self, temp, humidity, pressure):
        print(temp, humidity, pressure)


class StatisticDisplay:
    def update(self, temp, humidity, pressure):
        print(temp, humidity, pressure)


class ForecastDisplay:
    def update(self, temp, humidity, pressure):
        print(temp, humidity, pressure)


class ReportDisplay:
    def update(self, temp, humidity, pressure):
        print('Create report')
        with open('2observer-weather.txt', 'w') as file:
            date = datetime.datetime.now()
            report = f'---\n{date}\nTemperature: {temp}\nHumidity: {humidity}\nPressure: {pressure}\n'
            file.write(report)
        print('Done')


currentConditionDisplay = CurrentConditionDisplay()
statisticDisplay = StatisticDisplay()
forecastDisplay = ForecastDisplay()
reportDisplay = ReportDisplay()


class WeatherData:
    def get_temperature(self):
        return 20

    def get_humidity(self):
        return 10

    def get_pressure(self):
        return 750

    def mesurement_changed(self):
        temp = self.get_temperature()
        humidity = self.get_humidity()
        pressure = self.get_pressure()

        # concrete realization
        # flexible data
        currentConditionDisplay.update(temp, humidity, pressure)
        statisticDisplay.update(temp, humidity, pressure)
        forecastDisplay.update(temp, humidity, pressure)
        # need to change code
        reportDisplay.update(temp, humidity, pressure)


weather_data = WeatherData()

weather_data.mesurement_changed()


print('\nAdvanced example - subscription')
print('\none to many')

class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, obs=None, **kwargs):
        pass

class DisplayElement(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def display(self):
        pass

class WeakDisplay(Observer, DisplayElement):
    def __init__(self, weather_data):
        self.__weather_data = weather_data
        self.__weather_data.registerObserver(self)

    def __str__(self):
        return self.__class__.__name__


class CurrentConditionWeakDisplay(WeakDisplay):
    def __init__(self, weather_data):
        super().__init__(weather_data)
        self.__temp = 0
        self.__humidity = 0
        self.__pressure = 0

    def update(self, obs=None, **kwargs):
        print(f'\n-- Update: {self}')

        if isinstance(obs, WeatherData):
            self.__temp = obs.get_temperature()
            self.__humidity = obs.get_humidity()
            self.__pressure = obs.get_pressure()
        else:
            self.__temp = kwargs.get('temp', 0)
            self.__humidity = kwargs.get('humidity', 0)
            self.__pressure = kwargs.get('pressure', 0)

        self.display()
        print('-- Done')

    def display(self):
        date = datetime.datetime.now()
        print(
            f'{date}\nTemperature: {self.__temp}\nHumidity: {self.__humidity}\nPressure: {self.__pressure}'
        )


class StatisticWeakDisplay(WeakDisplay):
    def __init__(self, weather_data):
        super().__init__(weather_data)
        self.__temp = []
        self.__humidity = []
        self.__pressure = []

    def update(self, obs=None, **kwargs):
        print(f'\n-- Update: {self}')

        if isinstance(obs, WeatherData):
            self.__temp.append(obs.get_temperature())
            self.__humidity.append(obs.get_humidity())
            self.__pressure.append(obs.get_pressure())

        else:
            self.__temp.append(kwargs.get('temp', 0))
            self.__humidity.append(kwargs.get('humidity', 0))
            self.__pressure.append(kwargs.get('pressure', 0))

        self.display()
        print('-- Done')

    def display(self):
        date = datetime.datetime.now()
        av_temp = sum(self.__temp)/len(self.__temp) if self.__temp else 0
        av_hum = sum(self.__humidity)/len(self.__humidity) if self.__pressure else 0
        av_press = sum(self.__pressure)/len(self.__pressure) if self.__humidity else 0
        print(
            f'{date}\nTemperature: {av_temp}\nHumidity: {av_hum}\nPressure: {av_press}'
        )

class ForecastWeakDisplay(WeakDisplay):
    def __init__(self, weather_data):
        super().__init__(weather_data)
        self.__temp = 0
        self.__humidity = 0
        self.__pressure = 0

        self.__last_temp = None
        self.__last_humidity = None
        self.__last_pressure = None

    def update(self, obs=None, **kwargs):
        print(f'\n-- Update: {self}')

        self.__last_temp = self.__temp
        self.__last_humidity = self.__humidity
        self.__last_pressure = self.__pressure

        if isinstance(obs, WeatherData):
            self.__temp = obs.get_temperature()
            self.__humidity = obs.get_humidity()
            self.__pressure = obs.get_pressure()
        else:
            self.__temp = kwargs.get('temp', 0)
            self.__humidity = kwargs.get('humidity', 0)
            self.__pressure = kwargs.get('pressure', 0)

        self.display()
        print('-- Done')

    def display(self):
        date = datetime.datetime.now()
        print('Forecast')
        if self.__temp == self.__last_temp:
            print('Temperature more of the same')
        elif self.__temp > self.__last_temp:
            print('Temperature becomes higher')
        else:
            print('Temperature becomes lower')

        if self.__humidity == self.__last_humidity:
            print('Humidity more of the same')
        elif self.__humidity > self.__last_humidity:
            print('Humidity increases')
        else:
            print('Humidity decreases')

        if self.__pressure == self.__last_pressure:
            print('Pressure more of the same')
        elif self.__pressure > self.__last_pressure:
            print('Pressure goes up')
        else:
            print('Pressure goes down')


class HeatIndexWeakDisplay(WeakDisplay):
    def __init__(self, weather_data):
        super().__init__(weather_data)
        self.__temp = 0
        self.__humidity = 0
        self.__pressure = 0

    def update(self, obs=None, **kwargs):
        print(f'\n-- Update: {self}')

        if isinstance(obs, WeatherData):
            self.__temp = obs.get_temperature()
            self.__humidity = obs.get_humidity()
            self.__pressure = obs.get_pressure()
        else:
            self.__temp = kwargs.get('temp', 0)
            self.__humidity = kwargs.get('humidity', 0)
            self.__pressure = kwargs.get('pressure', 0)

        self.display()
        print('-- Done')

    @staticmethod
    def get_heat_index(t, rh):
        index = (
            (16.923 + (0.185212 * t) + (5.37941 * rh) - (0.100254 * t * rh)
                + (0.00941695 * (t * t))
                + (0.00728898 * (rh * rh))
                + (0.000345372 * (t * t * rh))
                - (0.000814971 * (t * rh * rh))
                + (0.0000102102 * (t * t * rh * rh))
                - (0.000038646 * (t * t * t))
                + (0.0000291583 *(rh * rh * rh))
                + (0.00000142721 * (t * t * t * rh))
                + (0.000000197483 * (t * rh * rh * rh))
                - (0.0000000218429 * (t * t * t * rh * rh))
                + 0.000000000843296 * (t * t * rh * rh * rh)
            )
            - (0.0000000000481975 * (t * t * t * rh * rh * rh))
        )
        return index

    def display(self):
        date = datetime.datetime.now()
        rh = self.__humidity/self.__pressure if self.__pressure else 0
        print(
            f'{date}\nHeat Index: {self.get_heat_index(self.__temp, rh)}'
        )


class ReportWeakDisplay(WeakDisplay):
    def __init__(self, weather_data):
        super().__init__(weather_data)
        self.__temp = 0
        self.__humidity = 0
        self.__pressure = 0

    def update(self, obs=None, **kwargs):
        print(f'\n-- Update: {self}')

        if isinstance(obs, WeatherData):
            self.__temp = obs.get_temperature()
            self.__humidity = obs.get_humidity()
            self.__pressure = obs.get_pressure()
        else:
            self.__temp = kwargs.get('temp', 0)
            self.__humidity = kwargs.get('humidity', 0)
            self.__pressure = kwargs.get('pressure', 0)

        self.display()
        print('-- Done')

    def display(self):
        file_name = "2observer-weak-weather.txt"
        print(f'Generate: {file_name}')
        with open('2observer-weak-weather.txt', 'a') as file:
            date = datetime.datetime.now()
            report = f'---\n{date}\nTemperature: {self.__temp}\nHumidity: {self.__humidity}\nPressure: {self.__pressure}\n'
            file.write(report)


class Observable(metaclass=abc.ABCMeta):
    def __init__(self):
        self.changed = False
        self.__observers = dict()

    def set_changed(self):
        self.changed = True

    def clear_changed(self):
        self.changed = False

    @property
    def has_changed(self):
        return self.changed

    def registerObserver(self, observer):
        self.__observers[id(observer)] = observer

    def removeObserver(self, observer):
        del self.__observers[id(observer)]

    def notifyObservers(self, **kwargs):
        if self.has_changed:
            for observer_id in self.__observers:
                if kwargs:
                    self.__observers.get(observer_id).update(**kwargs)
                else:
                    self.__observers.get(observer_id).update(self)

        self.clear_changed()

class WeatherData(Observable):

    def get_temperature(self):
        return self.__temp

    def get_humidity(self):
        return self.__humidity

    def get_pressure(self):
        return self.__pressure

    def mesurement_changed(self):
        self.set_changed()
        self.notifyObservers()
        # self.notifyObservers(temp=1,humidity=1,pressure=1)

    # test method
    def set_measurements(self):
        self.__temp = random.randrange(-10,10)
        self.__humidity = random.randrange(0,600)
        self.__pressure = random.randrange(-10, 1000)

        self.mesurement_changed()


class WeatherStation:
    def __init__(self):
        self.weather_data = WeatherData()

        currentConditionDisplay = CurrentConditionWeakDisplay(self.weather_data)
        statisticDisplay = StatisticWeakDisplay(self.weather_data)
        forecastDisplay = ForecastWeakDisplay(self.weather_data)
        heatDisplay = HeatIndexWeakDisplay(self.weather_data)
        reportDisplay = ReportWeakDisplay(self.weather_data)

    def run(self):
        self.weather_data.set_measurements()
        self.weather_data.set_measurements()
        self.weather_data.set_measurements()

ws = WeatherStation()

ws.run()


