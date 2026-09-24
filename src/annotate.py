# draws a box + label around every detected item, returns the image

from PIL import Image, ImageDraw, ImageFont


def annotateImage(img, detections):
    # work on a copy so the original photo stays clean
    imgCopy = img.convert("RGB").copy()
    draw = ImageDraw.Draw(imgCopy)

    # default font is tiny, use the mac one if it exists
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except OSError:
        font = ImageFont.load_default()

    for det in detections:
        boxCoords = det.get("box")
        if not boxCoords:
            continue

        x1, y1, x2, y2 = boxCoords

        # clip in case a box goes outside the photo
        x1 = max(0, min(x1, imgCopy.width - 1))
        y1 = max(0, min(y1, imgCopy.height - 1))
        x2 = max(0, min(x2, imgCopy.width - 1))
        y2 = max(0, min(y2, imgCopy.height - 1))

        draw.rectangle([x1, y1, x2, y2], outline="lime", width=2)

        # label looks like "bottle 87%", conf isnt always in the dict
        classLabel = det.get("class", "unknown")
        confScore = det.get("conf")
        if confScore is not None:
            labelText = f"{classLabel} {round(confScore * 100)}%"
        else:
            labelText = str(classLabel)

        # black background behind the text so its readable on anything
        # put it above the box unless theres no room up there
        labelY = y1 - 16 if y1 > 16 else y1
        textBox = draw.textbbox((x1, labelY), labelText, font=font)
        draw.rectangle(textBox, fill="black")
        draw.text((x1, labelY), labelText, fill="white", font=font)

    return imgCopy
