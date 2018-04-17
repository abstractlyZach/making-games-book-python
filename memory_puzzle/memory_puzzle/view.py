import logging
import math
import random

import pygame

from . import animation
from . import coords
from . import constants
from . import events
from . import settings

# size of groups to reveal for hints
REVEAL_GROUPS = 10


class GraphicalView(object):
    """Draws the model's state to the screen."""
    def __init__(self, event_manager, model):
        self._event_manager = event_manager
        event_manager.register_listener(self)
        self._model = model
        self._animation_statuses = animation.AnimationStatusTracker()
        self._is_initialized = False
        self._display_surface = None
        self._clicks = []
        self._active_jobs = []
        self._animation_request_queue = []
        self._frames_left_until_unpause = 0

    def initialize(self):
        """Set up the pygame graphical display and load graphical resources."""
        pygame.init()
        pygame.display.set_caption('Memory Game')
        window_dimensions = (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        self._display_surface = pygame.display.set_mode(window_dimensions)
        self._is_initialized = True
        self._mouse_position = coords.PixelCoords(0, 0)
        logging.info('View initialized.')

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            self._handle_jobs()
            self._progress_animations()
            self.render_all()
        elif isinstance(event, events.MouseMovementEvent):
            self._mouse_position = event.coords
        elif isinstance(event, events.ClickEvent):
            if not self.busy: # ignore clicks if the view is busy
                self._handle_click(event.coords)
        elif isinstance(event, events.BoxOpenRequest):
            self._animation_request_queue.append(event)
        elif isinstance(event, events.BoxCloseRequest):
            self._animation_request_queue.append(event)
        elif isinstance(event, events.AnimationPause):
            self._animation_request_queue.append(event)
        elif isinstance(event, events.NewGameEvent):
            self._do_new_game_animation()
            pass
        elif isinstance(event, events.InitializeEvent):
            self.initialize()
        elif isinstance(event, events.QuitEvent):
            # ends the pygame graphical display
            pygame.quit()

    @property
    def busy(self):
        return len(self._active_jobs) > 0

    def _handle_jobs(self):
        if not self._animation_statuses.any_animations_active():
            self._check_for_new_jobs()

    def _check_for_new_jobs(self):
        more_jobs_to_do = len(self._active_jobs) > 0
        if more_jobs_to_do:
            self._start_new_job()

    def _start_new_job(self):
        new_job = self._active_jobs.pop(0)
        for coord in new_job:
            self._open_and_close_box(coord)

    def _progress_animations(self):
        if not self._animation_statuses.animations_paused:
            self._handle_animation_queue()
            for animation in self._animation_statuses.get_active_animations():
                animation.tick_animation()
        else:
            self._frames_left_until_unpause -= 1
            if self._frames_left_until_unpause <= 0:
                self._animation_statuses.unpause_animations()

    def _handle_animation_queue(self):
        requests_to_put_back = []
        while not len(self._animation_request_queue) <= 0:
            request = self._animation_request_queue.pop(0)
            if isinstance(request, events.AnimationPause):
                if self._animation_statuses.any_animations_active():
                    self._animation_request_queue.insert(0, request)
                else:
                    self._animation_statuses.pause_animations()
                    self._frames_left_until_unpause = \
                        request.seconds * settings.FPS
                return
            elif isinstance(request, events.PositionalEvent):
                target_status = self._animation_statuses.get_status(
                    request.coords)
                if not target_status.being_animated:
                    if isinstance(request, events.BoxCloseRequest):
                        self._handle_box_close_request(request)
                    elif isinstance(request, events.BoxOpenRequest):
                        self._handle_box_open_request(request)
                else:
                    requests_to_put_back.append(request)
        for request in requests_to_put_back:
            self._animation_request_queue.append(request)

    def render_all(self):
        if not self._is_initialized:
            return
        # draw stuff
        self._display_surface.fill(settings.BG_COLOR)
        self._draw_visible_icons()
        self._draw_box_covers()
        self._draw_guidelines(constants.RED)
        self._try_to_draw_highlight(self._mouse_position)
        self._draw_click_markers()
        pygame.display.update()

    def _draw_visible_icons(self):
        for coord in coords.get_all_box_coords():
            animation_status = self._animation_statuses.get_status(coord)
            if animation_status.icon_visible:
                self._draw_icon_at_coord(coord)

    def _draw_icon_at_coord(self, coord):
        icon = self._model.get_icon(coord)
        icon.draw(self._display_surface)

    def _draw_box_covers(self):
        for coord in coords.get_all_box_coords():
            if self._animation_statuses.any_animations_active():
                animation_status = self._animation_statuses.get_status(coord)
                self._draw_box_cover(coord, animation_status.coverage)
            else:
                if not self._model.is_revealed(coord):
                    self._draw_box_cover(coord, settings.BOX_SIZE)

    def _draw_box_cover(self, box_coords, coverage):
        if coverage > settings.BOX_SIZE:
            raise Exception
        topleft_corner = coords.top_left_coords_of_box(box_coords)
        if coverage > 0:
            rect_tuple = (topleft_corner.pixel_x, topleft_corner.pixel_y,
                          coverage, settings.BOX_SIZE)
            pygame.draw.rect(self._display_surface, settings.BOX_COLOR,
                             rect_tuple)

    def _draw_guidelines(self, color):
        top_line = settings.Y_MARGIN
        bottom_line = settings.WINDOW_HEIGHT - settings.Y_MARGIN
        left_line = settings.X_MARGIN
        right_line = settings.WINDOW_WIDTH - settings.X_MARGIN
        pygame.draw.line(self._display_surface, color,
                         (0, top_line),
                         (settings.WINDOW_WIDTH, top_line))
        pygame.draw.line(self._display_surface, color,
                         (0, bottom_line),
                         (settings.WINDOW_WIDTH, bottom_line))
        pygame.draw.line(self._display_surface, color,
                         (left_line, 0),
                         (left_line, settings.WINDOW_HEIGHT))
        pygame.draw.line(self._display_surface, color,
                         (right_line, 0),
                         (right_line, settings.WINDOW_HEIGHT))

    def _draw_click_markers(self):
        for click_coord in self._clicks:
            self._draw_x(click_coord, constants.GREEN)

    def _draw_x(self, coord, color):
        edge_distance = 10
        top_left = (coord.pixel_x - edge_distance,
                    coord.pixel_y - edge_distance)
        bottom_right = (coord.pixel_x + edge_distance,
                        coord.pixel_y + edge_distance)
        pygame.draw.line(self._display_surface, color, top_left, bottom_right)
        top_right = (coord.pixel_x + edge_distance,
                     coord.pixel_y - edge_distance)
        bottom_left = (coord.pixel_x - edge_distance,
                       coord.pixel_y + edge_distance)
        pygame.draw.line(self._display_surface, color, top_right, bottom_left)

    def _handle_click(self, click_coords):
        if len(self._clicks) >= 3:
            self._clicks.pop(0)
        self._clicks.append(click_coords)

    def _handle_box_open_request(self, event):
        current_status = self._animation_statuses.get_status(event.coords)
        should_open = not current_status.being_animated
        should_open = should_open and not current_status.icon_visible
        if should_open:
            self._open_box(event.coords)
            self._event_manager.post(events.BoxOpenConfirm(event.coords))

    def _handle_box_close_request(self, event):
        current_status = self._animation_statuses.get_status(event.coords)
        should_close = not current_status.being_animated
        should_close = should_close and current_status.icon_visible
        if should_close:
            self._close_box(event.coords)
            self._event_manager.post(events.BoxCloseConfirm(event.coords))

    def _open_and_close_box(self, coord):
        animation_target = self._animation_statuses.get_status(coord)
        if not animation_target.being_animated:
            animation_target.start_animation(-4, True)

    def _open_box(self, coord):
        animation_target = self._animation_statuses.get_status(coord)
        if not animation_target.being_animated:
            animation_target.start_animation(-4)

    def _close_box(self, coord):
        animation_target = self._animation_statuses.get_status(coord)
        if not animation_target.being_animated:
            animation_target.start_animation(4)

    def _do_new_game_animation(self):
        all_coords = coords.get_all_box_coords()
        random.shuffle(all_coords)
        for i in range(0, len(all_coords), REVEAL_GROUPS):
            self._active_jobs.append(all_coords[i: i + REVEAL_GROUPS])

    def _try_to_draw_highlight(self, coord):
        if coord.in_a_box:
            self._draw_highlight(coord)

    def _draw_highlight(self, coord):
        top_left = coords.top_left_coords_of_box(coord)
        highlight_thickness = math.floor(settings.GAP_SIZE / 2)
        highlight_width = settings.BOX_SIZE + settings.GAP_SIZE
        top = top_left.pixel_y - highlight_thickness
        left = top_left.pixel_x - highlight_thickness
        bounding_rect = (left, top, highlight_width, highlight_width)
        pygame.draw.rect(self._display_surface, settings.HIGHLIGHT_COLOR,
                         bounding_rect, highlight_thickness)
        
