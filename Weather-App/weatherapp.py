import sys
import requests 
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from datetime import datetime, UTC, timedelta


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.description_label = QLabel(self)
        self.sunset_label = QLabel(self)
        self.sunrise_label = QLabel(self)
        self.feels_like_label = QLabel(self)
        self.name = QLabel(self)
        self.initUI()
    
    def initUI(self):
    
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.feels_like_label)
        vbox.addWidget(self.sunrise_label)
        vbox.addWidget(self.sunset_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.name)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.feels_like_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.sunrise_label.setAlignment(Qt.AlignCenter)
        self.sunset_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.feels_like_label.setObjectName("feels_like_label")
        self.description_label.setObjectName("description_label")
        self.sunrise_label.setObjectName("sunrise_label")
        self.sunset_label.setObjectName("sunset_label")
        self.name.setObjectName("name")

        self.setStyleSheet("""
            QLabel, QPushButton{
                           font-family: calibri;  
                           }   
            QLabel#city_label{
                            font-size: 40px;
                            font-style; italic;
                           }
            QLineEdit#city_input{
                           font-size: 40px;
                           }
            QPushButton#get_weather_button{
                           font-size: 30px;
                           font-weight: bold;
                           }
            QLabel#temperature_label{
                           font-size: 75px;
                           }
            QLabel#description_label{
                           font-size: 30px;
                           font-weight: bold;
                           }
            QLabel#sunrise_label{
                           font-size = 50px;
                           }
            QLabel#sunset_label{
                           font-size = 50px;
                           }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        
        api_key = "<change this for your api key>"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unathorised:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 501:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 502:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            print("Connection Error:\n Check your internet connection")
        except requests.exceptions.Timeout:
            print("Timeout Error:\n The request timed out")
        except requests.exceptions.TooManyRedirects:
            print("Too Many Redirects:\n Check the URL")
        except requests.exceptions.RequestException as req_error:
            print(f"Request Error:\n{req_error}")


    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.description_label.clear()
        self.sunrise_label.clear()
        self.sunset_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 50px;")
        self.sunset_label.setStyleSheet("font-size: 30px;")
        self.sunrise_label.setStyleSheet("font-size: 30px;")
        self.feels_like_label.setStyleSheet("font-size: 30px;")
        self.name.setStyleSheet("font-size: 15px;")

        temperature_k = data["main"]["temp"]
        feels_like_description = data["main"]["feels_like"]
        temperature_c = temperature_k - 273.15
        temperature_feels_like_c = feels_like_description - 273.15
        weather_description = data["weather"][0]["description"]
        sunrise_description = data["sys"]["sunrise"]
        sunset_description = data["sys"]["sunset"]
        timezone_offset = data["timezone"]

        sunrise_time = datetime.fromtimestamp(sunrise_description, tz=UTC) + timedelta(seconds = timezone_offset)
        sunset_time = datetime.fromtimestamp(sunset_description, tz=UTC) + timedelta(seconds = timezone_offset)

        self.temperature_label.setText(f"{temperature_c:.1f}°C")
        self.description_label.setText(weather_description)
        self.sunrise_label.setText(f"Sunrise: {sunrise_time.strftime("%H:%M")}")
        self.sunset_label.setText(f"Sunset: {sunset_time.strftime("%H:%M")}")
        self.feels_like_label.setText(f"Feels like: {temperature_feels_like_c:.1f}°C")
        self.name.setText("Made by Zynq")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
