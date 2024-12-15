import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io  # Needed to handle the image data from the icon URL
from io import BytesIO  # Import BytesIO to handle image data from the URL


class WeatherData:
    def __init__(self, temperature, wind_speed, humidity, description, icon_url):
        """
        Initialize the weather data with temperature, wind speed, humidity, description, and an icon.
        """
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.humidity = humidity
        self.description = description
        self.icon_url = icon_url

class WeatherStation:
    API_KEY = "cdd1fb390294441ab9b102555241212"  # Replace with your actual WeatherAPI key

    @staticmethod
    def fetch_weather(city_name):
        """
        Fetch weather data for the given city using WeatherAPI.
        """
        base_url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "key": WeatherStation.API_KEY,
            "q": city_name,  # Pass city name directly
        }
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            current = data['current']
            icon_url = "https:" + current['condition']['icon']  # Weather icon URL

            # Create and return a WeatherData object
            return WeatherData(
                temperature=current['temp_c'],
                wind_speed=current['wind_kph'],
                humidity=current['humidity'],
                description=current['condition']['text'],
                icon_url=icon_url
            )
        else:
            raise Exception("Error fetching weather data: " + response.json().get('error', {}).get('message', 'Unknown error'))

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("800x600")  # Set window size
        
        # Fetch the background image from URL
        self.bg_url = "https://img.freepik.com/free-vector/flat-design-monsoon-season-clouds-illustration_23-2149424294.jpg?t=st=1734001792~exp=1734005392~hmac=b03589ca7341e081e88f49f23b8e58cd5a868fbd189eaaf62404c9c2bc90971a&w=826"
        response = requests.get(self.bg_url)
        img_data = response.content
        
        # Open the image
        self.bg_image = Image.open(BytesIO(img_data))  # Open the image from the URL
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to window size
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)  # Convert to Tkinter compatible format
        
        # Create a Canvas widget and add the background image
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # Add a label or other widgets on top of the background using create_window()
        self.title_label = tk.Label(self.root, text="Welcome to the Weather App", font=("Arial", 24), bg="white", fg="black")
        self.canvas.create_window(400, 120, window=self.title_label)  # Center the title
        
        # Add buttons (such as Check Weather and Weather Blog) using create_window()
        self.weather_button = tk.Button(self.root, text="Check Weather", font=("Arial", 16), command=self.open_weather_page)
        self.canvas.create_window(400, 250, window=self.weather_button)  # Center button

        self.blog_button = tk.Button(self.root, text="Weather Blog", font=("Arial", 16), command=self.open_blog_page)
        self.canvas.create_window(400, 350, window=self.blog_button)



    def open_weather_page(self):
        """
        Open the Check Weather page when the user clicks the button.
        """
        self.root.destroy()  # Close the Home Page
        root = tk.Tk()
        app = WeatherApp(root)
        root.mainloop()

    def open_blog_page(self):
        """
        Open the Weather Blog page when the user clicks the button.
        """
        self.root.destroy()  # Close the Home Page
        root = tk.Tk()
        app = WeatherBlog(root)
        root.mainloop()


