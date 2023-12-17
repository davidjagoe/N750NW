"""Got a new phone. Now I have overlapping photo filenames. This script puts
a unique id in each filename."""

import glob
import os
import shutil
import uuid


INBOX = glob.glob("../PhotoInbox/*")


def main():
    
    for filename in INBOX:
        unique_id = uuid.uuid4()
        new_filename = str(unique_id) + "_" + os.path.basename(filename)
        dest = os.path.join(os.path.dirname(filename), new_filename)
        shutil.move(filename, dest)
        

if __name__ == "__main__":
    main()
