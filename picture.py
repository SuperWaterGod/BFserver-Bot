from PIL import Image, ImageDraw, ImageFont


def AlphaPicOverlay(MotherImg, SonImg, SaveImg, x, y, Opacity=1):
    overlay = Image.open(SonImg)
    base = Image.open(MotherImg)
    bands = list(overlay.split())
    if len(bands) == 4:
        bands[3] = bands[3].point(lambda x: x * Opacity)
        overlay = Image.merge(overlay.mode, bands)
        base.paste(overlay, (x, y), overlay)
        base.save(SaveImg)