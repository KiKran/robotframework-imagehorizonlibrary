# -*- coding: utf-8 -*-
import pyautogui as ag

from ..errors import MouseException


class _Mouse(object):

    def _click_to_the_direction_of(self, direction, location, offset,
                                   clicks, button, interval):
        raise NotImplementedError('This is defined in the main class.')

    def click_to_the_above_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        '''Clicks above of given location by given offset.

        ``location`` can be any Python sequence type (tuple, list, etc.) that
        represents coordinates on the screen ie. have an x-value and y-value.
        Locating-related keywords return location you can use with this
        keyword.

        ``offset`` is the number of pixels from the specified ``location``.

        ``clicks`` is how many times the mouse button is clicked.

        See `Click` for documentation for valid buttons.

        Example:

        | ${image location}=    | Locate             | my image |        |
        | Click To The Above Of | ${image location}  | 50       |        |
        | @{coordinates}=       | Create List        | ${600}   | ${500} |
        | Click To The Above Of | ${coordinates}     | 100      |        |
        '''
        self._click_to_the_direction_of('up', location, offset,
                                        clicks, button, interval)

    def click_to_the_below_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        '''Clicks below of given location by given offset.

        See argument documentation in `Click To The Above Of`.
        '''
        self._click_to_the_direction_of('down', location, offset,
                                        clicks, button, interval)

    def click_to_the_left_of(self, location, offset, clicks=1,
                             button='left', interval=0.0):
        '''Clicks left of given location by given offset.

        See argument documentation in `Click To The Above Of`.
        '''
        self._click_to_the_direction_of('left', location, offset,
                                        clicks, button, interval)

    def click_to_the_right_of(self, location, offset, clicks=1,
                              button='left', interval=0.0):
        '''Clicks right of given location by given offset.

        See argument documentation in `Click To The Above Of`.
        '''
        self._click_to_the_direction_of('right', location, offset,
                                        clicks, button, interval)

    def click_with_offset_from_location(self, location: tuple, x_offset: int = 0, y_offset: int = 0, clicks=1,
                                        button='left', interval=0.0):
        '''       
        Clicks at given location with offset in both planes.

        ``location`` can be any Python sequence type (tuple, list, etc.) that
        represents coordinates on the screen ie. have an x-value and y-value.
        Locating-related keywords return location you can use with this
        keyword.

        ``x_offset`` is the number of pixels from the specified ``location`` on the x-plane. Positive is offset to the right, negative to the left

        ``y_offset`` is the number of pixels from the specified ``location`` on the y-plane. Positive is offset to the top, negative to the bottom.

        ``clicks`` is how many times the mouse button is clicked.

        See `Click` for documentation for valid buttons.

        v1.2 Keyword

        Example:

        | ${image location}=    | Locate             | my image |        ||
        | Click With Offset From Location | ${image location}  | 50       | -20        ||
        | @{coordinates}=       | Create List        | ${600}   | ${500} ||
        | Click With Offset From Location | ${coordinates}     | 0      | 25       | 2|
        '''
        self._advanced_click_to_the_direction_of(location, x_offset, y_offset,
                                                 clicks, button, interval)

    def click_location(self, location: tuple):
        '''
        Clicks at given location. (No need for Click in direction with offset=0)
        '''
        ag.click(location)

    def move_to(self, *coordinates):
        '''Moves the mouse pointer to an absolute coordinates.

        ``coordinates`` can either be a Python sequence type with two values
        (eg. ``(x, y)``) or separate values ``x`` and ``y``:

        | Move To         | 25             | 150       |     |
        | @{coordinates}= | Create List    | 25        | 150 |
        | Move To         | ${coordinates} |           |     |
        | ${coords}=      | Evaluate       | (25, 150) |     |
        | Move To         | ${coords}      |           |     |


        X grows from left to right and Y grows from top to bottom, which means
        that top left corner of the screen is (0, 0)
        '''
        if len(coordinates) > 2 or (len(coordinates) == 1 and
                                    type(coordinates[0]) not in (list, tuple)):
            raise MouseException('Invalid number of coordinates. Please give '
                                 'either (x, y) or x, y.')
        if len(coordinates) == 2:
            coordinates = (coordinates[0], coordinates[1])
        else:
            coordinates = coordinates[0]
        try:
            coordinates = [int(coord) for coord in coordinates]
        except ValueError:
            raise MouseException(
                f'Coordinates {coordinates, } are not integers')    #todo test the comma in f-string
        ag.moveTo(*coordinates)

    def mouse_down(self, button='left'):
        '''Presses specidied mouse button down'''
        ag.mouseDown(button=button)

    def mouse_up(self, button='left'):
        '''Releases specified mouse button'''
        ag.mouseUp(button=button)

    def click(self, button='left'):
        '''Clicks with the specified mouse button.

        Valid buttons are ``left``, ``right`` or ``middle``.
        '''
        ag.click(button=button)

    def double_click(self, button='left', interval=0.0):
        '''Double clicks with the specified mouse button.

        See documentation of ``button`` in `Click`.

        ``interval`` specifies the time between clicks and should be
        floating point number.
        '''
        ag.doubleClick(button=button, interval=float(interval))

    def triple_click(self, button='left', interval=0.0):
        '''Triple clicks with the specified mouse button.

        See documentation of ``button`` in `Click`.

        See documentation of ``interval`` in `Double Click`.
        '''
        ag.tripleClick(button=button, interval=float(interval))

    def click_with_offset(self, x_offset: int = 0, y_offset: int = 0, button: str = 'left', clicks: int = 1, interval: float = 0.0):
        '''
        Advanced click option on the current mouse position with all possible click adjustments.

        `x_offset` (int): offset on the x-plane. Positive is offset to the right, negative to the left
        `y_offset` (int): offset on the y-plane. Positive is offset to the top, negative to the bottom

        See documentation of ``button`` in `Click`.

        See documentation of ``interval`` in `Double Click`.
        v1.2 Keyword
        '''
        if interval != 0.0 and clicks == 1:
            raise MouseException(
                f'Click interval is set ({interval}) but number of clicks is set to 1.')
        self._advanced_click_to_the_direction_of(None,
                                                 x_offset, y_offset, clicks, button, interval)

    def scroll_window(self, scroll_amount: int = -500) -> None:
        """
        Scrolls by given amount. Positive amount is upwards, negative downwards.
        Does not fail if screen can not be scrolled.

        ### Args
        `scroll_amount` (int): Amount to scroll up- or downwards, default is -500 (downwards)
        """
        if isinstance(scroll_amount, int):
            ag.scroll(scroll_amount)
        elif isinstance(scroll_amount, str):
            ag.scroll(int(scroll_amount))
        else:
            raise MouseException(
                f'Given number for `scroll_amount` could not be resolved: {scroll_amount}, type: {type(scroll_amount)}.')
