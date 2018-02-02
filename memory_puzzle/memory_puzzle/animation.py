"""Module for handling animation."""

from . import settings


class AnimationStatus(object):
    def __init__(self, starting_coverage=0):
        self._coverage = starting_coverage
        self._animation_rate = 0
        self._being_animated = False
        self._will_reverse = False

    @property
    def coverage(self):
        return self._coverage

    @property
    def animation_rate(self):
        return self._animation_rate

    @property
    def being_animated(self):
        return self._being_animated

    def start_animation(self, animation_rate, will_reverse=False):
        self._animation_rate = animation_rate
        self._being_animated = True
        self._will_reverse = will_reverse

    def tick_animation(self):
        self._coverage += self._animation_rate
        self._bring_coverage_within_box_bounds()
        if (self._coverage == settings.BOX_SIZE) or (self._coverage == 0):
            self._handle_animation_reaching_border()

    def _bring_coverage_within_box_bounds(self):
        if self._coverage > settings.BOX_SIZE:
            self._coverage = settings.BOX_SIZE
        elif self._coverage < 0:
            self._coverage = 0

    def _handle_animation_reaching_border(self):
        if self._will_reverse:
            self._animation_rate = -self._animation_rate
            self._will_reverse = False
        else:
            self._being_animated = False
