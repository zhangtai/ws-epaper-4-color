from PIL import ImageDraw


def draw_room_temperature(draw: ImageDraw, position: tuple[int, int]):
    # Draw the outer rectangle
    draw.rectangle(
        [position, (position[0] + 800, position[1] + 600)], outline="black", width=3
    )

    # Draw the first horizontal line
    # draw.line([(50, 300), (750, 300)], fill="black", width=3)

    # Draw the second horizontal line
    # draw.line([(50, 425), (500, 425)], fill="black", width=3)

    # Draw the vertical line
    # draw.line([(500, 300), (500, 550)], fill="black", width=3)
