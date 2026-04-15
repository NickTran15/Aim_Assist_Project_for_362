class ParticleSystem:
    """Manages all active particles."""

    def __init__(self):
        self._particles = []   # Create list to store all current particles

    def emit(self, x, y, color=(255, 200, 50), count=12):
        # Creating multiple particles in the current position 
        for _ in range(count):
            self._particles.append(Particle(x, y, color))   # Using 'particle' object

    def update(self):
        # Updating every particle 
        for p in self._particles:
            p.update()
        
        # Filter out dead particles after they've had a chance to update
        self._particles = [p for p in self._particles if p.is_alive()]

    def draw(self, screen):
        # Drawing all active particles on screen
        for p in self._particles:
            p.draw(screen)
