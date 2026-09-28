from PIL import ImageDraw, ImageFont


def annotateImage(img, detections):
    # work on a copy so the original photo stays clean
    img_copy = img.convert("RGB").copy()
    draw = ImageDraw.Draw(img_copy)

    # default font is tiny, use the mac one if it exists
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except OSError:
        font = ImageFont.load_default()

    for det in detections:
        box_coords = det.get("box")
        if not box_coords:
            continue

        x1, y1, x2, y2 = box_coords

        # clip in case a box goes outside the photo
        x1 = max(0, min(x1, img_copy.width - 1))
        y1 = max(0, min(y1, img_copy.height - 1))
        x2 = max(0, min(x2, img_copy.width - 1))
        y2 = max(0, min(y2, img_copy.height - 1))

        draw.rectangle([x1, y1, x2, y2], outline="lime", width=4)

        # label looks like "bottle 87%", conf isnt always in the dict
        class_label = det.get("class", "unknown")
        conf_score = det.get("conf")
        if conf_score is not None:
            label_text = f"{class_label} {round(conf_score * 100)}%"
        else:
            label_text = str(class_label)

        # black background behind the text so its readable on anything
        # put it above the box unless theres no room up there
        label_y = y1 - 16 if y1 > 16 else y1
        text_box = draw.textbbox((x1, label_y), label_text, font=font)
        draw.rectangle(text_box, fill="black")
        draw.text((x1, label_y), label_text, fill="white", font=font)

    return img_copy
