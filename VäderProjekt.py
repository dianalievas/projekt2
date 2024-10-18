import requests # Requets-library to make HTTP requests
import tkinter as tk # Importing tkinter to create a graphical user interface

# Class that handles the weather data from Open-Mateo API
class WeatherAPI:
    def __init__(self,latitude,longitude):
        self.latitude = latitude 
        self.longitude = longitude 
        self.timezone = "Europe/Stockholm"  # Hardcoded timezone
        # API URL to get curretn weather data from the coordinates 
        self.api_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&current_weather=true&timezone={self.timezone}"
        self.city_name = self.get_city_name()

    # Function to get the city name using a geocoding service 
    def get_city_name(self):
        # API URL to get the name of the city based on the coordinates 
        geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={self.latitude}+{self.longitude}&key=90b1092247d448be87607ef15de87a82"
        response = requests.get(geocode_url)
        if response.status_code == 200:
            results = response.json()
            # If the results are avaible, return the citys name, otherwise dont
            if results['results']:
                city = results['results'][0]['components'].get('city','Unindentified city')
                return city
        return "Unidentified city"
    # Function to get current weather data from Open-Mateo API
    def get_weather_data(self):
        response = requests.get(self.api_url) # an HTTP requets to Open-Mateo API
        if response.status_code == 200: # checks if the API request was succesful 
            return response.json().get("current_weather") # Returning the weather data as JSON
        else:
            print(f"Error getting weather: {response.status_code} ")
            return None
        
# Class that displays the weather in a GUI window by tkinter    
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

        # Creating a text widget to display the weather information 
        weather_info_text = tk.Text(root, height=10, width=50)
        weather_info_text.pack()

        # Inserting coordinates and city name into the text widget 
        weather_info_text.insert(tk.END, f"Coordinates: {self.latitude}, {self.longitude}\n")
        weather_info_text.insert(tk.END, f"{self.city_name}\n")

        # Checking if there is weather data
        if self.weather_data:
            weather_time = self.weather_data.get("time")
            if weather_info_text:
                weather_info_text.insert(tk.END, f"Time: {weather_time}\n")
                

            temperature = self.weather_data.get("temperature")
            if temperature:
                weather_info_text.insert(tk.END, f"Temperature: {temperature}°C\n")

            windspeed = self.weather_data.get("windspeed")
            if windspeed:
                weather_info_text.insert(tk.END, f"Windspeed: {windspeed} m/s\n")

            winddirection = self.weather_data.get("winddirection")
            if winddirection:
                weather_info_text.insert(tk.END, f"Winddirection: {winddirection}°\n")
            
            # Retrieving information about weather it is day or night
            is_day = self.weather_data.get("is_day")
            if is_day is not None:
                weather_info_text.insert(tk.END, f"Daytime: {'Yes' if is_day else 'No'}\n")

            else: 
                weather_info_text.insert(tk.END, "Unidentified weather.\n")

            root.mainloop() # Starts tkinter loop to show window

# Function to get weather data when the button is clicked in the GUI, insert exact coordinates
def get_weather(latitude_entry, longitude_entry):
    latitude = latitude_entry.get()
    longitude = longitude_entry.get()
    weather_api = WeatherAPI(latitude, longitude)
    current_weather_data = weather_api.get_weather_data()
    weather_display = WeatherDisplay(current_weather_data, weather_api.city_name, latitude, longitude)
    weather_display.display_weather()

# Main function that creates the graphical user interface (GUI)     
def main():

    root = tk.Tk()
    root.title("Coordinates: ")

    # Creating label and input field for latitude 
    tk.Label(root, text="Latitude: ").pack()
    latitude_entry = tk.Entry(root)
    latitude_entry.pack()

    # Creating label and input field for longitude
    tk.Label(root, text="Longitude: ").pack()
    longitude_entry = tk.Entry(root)
    longitude_entry.pack()

    # Creating a button that get the weather when clicked
    get_weather_button = tk.Button(root, text="Get Weather", command=lambda: get_weather(latitude_entry, longitude_entry))
    get_weather_button.pack()

    root.mainloop() # Start tkinters main loop for the GUI

# If the script is run directly, call the main function 
if __name__ == "__main__":
    main()