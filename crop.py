from PIL import Image

def crop(orig_image: Image.Image, top_left: tuple[int, int], bottom_right: tuple[int, int]) -> Image.Image | None:    
    # Keeping track of original size and new size.
    orig_width = orig_image.width
    orig_height = orig_image.height
    
    # Using the two corners to determine the cropped image's size.
    new_width = bottom_right[0] - top_left[0]
    new_height = bottom_right[1] - top_left[1]
    
    # Using try-except block to check an assertion that basically asks if the top left coerner is actually a top-left corner
    # and the bottom-right corner is actually a bottom-right corner.
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
        print("Assertion Failed: Invalid Crop")
        return None

    # Creating the vessel for our cropped image.
    cropped_size: tuple[int, int] = (bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])
    cropped_image: Image.Image = Image.new("RGB", cropped_size)
    
    # Nested for loop using putpixel at x and y. I have found putpixel() is slow, but the cropping process
    # isn't very complicated and this runs pretty quickly. Using get_flattened_data() and putdata() would be
    # a pain in the ass for this algorithm.
    for x in range(new_width):
        for y in range(new_height):
            _x = x + top_left[0]
            _y = y + top_left[1]
            replacement = orig_image.getpixel((_x, _y))
            cropped_image.putpixel((x, y), replacement) # pyright: ignore[reportArgumentType]
    
    return cropped_image

# USAGE EXAMPLE. Checking the type is probably optional, but it is safer / good practice given the function can return type None:
# new_img = crop(Image.open("static/images/Space Desert.jpg"), (100, 100), (200, 400))
# if(type(new_img) == Image.Image):
#     new_img.show()