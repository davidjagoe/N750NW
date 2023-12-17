
import exifread
import glob
import os
import shutil
import subprocess

from datetime import datetime


INBOX = glob.glob("../PhotoInbox/*")
STAGING_DIR = "../Staging"
OUTBOX = "../Staging/img"
NEW_POST_FILENAME = "../Staging/post.org"


def _get_datetime_from_exif_tags(tags):
    exif_dt_string = tags["EXIF DateTimeOriginal"]
    date_string, time_string = tuple(str(exif_dt_string).split(" "))
    dt_string = date_string.replace(":", "-") + "T" + time_string
    return datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S")


def _clean_staging():
    try:
        shutil.rmtree(STAGING_DIR)
    except Exception:
        pass
    os.mkdir(STAGING_DIR)
    os.mkdir(OUTBOX)


def main():
    items = {}

    _clean_staging()
    
    for filename in INBOX:
        with open(filename, "rb") as image_file:
            tags = exifread.process_file(image_file)
            try:
                photo_datetime = _get_datetime_from_exif_tags(tags).date()
                items.setdefault(photo_datetime, []).append(filename)
            except Exception:
                print("Error processing {0}".format(filename))

    with open(NEW_POST_FILENAME, "w") as orgmode_file:
        for dt in sorted(items.keys()):
            orgmode_file.write("* [{date}]\n".format(date=dt))
            for path in items[dt]:
                basename = os.path.basename(path)
                orgmode_file.write("#+CAPTION: \n")
                orgmode_file.write("#+ATTR_HTML: :width 400px\n")
                orgmode_file.write("[[./img/{name}]]\n".format(name=basename))
                # Resizing here is not ideal, but unfortunately I'm
                # using Emacs on Windows without imagemagick compile
                # option, so org-mode cannot auto-size images for
                # me. The raw images are too large for me to
                # practically in-line images in emacs while writing
                # the text content.
                subprocess.call(["magick", "convert", path, "-auto-orient", "-resize", "800x800", os.path.join(OUTBOX, basename)])
            orgmode_file.write("\n")

    print("""

DONE.

    You can now review and edit {new_post}, then copy {resized_photos}/*
    to the build log img directory, and the reviewed post content to the
    build log.""".format(new_post=NEW_POST_FILENAME, resized_photos=OUTBOX))
    

if __name__ == "__main__":
    main()
