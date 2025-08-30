import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QPalette, QLinearGradient, QBrush, QColor
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beautiful Weather App")
        self.setGeometry(200, 200, 420, 550)

        # Your API Key
        self.api_key = "YOUR API KEY"

        # Background Gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 600)
        gradient.setColorAt(0.0, QColor("#6dd5ed"))   # light blue
        gradient.setColorAt(1.0, QColor("#2193b0"))   # deep blue
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Title
        self.title = QLabel("🌤 Weather Forecast")
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setStyleSheet("color: white; margin: 15px;")
        self.title.setAlignment(Qt.AlignCenter)

        # City Input
        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("Enter City Name")
        self.input_city.setStyleSheet(
            "padding: 10px; border-radius: 15px; border: 2px solid white; background-color: #ffffff;"
        )

        # Button
        self.btn_get_weather = QPushButton("Get Weather")
        self.btn_get_weather.setStyleSheet(
            "QPushButton { background-color: #ffcc00; color: black; font-weight: bold; padding: 10px; border-radius: 15px; }"
            "QPushButton:hover { background-color: #ffdb4d; }"
        )

        # Weather Icon
        self.weather_icon = QLabel()
        self.weather_icon.setAlignment(Qt.AlignCenter)

        # Weather Info
        self.result_label = QLabel("Enter a city to see weather")
        self.result_label.setFont(QFont("Arial", 14))
        self.result_label.setStyleSheet("color: white; margin-top: 20px;")
        self.result_label.setAlignment(Qt.AlignCenter)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.input_city)
        vbox.addWidget(self.btn_get_weather)
        vbox.addWidget(self.weather_icon)
        vbox.addWidget(self.result_label)

        self.setLayout(vbox)

        # Button Event
        self.btn_get_weather.clicked.connect(self.get_weather)

    def get_weather(self):
        city = self.input_city.text().strip()
        if not city:
            self.result_label.setText("⚠ Please enter a city name!")
            return

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                self.result_label.setText("❌ City not found!")
                return

            city_name = data["name"]
            temp = data["main"]["temp"]
            desc = data["weather"][0]["main"]  # like Clear, Clouds, Rain, Mist, Snow

            # Weather Info Text
            self.result_label.setText(f"{city_name}\n🌡 {temp}°C\n{desc}")

            # Weather Icon Mapping with your downloaded icons
            icon_map = {
                "Clear": "icons/morning.png",       # morning sun
                "Clouds": "icons/resilience.png",   # cloud icon
                "Rain": "icons/rain.png",           # rain icon
                "Mist": "icons/mist.png",           # mist icon
                "Snow": "icons/snow.png",           # snow icon
                "Thunderstorm": "icons/rain.png"    # fallback
            }

            icon_file = icon_map.get(desc, "icons/resilience.png")  # default cloud
            pixmap = QPixmap(icon_file)
            self.weather_icon.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio))

        except Exception as e:
            self.result_label.setText(f"⚠ Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())

