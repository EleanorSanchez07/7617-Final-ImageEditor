from PIL import Image

def crop(orig_image: Image.Image, top_left: tuple[int, int], bottom_right: tuple[int, int]) -> Image.Image | None:    
    orig_width = orig_image.width
    orig_height = orig_image.height
    
    new_width = bottom_right[0] - top_left[0]
    new_height = bottom_right[1] - top_left[1]
    
    try:
        assert(
            new_width > 0 and
            new_height > 0 and
            top_left[0] >= 0 and
            top_left[1] >= 0 and
            bottom_right[0] <= orig_width and
            bottom_right[1] <= orig_height
        )
    except AssertionError:
        print("Invalid Crop")
        return None

    cropped_size: tuple[int, int] = (bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])
    cropped_image: Image.Image = Image.new("RGB", cropped_size)
    
    for x in range(new_width):
        for y in range(new_height):
            _x = x + top_left[0]
            _y = y + top_left[1]
            replacement = orig_image.getpixel((_x, _y))
            cropped_image.putpixel((x, y), replacement) # pyright: ignore[reportArgumentType]
    
    return cropped_image

# USAGE EXAMPLE. Checking the type is probably optional, but it is safer:
# new_img = crop(Image.open("static/images/Space Desert.jpg"), (100, 100), (200, 400))
# if(type(new_img) == Image.Image):
#     new_img.show()