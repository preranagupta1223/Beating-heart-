import turtle
import math
import tkinter as tk
from tkinter import ttk
import random

# Heart equation: y = |x|^(2/3) + 0.9*sin(kx)*sqrt(3-x^2)
class HeartAnimation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("❤️ Interactive Heart Equation Visualizer")
        self.root.configure(bg='#0a0a0a')
        self.root.geometry("920x900")
        
        # Header frame
        header_frame = tk.Frame(self.root, bg='#0a0a0a')
        header_frame.pack(pady=15)
        
        # Title with emoji
        title = tk.Label(header_frame, text="💕 Heart Equation Animator 💕", 
                        font=("Arial", 36, "bold"), 
                        fg="#FF1493", bg="#0a0a0a")
        title.pack()
        
        # Create canvas for turtle
        self.canvas = tk.Canvas(self.root, width=860, height=550, bg='#0a0a0a', highlightthickness=2, highlightbackground="#FF1493")
        self.canvas.pack(pady=10)
        
        # Setup turtle
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("#0a0a0a")
        self.pen = turtle.RawTurtle(self.screen)
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.width(3)
        
        # Multiple pens for glow effect
        self.glow_pens = []
        for i in range(3):
            glow_pen = turtle.RawTurtle(self.screen)
            glow_pen.hideturtle()
            glow_pen.speed(0)
            glow_pen.width(8 - i*2)
            self.glow_pens.append(glow_pen)
        
        # Color variables
        self.colors = ["#FF1493", "#FF69B4", "#FF0066", "#FF33CC", "#CC0099", "#FF1493"]
        self.current_color_index = 0
        self.rainbow_mode = False
        self.glow_enabled = True
        
        # Equation label with better styling
        eq_frame = tk.Frame(self.root, bg='#1a1a1a', relief=tk.RIDGE, bd=2)
        eq_frame.pack(pady=10, padx=20, fill=tk.X)
        
        eq_text = "y = |x|^(2/3) + 0.9·sin(kx)√(3-x²)"
        eq_label = tk.Label(eq_frame, text=eq_text, 
                           font=("Courier", 18, "bold"), 
                           fg="#00FFFF", bg="#1a1a1a")
        eq_label.pack(pady=8)
        
        # K value display
        self.k_value = 20.75
        k_frame = tk.Frame(self.root, bg='#0a0a0a')
        k_frame.pack(pady=5)
        
        self.k_label = tk.Label(k_frame, text=f"k = {self.k_value:.2f}", 
                               font=("Arial", 24, "bold"), 
                               fg="#00FF00", bg="#0a0a0a")
        self.k_label.pack()
        
        # Control panel
        control_panel = tk.Frame(self.root, bg='#1a1a1a', relief=tk.RAISED, bd=3)
        control_panel.pack(pady=10, padx=20, fill=tk.X)
        
        # Buttons frame
        btn_frame = tk.Frame(control_panel, bg='#1a1a1a')
        btn_frame.pack(pady=15)
        
        # Styled buttons
        button_style = {
            'font': ("Arial", 14, "bold"),
            'bg': "#FF1493",
            'fg': "white",
            'width': 12,
            'height': 1,
            'relief': tk.RAISED,
            'bd': 3,
            'activebackground': "#FF69B4",
            'cursor': 'hand2'
        }
        
        # Play button
        self.play_btn = tk.Button(btn_frame, text="▶ Play", 
                                   command=self.play_animation,
                                   **button_style)
        self.play_btn.grid(row=0, column=0, padx=8)
        
        # Reset button
        self.reset_btn = tk.Button(btn_frame, text="↺ Reset", 
                                    command=self.reset,
                                    bg="#FF6600",
                                    activebackground="#FF8833",
                                    font=("Arial", 14, "bold"),
                                    fg="white",
                                    width=12,
                                    height=1,
                                    relief=tk.RAISED,
                                    bd=3,
                                    cursor='hand2')
        self.reset_btn.grid(row=0, column=1, padx=8)
        
        # Rainbow mode button
        self.rainbow_btn = tk.Button(btn_frame, text="🌈 Rainbow", 
                                      command=self.toggle_rainbow,
                                      bg="#9933FF",
                                      activebackground="#AA55FF",
                                      font=("Arial", 14, "bold"),
                                      fg="white",
                                      width=12,
                                      height=1,
                                      relief=tk.RAISED,
                                      bd=3,
                                      cursor='hand2')
        self.rainbow_btn.grid(row=0, column=2, padx=8)
        
        # Glow toggle button
        self.glow_btn = tk.Button(btn_frame, text="✨ Glow ON", 
                                   command=self.toggle_glow,
                                   bg="#00CCFF",
                                   activebackground="#33DDFF",
                                   font=("Arial", 14, "bold"),
                                   fg="white",
                                   width=12,
                                   height=1,
                                   relief=tk.RAISED,
                                   bd=3,
                                   cursor='hand2')
        self.glow_btn.grid(row=0, column=3, padx=8)
        
        # Slider frame
        slider_frame = tk.Frame(control_panel, bg='#1a1a1a')
        slider_frame.pack(pady=15, padx=20)
        
        # Manual control label
        control_label = tk.Label(slider_frame, text="🎚️ Manual Control (k value):", 
                                font=("Arial", 14, "bold"), 
                                fg="#FFD700", bg="#1a1a1a")
        control_label.pack(pady=8)
        
        # Styled slider
        self.slider = tk.Scale(slider_frame, from_=1, to=50, 
                              orient=tk.HORIZONTAL,
                              command=self.update_k,
                              bg="#1a1a1a", 
                              fg="white",
                              highlightthickness=0,
                              length=700,
                              troughcolor="#FF1493",
                              sliderrelief=tk.RAISED,
                              font=("Arial", 11),
                              resolution=0.25)
        self.slider.set(20.75)
        self.slider.pack(pady=5)
        
        # Speed control
        speed_frame = tk.Frame(control_panel, bg='#1a1a1a')
        speed_frame.pack(pady=10)
        
        speed_label = tk.Label(speed_frame, text="⚡ Animation Speed:", 
                              font=("Arial", 12, "bold"), 
                              fg="#FFFF00", bg="#1a1a1a")
        speed_label.pack(side=tk.LEFT, padx=10)
        
        self.speed_var = tk.IntVar(value=5)
        speed_slider = tk.Scale(speed_frame, from_=1, to=20, 
                               orient=tk.HORIZONTAL,
                               variable=self.speed_var,
                               bg="#1a1a1a", 
                               fg="white",
                               highlightthickness=0,
                               length=300,
                               troughcolor="#00FF00")
        speed_slider.pack(side=tk.LEFT, padx=10)
        
        self.is_playing = False
        self.current_step = 0
        
        # Draw initial heart
        self.draw_heart(self.k_value)
        
    def heart_equation(self, x, k):
        """Calculate y value for heart equation"""
        try:
            if 3 - x**2 < 0:
                return None
            y = abs(x)**(2/3) + 0.9 * math.sin(k * x) * math.sqrt(3 - x**2)
            return y
        except:
            return None
    
    def get_rainbow_color(self, step, max_steps):
        """Generate rainbow colors"""
        hue = (step / max_steps) * 360
        # Convert HSV to RGB (simplified)
        c = 1
        x = c * (1 - abs((hue / 60) % 2 - 1))
        m = 0
        
        if hue < 60:
            r, g, b = c, x, 0
        elif hue < 120:
            r, g, b = x, c, 0
        elif hue < 180:
            r, g, b = 0, c, x
        elif hue < 240:
            r, g, b = 0, x, c
        elif hue < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    def draw_heart(self, k, steps=300):
        """Draw the heart with given k value"""
        self.pen.clear()
        for glow_pen in self.glow_pens:
            glow_pen.clear()
        
        self.pen.penup()
        
        # Collect points
        x_values = []
        y_values = []
        
        for i in range(steps + 1):
            x = -1.8 + (3.6 * i / steps)
            y = self.heart_equation(x, k)
            if y is not None:
                x_values.append(x * 100)
                y_values.append(y * 100)
        
        if not x_values:
            return
        
        # Draw glow effect
        if self.glow_enabled:
            for idx, glow_pen in enumerate(self.glow_pens):
                glow_pen.penup()
                glow_pen.goto(x_values[0], y_values[0])
                glow_pen.pendown()
                
                # Set glow color (lighter than main)
                if self.rainbow_mode:
                    glow_pen.color("#FF1493")
                else:
                    alpha = 0.3 + idx * 0.2
                    glow_pen.color(self.colors[self.current_color_index])
                
                for i in range(1, len(x_values)):
                    glow_pen.goto(x_values[i], y_values[i])
                glow_pen.penup()
        
        # Draw main heart
        self.pen.goto(x_values[0], y_values[0])
        self.pen.pendown()
        
        if self.rainbow_mode:
            for i in range(1, len(x_values)):
                color = self.get_rainbow_color(i, len(x_values))
                self.pen.color(color)
                self.pen.goto(x_values[i], y_values[i])
        else:
            self.pen.color(self.colors[self.current_color_index])
            for i in range(1, len(x_values)):
                self.pen.goto(x_values[i], y_values[i])
        
        self.pen.penup()
    
    def play_animation(self):
        """Animate the heart drawing"""
        self.is_playing = True
        self.play_btn.config(text="⏸ Playing...", state=tk.DISABLED)
        self.animate_step(0)
    
    def animate_step(self, step):
        """Draw one step of the animation"""
        max_steps = 300
        
        if not self.is_playing or step > max_steps:
            self.is_playing = False
            self.play_btn.config(text="▶ Play", state=tk.NORMAL)
            self.draw_heart(self.k_value)
            return
        
        self.pen.clear()
        for glow_pen in self.glow_pens:
            glow_pen.clear()
        
        self.pen.penup()
        
        k = self.k_value
        
        # Collect points for this step
        points = []
        for i in range(step + 1):
            x = -1.8 + (3.6 * i / max_steps)
            y = self.heart_equation(x, k)
            if y is not None:
                points.append((x * 100, y * 100))
        
        if not points:
            self.root.after(10, lambda: self.animate_step(step + 1))
            return
        
        # Draw glow
        if self.glow_enabled:
            for glow_pen in self.glow_pens:
                glow_pen.penup()
                glow_pen.goto(points[0][0], points[0][1])
                glow_pen.pendown()
                glow_pen.color("#FF1493")
                for point in points[1:]:
                    glow_pen.goto(point[0], point[1])
                glow_pen.penup()
        
        # Draw main line
        self.pen.goto(points[0][0], points[0][1])
        self.pen.pendown()
        
        for i, point in enumerate(points[1:]):
            if self.rainbow_mode:
                color = self.get_rainbow_color(i, len(points))
                self.pen.color(color)
            else:
                self.pen.color(self.colors[self.current_color_index])
            self.pen.goto(point[0], point[1])
        
        self.pen.penup()
        
        # Schedule next step with variable speed
        delay = max(1, 25 - self.speed_var.get())
        self.root.after(delay, lambda: self.animate_step(step + 1))
    
    def reset(self):
        """Reset the animation"""
        self.is_playing = False
        self.pen.clear()
        for glow_pen in self.glow_pens:
            glow_pen.clear()
        self.play_btn.config(text="▶ Play", state=tk.NORMAL)
        self.draw_heart(self.k_value)
    
    def toggle_rainbow(self):
        """Toggle rainbow mode"""
        self.rainbow_mode = not self.rainbow_mode
        if self.rainbow_mode:
            self.rainbow_btn.config(text="🌈 Rainbow ON", bg="#00FF00")
        else:
            self.rainbow_btn.config(text="🌈 Rainbow OFF", bg="#9933FF")
        self.draw_heart(self.k_value)
    
    def toggle_glow(self):
        """Toggle glow effect"""
        self.glow_enabled = not self.glow_enabled
        if self.glow_enabled:
            self.glow_btn.config(text="✨ Glow ON", bg="#00CCFF")
        else:
            self.glow_btn.config(text="✨ Glow OFF", bg="#666666")
        self.draw_heart(self.k_value)
    
    def update_k(self, value):
        """Update k value from slider"""
        self.k_value = float(value)
        self.k_label.config(text=f"k = {self.k_value:.2f}")
        if not self.is_playing:
            self.draw_heart(self.k_value)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = HeartAnimation()
    app.run()