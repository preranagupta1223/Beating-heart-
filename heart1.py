import turtle
import math
import tkinter as tk
import time

class BeatingHeart:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💗  Beating Heart Animation")
        self.root.configure(bg='#000000')
        self.root.geometry("900x800")
        
        # Title
        title = tk.Label(self.root, text="💗 MUMMY PAPA 💗", 
                        font=("Arial", 40, "bold"), 
                        fg="#FF0066", bg="#000000")
        title.pack(pady=15)
        
        # Canvas
        self.canvas = tk.Canvas(self.root, width=850, height=440, bg='#000000', highlightthickness=3, highlightbackground="#FF0066")
        self.canvas.pack(pady=10)
        
        # Setup turtle
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("#000000")
        self.screen.tracer(0)  # Turn off auto-update for smooth animation
        
        # Create multiple heart turtles for expanding pulse effect
        self.hearts = []
        for i in range(5):
            heart = turtle.RawTurtle(self.screen)
            heart.hideturtle()
            heart.speed(0)
            heart.width(3)
            self.hearts.append({
                'turtle': heart,
                'scale': 1.0,
                'opacity': 1.0,
                'active': False
            })
        
        # Animation variables
        self.beat_time = 0
        self.is_beating = True
        self.beat_interval = 0  # Counter for beat timing
        
        # Control panel
        control_frame = tk.Frame(self.root, bg='#1a1a1a', relief=tk.RAISED, bd=3)
        control_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Buttons
        btn_frame = tk.Frame(control_frame, bg='#1a1a1a')
        btn_frame.pack(pady=15)
        
        self.beat_btn = tk.Button(btn_frame, text="💓 Stop Beating", 
                                   command=self.toggle_beat,
                                   font=("Arial", 16, "bold"),
                                   bg="#FF0066", fg="white",
                                   width=15, height=1, bd=3,
                                   cursor='hand2')
        self.beat_btn.pack(side=tk.LEFT, padx=10)
        
        # Speed control
        speed_frame = tk.Frame(control_frame, bg='#1a1a1a')
        speed_frame.pack(pady=10)
        
        speed_label = tk.Label(speed_frame, text="💗 Heart Rate (BPM):", 
                              font=("Arial", 14, "bold"), 
                              fg="#FF69B4", bg="#1a1a1a")
        speed_label.pack(side=tk.LEFT, padx=10)
        
        self.bpm_var = tk.IntVar(value=72)
        self.bpm_slider = tk.Scale(speed_frame, from_=40, to=150, 
                                   orient=tk.HORIZONTAL,
                                   variable=self.bpm_var,
                                   bg="#1a1a1a", fg="white",
                                   length=500, troughcolor="#FF0066",
                                   font=("Arial", 11))
        self.bpm_slider.pack(side=tk.LEFT, padx=10)
        
        bpm_display = tk.Label(speed_frame, textvariable=self.bpm_var,
                              font=("Arial", 16, "bold"),
                              fg="#00FF00", bg="#1a1a1a",
                              width=4)
        bpm_display.pack(side=tk.LEFT, padx=5)
        
        # Info label
        info = tk.Label(control_frame, text="Watch the heart beat with expanding pulse waves! 💓", 
                       font=("Arial", 12, "italic"), 
                       fg="#FFB6C1", bg="#1a1a1a")
        info.pack(pady=10)
        
        # Start animation
        self.animate()
    
    def heart_parametric(self, t, scale=1.0):
        """Parametric heart equation"""
        x = 16 * math.sin(t)**3 * scale
        y = (13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)) * scale
        return x * 4, y * 4
    
    def draw_heart(self, heart_obj, scale, color, width):
        """Draw a single heart at given scale"""
        turtle_obj = heart_obj['turtle']
        turtle_obj.clear()
        turtle_obj.width(width)
        turtle_obj.color(color)
        turtle_obj.penup()
        
        # Draw heart
        steps = 100
        first = True
        for i in range(steps + 1):
            t = (i / steps) * 2 * math.pi
            x, y = self.heart_parametric(t, scale)
            
            if first:
                turtle_obj.goto(x, y)
                turtle_obj.pendown()
                first = False
            else:
                turtle_obj.goto(x, y)
        
        turtle_obj.penup()
    
    def get_pulse_color(self, opacity):
        """Get color based on opacity"""
        # Fade from bright pink to dark
        r = int(255 * opacity)
        g = int(20 * opacity)
        b = int(102 * opacity)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def animate(self):
        """Main animation loop"""
        if not self.is_beating:
            self.root.after(50, self.animate)
            return
        
        # Calculate beat timing based on BPM
        bpm = self.bpm_var.get()
        beat_duration = 60.0 / bpm  # seconds per beat
        frames_per_beat = int(beat_duration * 20)  # 20 fps
        
        self.beat_interval += 1
        
        # REAL HEARTBEAT PATTERN: lub-DUB (two beats)
        beat_phase = (self.beat_interval % frames_per_beat) / frames_per_beat
        
        # Main heart beating (lub-DUB pattern)
        if beat_phase < 0.15:  # First beat (lub)
            scale = 1.0 + (math.sin(beat_phase * math.pi / 0.15) * 0.3)
        elif beat_phase < 0.25:  # Brief pause
            scale = 1.0
        elif beat_phase < 0.35:  # Second beat (DUB) - stronger
            scale = 1.0 + (math.sin((beat_phase - 0.25) * math.pi / 0.1) * 0.4)
        else:  # Relaxation
            scale = 1.0
        
        # Draw main heart with pulsing
        main_color = self.get_pulse_color(1.0)
        self.draw_heart(self.hearts[0], scale, main_color, 4)
        
        # Expanding pulse waves (triggered at each beat)
        if beat_phase < 0.02 or (0.25 < beat_phase < 0.27):  # Trigger new wave
            # Find inactive heart for new wave
            for heart in self.hearts[1:]:
                if not heart['active']:
                    heart['active'] = True
                    heart['scale'] = scale
                    heart['opacity'] = 1.0
                    break
        
        # Update and draw expanding waves
        for i, heart in enumerate(self.hearts[1:]):
            if heart['active']:
                # Expand
                heart['scale'] += 0.04
                heart['opacity'] -= 0.02
                
                # Deactivate if too faded
                if heart['opacity'] <= 0:
                    heart['active'] = False
                    heart['turtle'].clear()
                else:
                    # Draw expanding heart
                    color = self.get_pulse_color(heart['opacity'])
                    width = max(1, int(4 * heart['opacity']))
                    self.draw_heart(heart, heart['scale'], color, width)
        
        # Update screen
        self.screen.update()
        
        # Schedule next frame (20 fps)
        self.root.after(50, self.animate)
    
    def toggle_beat(self):
        """Toggle heartbeat"""
        self.is_beating = not self.is_beating
        if self.is_beating:
            self.beat_btn.config(text="💓 Stop Beating", bg="#FF0066")
        else:
            self.beat_btn.config(text="💔 Start Beating", bg="#666666")
            # Clear all expanding waves
            for heart in self.hearts[1:]:
                heart['active'] = False
                heart['turtle'].clear()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = BeatingHeart()
    app.run()