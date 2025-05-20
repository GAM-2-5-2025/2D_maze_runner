import pygame


class Camera:
    def __init__(self, scale):
        self.scale = scale

    def apply(self, klasa):
        """Converts imaginary position/rect/... to real screen version"""
        if isinstance(klasa, (int, float)):
            return klasa * self.scale
        
        elif isinstance(klasa, pygame.Rect):
            return pygame.Rect(
                klasa.x * self.scale,
                klasa.y * self.scale,
                klasa.width * self.scale,
                klasa.height * self.scale
            )
        
        elif isinstance(klasa, (tuple, list)):
            return type(klasa)(self.apply(i) for i in klasa)
        
        elif isinstance(klasa, dict):
            return {k: self.apply(v) for k,v in klasa.items()}

        elif isinstance(klasa, pygame.Vector2):
            return klasa * self.scale
        
        else:
            raise TypeError("Unsupported type for camera.apply")

    def unscale(self, klasa):
        """Converts from real screen space to imaginary (miš i to)"""
        if isinstance(klasa, (int, float)):
            return type(klasa)(klasa / self.scale)
        
        elif isinstance(klasa, pygame.Rect):
            return pygame.Rect(
                klasa.x / self.scale,
                klasa.y / self.scale,
                klasa.width / self.scale,
                klasa.height / self.scale
            )
        
        elif isinstance(klasa, (tuple, list)):
            return type(klasa)(self.unscale(i) for i in klasa)
        
        elif isinstance(klasa, dict):
            return {k: self.unscale(v) for k,v in klasa.items()}
        
        elif isinstance(klasa, pygame.Vector2):
            return klasa / self.scale
        
        else:
            raise TypeError("Unsupported type for camera.unscale")

    def applyFont(self, font_path, font_size):
        
        return pygame.font.Font(font_path, int(font_size * self.scale))
