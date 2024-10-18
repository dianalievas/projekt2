import requests # Library to make HTTP requests
import tkinter as tk # Library to create graphical user interface
from tkinter import messagebox 

# Class that handles the weather data from Open-Mateo API
class WeatherAPI:
    def __init__(self,city_name):
        self.latitude, self.longitude = self.get_coordinates(city_name) 
        self.timezone = "Europe/Stockholm"  # Hardcoded timezone
        # API URL to get current weather data from the coordinates 
        self.api_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&current_weather=true&timezone={self.timezone}"
        self.city_name = city_name
   
    # Function to get the city name using a geocoding service 
    def get_coordinates(self, city_name):
        geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key=90b1092247d448be87607ef15de87a82"
        response = requests.get(geocode_url)
        if response.status_code == 200:
            results = response.json()
            if results['results']:
                # Return latitude and longitude from results
                latitude = results['results'][0]['geometry']['lat']
                longitude = results['results'][0]['geometry']['lng']
                return latitude, longitude
            else:
                raise ValueError("City not found, try again and check the spelling.")
        else: 
            raise ValueError(f"Error from input of coordinates {response.status_code} ")      
    
    def get_weather_data(self):
        # HTTP request to Open-Mateo API
        response = requests.get(self.api_url) # an HTTP request to Open-Mateo API
        if response.status_code == 200: # checks if the API request was succesful 
            return response.json().get("current_weather") # Returning the weather data as JSON
        else:
            print(f"Error getting weather: {response.status_code} ")
            return None
        
# Class that displays the weather in a GUI window    
class WeatherDisplay:
    def __init__(self, weather_data, city_name, latitude, longitude):
        # Initialize with weather data, city name and coordinates
        self.weather_data = weather_data
        self.city_name = city_name
        self.latitude = latitude
        self.longitude = longitude

    # Function to display the weather information in GUI window
    def display_weather(self):
        root = tk.Tk() # Creates a tkinter window
        root.title("Weather Information: ")
        root.geometry("400x300") # Window size
        root.configure(bg="#2E2E2E") #Window color

        weather_frame = tk.Frame(root, bg="#2E2E2E", width=500, height=400)
        weather_frame.pack(pady=20)

        title_label = tk.Label(weather_frame, text=f"Weather in {self.city_name}", font=("Arial", 16), bg="#2E2E2E", fg="white")
        title_label.pack()

        # Creating a text widget to display the weather information 
        weather_info_text = tk.Text(weather_frame,height=15, width=60, font=("Arial", 14), bg="#ffffff", fg="black")
        weather_info_text.pack(padx=10, pady=10)

        # Coordinates and city name for the text widget 
        weather_info_text.insert(tk.END, f"Coordinates: {self.latitude}, {self.longitude}\n\n")
        
        if self.weather_data:
            #Extrsct weather data
            weather_time = self.weather_data.get("time")
            temperature = self.weather_data.get("temperature")
            windspeed = self.weather_data.get("windspeed")
            winddirection = self.weather_data.get("winddirection")
            is_day = self.weather_data.get("is_day")

            if temperature >= 15:
                emoji = "\U00002600" #Sun emoji for warm weather
            else:
                emoji = "\U00002601" #Cloud emoji for colder weather

            wind_emoji = "\U0001F32B"
            clock_emoji = "\U0001F553"
            wind2_emoji = "\U0001F32C"

            if is_day:
                day_night_emoji = "\U0001F305" #Sunrise emoji if its daytime
            else:
                day_night_emoji = "\U0001F307" #Sunset emoji if its nightime

            weather_info_text.insert(tk.END, f"Temperature: {temperature}°C {emoji}\n\n")
            weather_info_text.insert(tk.END, f"Time: {weather_time} {clock_emoji}\n\n")
            weather_info_text.insert(tk.END, f"Windspeed: {windspeed} m/s {wind_emoji} \n\n")
            weather_info_text.insert(tk.END, f"Winddirection: {winddirection}° {wind2_emoji}\n\n")
            weather_info_text.insert(tk.END, f"Daytime: {'Yes' if is_day else 'No'} {day_night_emoji}\n\n")

            weather_info_text.config(state=tk.DISABLED)

        root.mainloop() # Starts tkinter loop to show window

# Function to get weather data when the button is clicked in the GUI, insert exact coordinates
def get_weather(city_entry):
    city_name = city_entry.get()
    print(f"The entered city: {city_name}")

    try:
        weather_api = WeatherAPI(city_name)
        current_weather_data = weather_api.get_weather_data()
        print(current_weather_data)

        if current_weather_data is None:
            raise ValueError("Unable to get weather data.")
        # Displays weather data in a new window
        weather_display = WeatherDisplay(current_weather_data, weather_api.city_name, weather_api.latitude, weather_api.longitude)
        weather_display.display_weather()

    except ValueError as e:
        # Error message if there is an issue retrieving data
        messagebox.showerror("Error getting weather data", f"Could not retrieve data for '{city_name}'. Please check the spelling and try again.")
        print(f"Error: {e}")

# Main function that creates the GUI    
def main():
    
    root = tk.Tk()
    root.title("Europe Weather App")
    root.geometry("400x300")
    root.configure(bg="#2E2E2E")

    # Creating label and input field for city name 
    tk.Label(root, text="Enter city: ").pack()
    city_entry = tk.Entry(root, width=30)
    city_entry.pack(pady=5)

    # Creating a button that get the weather when clicked
    get_weather_button = tk.Button(root, text="Get Weather", command=lambda: get_weather(city_entry))
    get_weather_button.pack(pady=5)
    
    #Button to exit the app
    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=5)

    root.mainloop() # Start tkinters main loop for the GUI

# If the script is run directly, call the main function 
if __name__ == "__main__":
    main()