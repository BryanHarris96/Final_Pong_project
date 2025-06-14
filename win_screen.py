import pygame
import random

class WinScreen:
    def __init__(self, screen, winner, particle_count=100):
        self.screen    = screen
        self.w, self.h = screen.get_size()
        self.winner    = winner
        self.font      = pygame.font.Font(None, 72)

        self.particles = []
        for _ in range(particle_count):
            x  = random.uniform(0, self.w)
            y  = random.uniform(-self.h*0.5, 0)
            vx = random.uniform(-2, 2)
            vy = random.uniform(1, 5)
            color = (
                random.randint(50,255),
                random.randint(50,255),
                random.randint(50,255)
            )
            self.particles.append([x, y, vx, vy, color])

    def draw(self):
        self.screen.fill((0,0,0))
        for p in self.particles:
            x, y, vx, vy, color = p
            p[0] += vx; p[1] += vy
            if p[1] > self.h:
                p[0] = random.uniform(0, self.w)
                p[1] = random.uniform(-self.h*0.2, 0)
                p[2] = random.uniform(-2, 2)
                p[3] = random.uniform(1, 5)
            pygame.draw.rect(self.screen, color, (int(p[0]), int(p[1]), 5, 5))

        text = f"{self.winner} wins the match!"
        surf = self.font.render(text, True, (255,255,255))
        rect = surf.get_rect(center=(self.w//2, self.h//2))
        self.screen.blit(surf, rect)
