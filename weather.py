import os
import tkinter
from tkinter.font import Font
import requests
from PIL import ImageTk, Image
from enum import Enum
from datetime import datetime, date

# Maps openweathermap codes to icons
icon_map = {
    '01d': 'sunny.png',
    '01n': 'night_clear.png',
    '02d': 'partially_cloudy.png',
    '02n': 'night_cloudy.png',
    '03d': 'cloudy.png',
    '04d': 'very_cloudy.png',
    '09d': 'rain.png',
    '10d': 'heavy_rain.png',
    '11d': 'lightning.png',
    '13d': 'snow.png'
}

class WeatherResource(Enum):
    WEATHER=1
    FORECAST=2

class Weather(tkinter.Frame):
    def __init__(self, master:tkinter.Frame=None, **kwargs):
        self.API_KEY = "ba9d1024262f545b91d7fe3ed303a785"
        self.api_base = "http://api.openweathermap.org/data/2.5" 
        super().__init__(master, background='black')
        self.grid(row=0, column=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.constructTopFrame()
        self.constructBottomFrame()
        self.set_weather()

    def constructTopFrame(self):
        self.topFrame = tkinter.Frame(self, background='black')
        self.topFrame.grid(row=0, column=0, sticky='nsew')
        self.temperature = tkinter.Label(self.topFrame, background='black', fg='white')
        self.temperature.configure(
            font=Font(family="Avenir LT Std 35 Light", size=45, weight="normal")
        )
        self.img = None
        self.icon = tkinter.Label(self.topFrame, image=self.img)
        self.icon.place(relx=0.2, rely=0.45, anchor=tkinter.CENTER)
        self.temperature.place(relx=0.4, rely=0.45, anchor=tkinter.CENTER)

    def constructBottomFrame(self):
        self.bottomFrame = tkinter.Frame(self, background='green')
        self.bottomFrame.grid_rowconfigure(0, weight=1)
        self.bottomFrame.grid_columnconfigure(0, weight=1)
        self.bottomFrame.grid_columnconfigure(1, weight=1)
        self.bottomFrame.grid_columnconfigure(2, weight=1)
        self.bottomFrame.grid_columnconfigure(3, weight=1)
        self.bottomFrame.grid_columnconfigure(4, weight=1)
        self.bottomFrame.grid(row=1, column=0, sticky='nsew')

    def getWeather(self, resource:WeatherResource, **kwargs):
        api_url = "{base_url}/{resource}?zip={zipcode}&APPID={api_key}&units=imperial".format(
            base_url=self.api_base,
            resource=resource.name.lower(),
            zipcode="85255",
            api_key=self.API_KEY
        )
        for key, value in kwargs.items():
            api_url = "{url}&{k}={v}".format(
                url=api_url,
                k=key,
                v=value
            )
        response = requests.get(api_url)
        return response.json()

    def parse_forecast(self, data):
        """
        :rtype: Dict
        """
        forecast = dict()
        """
        Parse date from dt_text
        Forecast format:
        "<date>": {
            "hi": INT,
            "low": INT,
            "weather": TBD
        }
        """
        for day in data:
            cur_datetime = datetime.strptime(day['dt_txt'], '%Y-%m-%d %H:%M:%S')
            cur_day = date(cur_datetime.year, cur_datetime.month, cur_datetime.day)
            if cur_day not in forecast:
                forecast[cur_day] = {
                    "date": cur_day,
                    "hi": int(day['main']['temp_max']),
                    "low": int(day['main']['temp_min'])
                }
            else:
                forecast[cur_day]['hi'] = max(
                    forecast[cur_day]['hi'],
                    int(day['main']['temp_max'])
                )

                forecast[cur_day]['low'] = min(
                    forecast[cur_day]['low'],
                    int(day['main']['temp_min'])
                )
        return forecast

    def set_forecast(self):
        data = self.getWeather(WeatherResource.FORECAST)
        forecast = self.parse_forecast(data['list'])
        forecast_font = Font(family="Avenir LT Std 35 Light", size=15, weight="normal")
        i = 0
        for key in sorted(forecast.keys()):
            forecastFrame = tkinter.Frame(self.bottomFrame, background='black')
            forecastFrame.grid_columnconfigure(0, weight=1)
            forecastFrame.grid_rowconfigure(0, weight=2)
            forecastFrame.grid_rowconfigure(1, weight=1)
            forecastFrame.grid_rowconfigure(2, weight=1)
            forecastFrame.grid(row=0, column=i, sticky='nsew')
            date_label = tkinter.Label(forecastFrame, background='black', fg='white')
            date_label.configure(
                text='{month}/{day}'.format(
                    month=forecast[key]['date'].month,
                    day=forecast[key]['date'].day
                ),
                font=forecast_font
            )
            date_label.grid(row=1, column=0, sticky='nsew')
            temp_label = tkinter.Label(forecastFrame, background='black', fg='white')
            temp_label.configure(
                text='{hi}°/{low}°'.format(
                    hi=forecast[key]['hi'],
                    low=forecast[key]['low']
                ),
                font=forecast_font
            )
            temp_label.grid(row=2, column=0, sticky='nsew')
            i += 1

    def set_current_weather(self):
        data = self.getWeather(WeatherResource.WEATHER)
        temp_text = "{}°F".format(int(data['main']['temp']))
        self.temperature.configure(text=temp_text)
        img_path = '{cur_dir}/assets/{code}'.format(
            cur_dir=os.path.dirname(os.path.realpath(__file__)),
            code=icon_map[data['weather'][0]['icon']]
        )
        self.img = ImageTk.PhotoImage(Image.open(img_path))
        self.icon.image = self.img
        self.icon.configure(image=self.img)

    def set_weather(self):
        self.set_current_weather()
        self.set_forecast()
        self.after(300000, self.set_weather) # Every 5 minutes
        