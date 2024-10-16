from .camera import add_rtsp_capture
from .dates import add_calendar_block
from .local_image import add_local_image
from .weather import add_weather_block
from .web_image import add_web_image

__all__ = (
    add_rtsp_capture,
    add_calendar_block,
    add_local_image,
    add_weather_block,
    add_web_image,
)
