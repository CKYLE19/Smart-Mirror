import os
import tkinter
from tkinter.font import Font
import requests
from PIL import ImageTk, Image
from enum import Enum
from datetime import datetime

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
        super().__init__(master, background='black', height=master.winfo_height(), width=master.winfo_width()/3)
        self.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
        self.constructTopFrame()
        self.constructBottomFrame()
        self.set_weather()

    def constructTopFrame(self):
        self.topFrame = tkinter.Frame(self, background='black', height=self.winfo_height()/2, width=self.winfo_width())
        self.topFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)
        self.temperature = tkinter.Label(self.topFrame, background='black', fg='white')
        self.font = Font(family="Avenir LT Std 35 Light", size=45, weight="normal")
        self.temperature.configure(font=self.font)
        self.img = None
        self.icon = tkinter.Label(self.topFrame, image=self.img)
        self.icon.place(relx=0.15, rely=0.2, anchor=tkinter.CENTER)
        self.temperature.place(relx=0.4, rely=0.2, anchor=tkinter.CENTER)

    def constructBottomFrame(self):
        self.bottomFrame = tkinter.Frame(self, background='green', height=self.winfo_height()/2, width=self.winfo_width())
        self.bottomFrame.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=tkinter.YES)

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
            time = datetime.strptime(day['dt_txt'], '%Y-%m-%d %H:%M:%S')
            print(time.day)
        return forecast

    def set_forecast(self):
        data = self.getWeather(WeatherResource.FORECAST)
        forecast = self.parse_forecast(data['list'])

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
        