"""Audio utilities for loading and playing sounds."""
from __future__ import annotations

import math
from array import array

import pygame

class SoundManager:
    def __init__(self) -> None:
        try:
            pygame.mixer.init()
            self.background = self._tone(440, 1000)
            self.munch = self._tone(880, 100)
            self.death = self._tone(220, 250)
            self.background.set_volume(0.1)
            self.munch.set_volume(0.3)
            self.death.set_volume(0.5)
            self.loaded = True
        except pygame.error:
            self.loaded = False

    def _tone(self, frequency: int, duration_ms: int) -> pygame.mixer.Sound:
        """Return a simple sine wave tone."""
        sample_rate = 44_100
        n_samples = int(sample_rate * duration_ms / 1000)
        amplitude = 32767
        buf = array("h", [0] * n_samples)
        for i in range(n_samples):
            t = i / sample_rate
            buf[i] = int(amplitude * math.sin(2 * math.pi * frequency * t))
        return pygame.mixer.Sound(buffer=buf)

    def play_music(self) -> None:
        if self.loaded:
            self.background.play(loops=-1)

    def play_munch(self) -> None:
        if self.loaded:
            self.munch.play()

    def play_death(self) -> None:
        if self.loaded:
            self.death.play()
