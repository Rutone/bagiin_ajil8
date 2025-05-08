import time
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk  # For displaying images

class LightControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Хөдөлгөөнөөр асдаг автомат гэрэл")
        self.light_on = False
        self.last_motion_time = None
        self.timeout = 15  # Default timeout in seconds

        # Load house plan image
        self.house_image = Image.open("zurag2.png")  # Replace with your house plan image file
        self.house_image = self.house_image.resize((802, 612), Image.Resampling.LANCZOS)
        self.house_photo = ImageTk.PhotoImage(self.house_image)

        # Create UI elements
        self.canvas = tk.Canvas(root, width=500, height=400)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.house_photo)

        # Add a light indicator (circle) to the canvas
        self.light_indicator = self.canvas.create_oval(200, 200, 250, 250, fill="gray", outline="gray")

        self.status_label = tk.Label(root, text="[УНТРААЛТТАЙ] Хөдөлгөөн илрээгүй...", font=("Arial", 16))
        self.status_label.pack(pady=10)

        self.countdown_label = tk.Label(root, text="", font=("Arial", 14))
        self.countdown_label.pack(pady=5)

        # Add buttons for manual control
        self.manual_on_button = tk.Button(root, text="Гэрэл асаах", command=self.turn_on_light, font=("Arial", 14))
        self.manual_on_button.pack(pady=5)

        self.manual_off_button = tk.Button(root, text="Гэрэл унтраах", command=self.turn_off_light, font=("Arial", 14))
        self.manual_off_button.pack(pady=5)

        # Add input field to change timeout duration
        self.timeout_label = tk.Label(root, text="Гэрэл унтрах хугацаа (сек):", font=("Arial", 14))
        self.timeout_label.pack(pady=5)

        self.timeout_entry = tk.Entry(root, font=("Arial", 14))
        self.timeout_entry.pack(pady=5)
        self.timeout_entry.insert(0, str(self.timeout))  # Set default timeout value

        self.set_timeout_button = tk.Button(root, text="Хугацааг тохируулах", command=self.set_timeout, font=("Arial", 14))
        self.set_timeout_button.pack(pady=5)

        self.motion_button = tk.Button(root, text="Хөдөлгөөн", command=self.simulate_motion, font=("Arial", 14))
        self.motion_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Гарах", command=self.exit_program, font=("Arial", 14))
        self.exit_button.pack(pady=5)

        # Start the update loop in a separate thread
        self.running = True
        self.update_thread = Thread(target=self.update_loop)
        self.update_thread.start()

    def simulate_motion(self):
        if not self.light_on:
            self.light_on = True
            self.status_label.config(text="[АСААЛТТАЙ] Хөдөлгөөн илэрлээ! Гэрэл аслаа.")
            self.canvas.itemconfig(self.light_indicator, fill="green", outline="green")  # Turn on the light
        self.last_motion_time = time.time()

    def turn_on_light(self):
        self.light_on = True
        self.status_label.config(text="[АСААЛТТАЙ] Гэрэл гар удирдлагаар аслаа.")
        self.canvas.itemconfig(self.light_indicator, fill="green", outline="green")  # Turn on the light
        self.last_motion_time = None  # Disable auto-off temporarily

    def turn_off_light(self):
        self.light_on = False
        self.status_label.config(text="[УНТРААЛТТАЙ] Гэрэл гар удирдлагаар унтарлаа.")
        self.canvas.itemconfig(self.light_indicator, fill="gray", outline="gray")  # Turn off the light
        self.last_motion_time = None  # Disable auto-off temporarily

    def set_timeout(self):
        try:
            new_timeout = int(self.timeout_entry.get())
            if new_timeout > 0:
                self.timeout = new_timeout
                self.status_label.config(text=f"[ТОХИРУУЛСАН] Гэрэл унтрах хугацаа {self.timeout} секунд.")
            else:
                self.status_label.config(text="[АЛДАА] Хугацаа 0-ээс их байх ёстой!")
        except ValueError:
            self.status_label.config(text="[АЛДАА] Зөвхөн тоо оруулна уу!")

    def exit_program(self):
        self.running = False
        self.root.destroy()

    def update_loop(self):
        while self.running:
            if self.light_on and self.last_motion_time:
                elapsed_time = time.time() - self.last_motion_time
                remaining_time = self.timeout - int(elapsed_time)
                if remaining_time > 0:
                    self.countdown_label.config(text=f"Гэрэл унтрахад {remaining_time} секунд...")
                if elapsed_time > self.timeout:
                    self.light_on = False
                    self.last_motion_time = None
                    self.status_label.config(text="[УНТРААЛТТАЙ] Хөдөлгөөн илэрсэнгүй. Гэрэл унтарлаа.")
                    self.countdown_label.config(text="")
                    self.canvas.itemconfig(self.light_indicator, fill="gray", outline="gray")  # Turn off the light
            time.sleep(0.1)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LightControlApp(root)
    root.mainloop()