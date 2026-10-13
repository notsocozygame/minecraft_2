import time

class GameEngine:
    def __init__(self, title="Custom Engine", target_fps=60):
        self.title = title
        self.target_fps = target_fps
        self.frame_duration = 1.0 / target_fps
        self.is_running = False

    def initialize(self):
        print(f"[*] Initializing '{self.title}'...")
        pass

    def update(self, dt):
        pass

    def render(self):
        pass

    def run(self):
        self.initialize()
        self.is_running = True
        print(f"[*] Engine running at {self.target_fps} FPS. Press Ctrl+C to stop.")
        
        last_time = time.time()
        
        try:
            while self.is_running:
                current_time = time.time()
                dt = current_time - last_time
                
                if dt < self.frame_duration:
                    time.sleep(self.frame_duration - dt)
                    dt = self.frame_duration
                
                last_time = current_time

                self.update(dt)
                self.render()
                
        except KeyboardInterrupt:
            print("\n[*] Engine shut down gracefully.")

if __name__ == "__main__":
    engine = GameEngine("My Custom Engine", target_fps=30)
    engine.run()