class WeatherApp:
    def __init__(self, root):
        """
        Initialize the GUI with the main window and widgets for weather checking.
        """
        self.root = root
        self.root.title("Weather Monitoring System")
        self.root.geometry("800x600")  # Start with a larger size
        self.root.resizable(True, True)  # Allow window resizing

        # Fetch the background image from URL
        self.bg_url = "https://img.freepik.com/free-vector/flat-design-monsoon-season-clouds-illustration_23-2149424294.jpg?t=st=1734001792~exp=1734005392~hmac=b03589ca7341e081e88f49f23b8e58cd5a868fbd189eaaf62404c9c2bc90971a&w=826"
        response = requests.get(self.bg_url)
        img_data = response.content
        
        # Open the image
        self.bg_image = Image.open(BytesIO(img_data))  # Open the image from the URL
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to window size
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)  # Convert to Tkinter compatible format
        
        # Create a Canvas widget and add the background image
        self.canvas = tk.Canvas(self.root, width=800, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # City input label and entry field
        self.city_label = tk.Label(self.root, text="Enter City Name:", font=("Arial", 14), bg="white")
        self.canvas.create_window(400, 70, window=self.city_label)  # Position the label at the top center

        self.city_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.canvas.create_window(400, 120, window=self.city_entry)  # Position the entry field under the label

        # Fetch button
        self.fetch_button = tk.Button(self.root, text="Fetch Weather", font=("Arial", 14), command=self.fetch_weather)
        self.canvas.create_window(400, 170, window=self.fetch_button)  # Position the button under the entry

        # Weather icon label
        self.icon_label = tk.Label(self.root)
        self.canvas.create_window(400, 250, window=self.icon_label)  # Position the icon label under the button

        # Result label to display the weather data
        self.result_label = tk.Label(self.root, text="", font=("Arial", 16), wraplength=600, justify="left", bg="white")
        self.canvas.create_window(400, 400, window=self.result_label)  # Position the result label under the icon

        # Back to Home button
        self.back_button = tk.Button(self.root, text="Back to Home", font=("Arial", 14), command=self.back_to_home)
        self.canvas.create_window(400, 550, window=self.back_button)  # Position the back button at the bottom

    def fetch_weather(self):
        """
        Fetch the weather data for the entered city and display it in the result label.
        """
        city_name = self.city_entry.get().strip()
        if not city_name:
            messagebox.showerror("Error", "Please enter a city name!")
            return

        try:
            # Fetch weather data using WeatherStation (you would need to import or define this class)
            weather = WeatherStation.fetch_weather(city_name)
            result = (
                f"City: {city_name}\n\n"
                f"Temperature: {weather.temperature}°C\n"
                f"Wind Speed: {weather.wind_speed} km/h\n"
                f"Humidity: {weather.humidity}%\n"
                f"Description: {weather.description}"
            )
            self.result_label.config(text=result)  # Display the weather data in the label

            # Fetch the weather icon
            self.display_weather_icon(weather.icon_url)

        except Exception as e:
            # Show error if there is an issue with fetching weather data
            messagebox.showerror("Error", str(e))

    def display_weather_icon(self, icon_url):
        """
        Fetch the weather icon from the given URL and display it in the GUI.
        """
        try:
            # Fetch the image from the URL
            img_response = requests.get(icon_url)
            img_data = img_response.content

            # Open the image and display it in Tkinter
            img = Image.open(BytesIO(img_data))
            img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Resize to fit in the window
            img = ImageTk.PhotoImage(img)

            self.icon_label.config(image=img)
            self.icon_label.image = img  # Keep a reference to the image

        except Exception as e:
            print(f"Error fetching weather icon: {e}")

    def back_to_home(self):
        """
        Return to the Home Page when the user clicks the button.
        """
        self.root.destroy()  # Close the Weather App Page
        root = tk.Tk()
        app = HomePage(root)  # Open HomePage
        root.mainloop()

    


class Blog:
    def __init__(self, title, content):
        """
        Blog class that holds the title and content for a weather safety blog.
        """
        self.title = title
        self.content = content

class WeatherBlog:
    def __init__(self, root):
        """
        Initialize the Weather Blog Page to show a list of weather safety blogs.
        """
        self.root = root
        self.root.title("Weather Safety Blogs")
        self.root.geometry("600x400")  # Set a suitable window size
        self.root.resizable(True, True)

        # Fetch the background image from URL
        self.bg_url = "https://img.freepik.com/free-vector/flat-design-monsoon-season-clouds-illustration_23-2149424294.jpg?t=st=1734001792~exp=1734005392~hmac=b03589ca7341e081e88f49f23b8e58cd5a868fbd189eaaf62404c9c2bc90971a&w=826"
        response = requests.get(self.bg_url)
        img_data = response.content

        # Open and resize the image
        self.bg_image = Image.open(BytesIO(img_data))
        self.bg_image = self.bg_image.resize((600, 400), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a Canvas widget and add the background image
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Title label
        self.title_label = tk.Label(self.root, text="Weather Safety Blogs", font=("Arial", 18), bg="white")
        self.canvas.create_window(300, 30, window=self.title_label)

        # Sample blogs (List of Blog objects)
        self.blogs = [
            Blog("How to Stay Safe During a Thunderstorm", """
Thunderstorms are one of nature's most powerful weather events, capable of causing significant damage. It’s essential to know how to protect yourself when thunderstorms strike.

First, stay indoors! Avoid taking showers, using electrical appliances, or touching metal objects, as lightning can travel through plumbing and wiring. Keep away from windows and doors, and stay in a basement or interior room if possible.

If you are caught outside, find shelter immediately and avoid taking shelter under trees, as they are prone to lightning strikes.

Always have a battery-powered weather radio or app to stay updated on the storm’s progress.
"""),
            Blog("Preparing for Cyclones: A Complete Guide", """
Cyclones, or hurricanes, are powerful tropical storms that can cause extensive damage to infrastructure, the environment, and even lead to loss of life. It’s crucial to be well-prepared for the arrival of a cyclone.

First, know your evacuation routes and make arrangements to stay with friends, family, or at a safe shelter if necessary. Stock up on emergency supplies such as food, water, medicines, flashlights, and batteries. Secure windows, doors, and roofs to minimize damage. Make sure you have a plan for your pets and other animals. Always heed evacuation warnings and never underestimate the power of a cyclone.
"""),
            Blog("Flood Safety Tips", """
Flooding is one of the most common natural disasters, and it can happen quickly, especially after heavy rain or snowmelt. The key to flood safety is preparation.

Keep important documents in a waterproof container, and know if you live in a flood-prone area. If flooding occurs, avoid walking or driving through floodwaters, as just a few inches can be deadly.

Move to higher ground as soon as possible, and always follow evacuation orders if issued. Stay away from electrical outlets and appliances if you’re in a flooded area, and avoid using electrical devices in wet conditions. Once the floodwater recedes, wait for authorities to confirm it’s safe before returning home.
"""),
            Blog("Protecting Yourself During Extreme Heat", """
Extreme heat can be dangerous, especially for children, the elderly, and those with health conditions.

To stay safe during heat waves, make sure to stay hydrated and avoid outdoor activities during peak sun hours, typically from 10 a.m. to 4 p.m. Wear loose, light-colored clothing and apply sunscreen with a high SPF.

If you must be outdoors, take regular breaks in the shade or air-conditioned areas. If you notice signs of heat exhaustion, such as heavy sweating, weakness, or dizziness, move to a cooler place and drink water. Extreme heat can be a silent killer, so always stay vigilant and prepared.
"""),
            Blog("Winter Storm Safety: What You Need to Know", """
Winter storms can bring a wide range of hazards, from heavy snow and ice to extreme cold.

The most important step in preparing for a winter storm is ensuring your home is insulated and that heating systems are in working order. Keep extra blankets, warm clothing, and batteries for flashlights and radios. If you need to travel, make sure your car is winter-ready with antifreeze, warm clothing, and non-perishable food and water. Never leave your car running in a garage, and avoid driving during a storm unless absolutely necessary.
"""),
        ]

        # Display the blogs in a Listbox
        self.blog_listbox = tk.Listbox(self.root, font=("Arial", 14), width=40, height=10)
        for blog in self.blogs:
            self.blog_listbox.insert(tk.END, blog.title)
        self.canvas.create_window(300, 200, window=self.blog_listbox)

        # Button to go back to Home Page
        self.back_button = tk.Button(self.root, text="Back to Home", font=("Arial", 14), command=self.back_to_home)
        self.canvas.create_window(300, 350, window=self.back_button)

        # Bind the click event to open blog details
        self.blog_listbox.bind("<ButtonRelease-1>", self.show_blog_content)

    def show_blog_content(self, event):
        """
        Show the detailed content of the selected blog.
        """
        selected_index = self.blog_listbox.curselection()[0]
        selected_blog = self.blogs[selected_index]

        # Open a new window to display the content of the selected blog
        blog_window = tk.Toplevel(self.root)
        blog_window.title(selected_blog.title)
        blog_window.geometry("500x400")
        blog_window.resizable(True, True)

        # Fetch the background image again for the blog details page
        response = requests.get(self.bg_url)
        img_data = response.content
        bg_image = Image.open(BytesIO(img_data)).resize((500, 400), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a canvas for the blog details page
        blog_canvas = tk.Canvas(blog_window, width=500, height=400)
        blog_canvas.pack(fill="both", expand=True)
        blog_canvas.create_image(0, 0, image=bg_photo, anchor="nw")

        # Keep a reference to avoid garbage collection of the image
        blog_window.bg_photo = bg_photo

        # Display the blog content
        content_label = tk.Label(blog_window, text=selected_blog.content, font=("Arial", 12), wraplength=450, justify="left", bg="white")
        blog_canvas.create_window(250, 150, window=content_label)

        # Button to close the blog window
        close_button = tk.Button(blog_window, text="Close", font=("Arial", 14), command=blog_window.destroy)
        blog_canvas.create_window(250, 350, window=close_button)

    def back_to_home(self):
        """
        Return to the Home Page when the user clicks the button.
        """
        self.root.destroy()  # Close the Weather Blog Page
        root = tk.Tk()
        app = HomePage(root)
        root.mainloop()
# Main function to run the app
if __name__ == "__main__":
    # Create the Tkinter window (root)
    root = tk.Tk()
    app = HomePage(root)  # Open HomePage first
    root.mainloop()  # Start the Tkinter main loop
