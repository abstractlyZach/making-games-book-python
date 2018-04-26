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
        self._animation_request_queue = []
        self._frames_left_until_unpause = 0
        self._background_color = settings.BG_COLOR

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
        """Handle an event from the event manager."""
        if isinstance(event, events.TickEvent):
            self._handle_tick_event()
        elif isinstance(event, events.MouseMovementEvent):
            self._mouse_position = event.coords
        elif isinstance(event, events.ClickEvent):
            self._handle_click(event.coords)
        elif isinstance(event, events.AnimationRequest):
            self._animation_request_queue.append(event)
        elif isinstance(event, events.NewGameEvent):
            self._do_new_game_animation()
        elif isinstance(event, events.GameOverEvent):
            self._handle_game_over()
        elif isinstance(event, events.InitializeEvent):
            self.initialize()
        elif isinstance(event, events.QuitEvent):
            self._is_initialized = False
            # ends the pygame graphical display
            pygame.quit()

    def _handle_tick_event(self):
        """Handle a tick event."""
        if self._animation_statuses.animations_paused:
            self._handle_pause_tick()
        else:
            self._progress_animations()
        self.render_all()

    def _handle_pause_tick(self):
        """Handle a single tick while animations are paused."""
        self._frames_left_until_unpause -= 1
        if self._frames_left_until_unpause <= 0:
            self._animation_statuses.unpause_animations()

    def _progress_animations(self):
        """Handle a single tick of animation."""
        self._handle_animation_queue()
        for animation in self._animation_statuses.get_active_animations():
            animation.tick_animation()

    def _handle_animation_queue(self):
        """Gather animation requests and fulfill them until the queue is
        empty or a pause event is found."""
        while not len(self._animation_request_queue) <= 0:
            request = self._animation_request_queue.pop(0)
            if isinstance(request, events.AnimationPause):
                self._handle_pause_request(request)
                return
            elif isinstance(request, events.PositionalEvent):
                self._handle_box_animation_request(request)

    def _handle_pause_request(self, request):
        """If animations are active, defer the pause until they're done.
        Otherwise, pause all the animations."""
        if self._animation_statuses.any_animations_active():
            self._animation_request_queue.insert(0, request)
        else:
            self._animation_statuses.pause_animations()
            self._frames_left_until_unpause = \
                request.seconds * settings.FPS

    def _handle_box_animation_request(self, request):
        """Sort a box animation request into its proper handling function."""
        if isinstance(request, events.BoxCloseRequest):
            self._handle_box_close_request(request)
        elif isinstance(request, events.BoxOpenRequest):
            self._handle_box_open_request(request)
        elif isinstance(request, events.BoxOpenAndCloseRequest):
            self._handle_box_open_and_close_request(request)

    def render_all(self):
        """Draw the current frame to the display."""
        if not self._is_initialized:
            return
        # draw stuff
        self._display_surface.fill(self._background_color)
        self._draw_visible_icons()
        self._draw_box_covers()
        self._try_to_draw_highlight(self._mouse_position)
        # draw visual debug stuff
        if settings.VISUAL_DEBUG_MODE:
            self._draw_guidelines(constants.RED)
            self._draw_click_markers()
        # send frame to the display
        pygame.display.update()

    def _draw_visible_icons(self):
        """Draw all icons that are visible."""
        for coord in coords.get_all_box_coords():
            animation_status = self._animation_statuses.get_status(coord)
            if animation_status.icon_visible:
                self._draw_icon_at_coord(coord)

    def _draw_icon_at_coord(self, coord):
        """Draw the icon at the given coordinate."""
        icon = self._model.get_icon(coord)
        icon.draw(self._display_surface)

    def _draw_box_covers(self):
        """Draw all box covers."""
        for coord in coords.get_all_box_coords():
            if self._animation_statuses.any_animations_active():
                animation_status = self._animation_statuses.get_status(coord)
                self._draw_box_cover(coord, animation_status.coverage)
            else:
                if not self._model.is_revealed(coord):
                    self._draw_box_cover(coord, settings.BOX_SIZE)

    def _draw_box_cover(self, box_coords, coverage):
        """Draw the box cover at the given coordinate. Coverage is the
        number of pixels of width that this cover is using to cover its box."""
        if coverage > settings.BOX_SIZE:
            raise Exception
        topleft_corner = coords.top_left_coords_of_box(box_coords)
        if coverage > 0:
            rect_tuple = (topleft_corner.pixel_x, topleft_corner.pixel_y,
                          coverage, settings.BOX_SIZE)
            pygame.draw.rect(self._display_surface, settings.BOX_COLOR,
                             rect_tuple)

    def _draw_guidelines(self, color):
        """Draw guidelines so you can see where the margins are."""
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
        """Draw markers that denote where the last few clicks were."""
        for click_coord in self._clicks:
            self._draw_x(click_coord, constants.GREEN)

    def _draw_x(self, coord, color):
        """Draw an 'X' at the given coordinates."""
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
        """Record the click in memory."""
        if len(self._clicks) >= 3:
            self._clicks.pop(0)
        self._clicks.append(click_coords)

    def _handle_box_open_and_close_request(self, event):
        """Handle a BoxOpenAndCloseRequest."""
        current_status = self._animation_statuses.get_status(event.coords)
        should_open = not current_status.being_animated
        should_open = should_open and not current_status.icon_visible
        if should_open:
            self._open_and_close_box(event.coords)

    def _handle_box_open_request(self, event):
        """Handle a BoxOpenRequest."""
        current_status = self._animation_statuses.get_status(event.coords)
        should_open = not current_status.being_animated
        should_open = should_open and not current_status.icon_visible
        if should_open:
            self._open_box(event.coords)
            self._event_manager.post(events.BoxOpenConfirm(event.coords))

    def _handle_box_close_request(self, event):
        """Handle a BoxCloseRequest."""
        current_status = self._animation_statuses.get_status(event.coords)
        should_close = not current_status.being_animated
        should_close = should_close and current_status.icon_visible
        if should_close:
            self._close_box(event.coords)
            self._event_manager.post(events.BoxCloseConfirm(event.coords))

    def _open_and_close_box(self, coord):
        """Open and close a box."""
        animation_target = self._animation_statuses.get_status(coord)
        if not animation_target.being_animated:
            animation_target.start_animation(-4, True)

    def _open_box(self, coord):
        """Open a box."""
        animation_target = self._animation_statuses.get_status(coord)
        if not animation_target.being_animated:
            animation_target.start_animation(-4)

    def _close_box(self, coord):
        """Close a box."""
        animation_target = self._animation_statuses.get_status(coord)
        if not animation_target.being_animated:
            animation_target.start_animation(4)

    def _do_new_game_animation(self):
        """Drop animation requests onto the queue for the new game
        animation."""
        all_coords = coords.get_all_box_coords()
        random.shuffle(all_coords)
        for i in range(0, len(all_coords), REVEAL_GROUPS):
            for coord in all_coords[i: i + REVEAL_GROUPS]:
                self._animation_request_queue.append(
                    events.BoxOpenAndCloseRequest(coord))
            self._animation_request_queue.append(events.AnimationPause(0))

    def _try_to_draw_highlight(self, coord):
        """Attempt to draw a highlight at the coordinate to show where the
        mouse is."""
        if coord.in_a_box:
            self._draw_highlight(coord)

    def _draw_highlight(self, coord):
        """Draw a highlight around the box at the given coord."""
        top_left = coords.top_left_coords_of_box(coord)
        highlight_thickness = math.floor(settings.GAP_SIZE / 2)
        highlight_width = settings.BOX_SIZE + settings.GAP_SIZE
        top = top_left.pixel_y - highlight_thickness
        left = top_left.pixel_x - highlight_thickness
        bounding_rect = (left, top, highlight_width, highlight_width)
        pygame.draw.rect(self._display_surface, settings.HIGHLIGHT_COLOR,
                         bounding_rect, highlight_thickness)

    def _handle_game_over(self):
        """Handle the game over event."""
        self._do_game_over_animation()
        self._event_manager.post(events.NewGameEvent())

    def _do_game_over_animation(self):
        """Animate the board to celebrate victory."""
        color1 = settings.LIGHT_BG_COLOR
        color2 = settings.BG_COLOR
        self._animation_statuses = animation.AnimationStatusTracker()
        for i in range(13):
            color1, color2 = color2, color1
            self._background_color = color1
            self.render_all()
            pygame.time.wait(300)
        self._background_color = settings.BG_COLOR

