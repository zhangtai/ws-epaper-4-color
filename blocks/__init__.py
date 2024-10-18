from .camera import add_rtsp_capture
from .dates import add_calendar_block
from .local_image import add_local_image
from .stock import draw_stock
from .weather import add_weather_block
from .web_image import add_web_image
from .room_temperature import draw_room_temperature

__all__ = (
    add_rtsp_capture,
    add_calendar_block,
    draw_room_temperature,
    draw_stock,
    add_local_image,
    add_weather_block,
    add_web_image,
)
