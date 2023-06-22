#@title 🖥️ Main Colab Leech Code [ Click to Magic ✨ ]
import os
import io
import re

# import sys
import cv2
import time
import psutil
import shutil
import pickle
import uvloop
import zipfile
import datetime
import subprocess
from PIL import Image
from pyrogram import Client
from natsort import natsorted
from urllib.parse import urlparse
from re import search as re_search
from os import makedirs, path as ospath
from IPython.display import clear_output
from urllib.parse import parse_qs, urlparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from pyrogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

uvloop.install()


# =================================================================
#    Local OS Functions
# =================================================================


def convert_seconds(seconds):
    seconds = int(seconds)
    days = seconds // (24 * 3600)
    seconds = seconds % (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    if days > 0:
        return f"{days}d {hours}h {minutes}m {seconds}s"
    elif hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def size_measure(size):
    if size > 1024 * 1024 * 1024 * 1024:
        siz = f"{size/(1024**4):.2f} TiB"
    elif size > 1024 * 1024 * 1024:
        siz = f"{size/(1024**3):.2f} GiB"
    elif size > 1024 * 1024:
        siz = f"{size/(1024**2):.2f} MiB"
    elif size > 1024:
        siz = f"{size/1024:.2f} KiB"
    else:
        siz = f"{size} B"
    return siz


def get_file_type(file_path):
    name, extension = os.path.splitext(file_path)

    extensions_dict = {
        ".mp4": "video",
        ".avi": "video",
        ".mkv": "video",
        ".mov": "video",
        ".webm": "video",
        ".vob": "video",
        ".m4v": "video",
        ".mp3": "audio",
        ".wav": "audio",
        ".flac": "audio",
        ".aac": "audio",
        ".ogg": "audio",
        ".jpg": "photo",
        ".jpeg": "photo",
        ".png": "photo",
        ".gif": "photo",
    }

    if extension.lower() in extensions_dict:
        if extensions_dict[extension] == "video":
            video_extension_fixer(file_path)
        return extensions_dict[extension]
    else:
        return "document"


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def get_file_count(folder_path):
    count = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            count += 1
    return count


def video_extension_fixer(file_path):
    dir_path, filename = os.path.split(file_path)

    if filename.endswith(".mp4") or filename.endswith(".mkv"):
        pass
    # split the file name and the extension
    else:
        # rename the video file with .mp4 extension
        name, ext = os.path.splitext(filename)
        os.rename(
            os.path.join(dir_path, filename), os.path.join(dir_path, name + ".mp4")
        )
        print(f"{filename} was changed to {name}.mp4")


def system_info():
    ram_usage = psutil.Process(os.getpid()).memory_info().rss
    disk_usage = psutil.disk_usage("/")
    cpu_usage_percent = psutil.cpu_percent()

    string = "\n\n⍟───── [Colab Usage](https://colab.research.google.com/drive/12hdEqaidRZ8krqj7rpnyDzg1dkKmvdvp) ─────⍟\n"
    string += f"\n╭🖥️ **CPU Usage »**  {cpu_usage_percent}%"
    string += f"\n├💽 **RAM Usage »**  {size_measure(ram_usage)}"
    string += f"\n╰💾 **DISK Free »**  {size_measure(disk_usage.free)}"
    string += f"\n\n<i>💖 When I'm Doin This, Do Something Else. **Time Is Precious ✨**</i>"

    return string


async def zip_folder(path):
    # Calculate total size of folder to track progress
    print("Function Triggered")
    chunk_size = 1024 * 1024 * 80  # 80 megabyte
    bytes_written = zip_speed = 0
    starting_time = datetime.datetime.now()
    if os.path.isfile(path):
        total_size = os.path.getsize(path)
        zip_msg = (
            f"<b>🔐 ZIPPING B4 SPLIT » </b>\n\n<code>{os.path.basename(path)}</code>\n"
        )
        with zipfile.ZipFile(
            f"{path}.zip", "w", compression=zipfile.ZIP_STORED
        ) as zipf:
            with open(path, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    zipf.writestr(os.path.basename(path), chunk)
                    bytes_written += len(chunk)
                    speed_string, eta, percentage = speed_eta(
                        starting_time, bytes_written, total_size
                    )
                    await status_bar(
                        zip_msg,
                        speed_string,
                        percentage,
                        convert_seconds(eta),
                        size_measure(bytes_written),
                        size_measure(total_size),
                        "Xr-Zipp 🔒",
                    )
        os.remove(path)

    elif os.path.isdir(path):
        total_size = get_folder_size(path)
        with zipfile.ZipFile(
            f"{path}.zip", "w", compression=zipfile.ZIP_STORED
        ) as zip_file:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, path)
                    with open(file_path, "rb") as f:
                        while True:
                            chunk = f.read(chunk_size)
                            if not chunk:
                                break
                            zip_file.writestr(rel_path, chunk)
                            bytes_written += len(chunk)
                            speed_string, eta, percentage = speed_eta(
                                starting_time, bytes_written, total_size
                            )
                            await status_bar(
                                down_msg,
                        "N/A",
                        percentage,
                                convert_seconds(eta),
                                size_measure(bytes_written),
                                size_measure(total_size),
                                "Xr-Zipp 🔒",
                            )
                        # Delete the file after writing it to the zip object.
                        os.remove(file_path)
    else:
        raise ValueError("Invalid path")
    return f"{path}.zip"


async def extract_zip(zip_filepath):
    if not os.path.exists(temp_unzip_path):
        makedirs(temp_unzip_path)

    with zipfile.ZipFile(zip_filepath) as zf:
        num_files = len(zf.infolist())

        total_size = sum(file.file_size for file in zf.infolist())
        extracted_size = 0
        print(f"Extracting {num_files} files...")
        for i, member in enumerate(zf.infolist(), 1):
            # print(f"Extracting {member.filename} ({member.file_size} bytes)")
            extracted_size += member.file_size
            zf.extract(member, temp_unzip_path)
            percentage = (extracted_size / total_size) * 100 if total_size else 0

            down_msg = f"<b>📂 EXTRACTING »</b>\n\n<code>{d_name}</code>\n"

            await status_bar(
                down_msg,
                "N/A",
                percentage,
                "N/A",
                size_measure(extracted_size),
                size_measure(os.stat(zip_filepath).st_size),
                "Xr-Unzip 🔓",
            )


async def size_checker(file_path):
    max_size = 2097152000  # 2 GB
    file_size = os.stat(file_path).st_size

    if file_size > max_size:
        print(f"File size is {size_measure(file_size)} SPLITTING.......")

        if not ospath.exists(temp_lpath):
            makedirs(temp_lpath)

        await split_zipFile(file_path, max_size)

        return True
    else:
        print(f"File size is {size_measure(file_size)} MB. NOT SPLITTING.......")
        return False


async def split_zipFile(file_path, max_size):
    dir_path, filename = os.path.split(file_path)
    new_path = f"{temp_lpath}/{filename}"
    down_msg = f"<b>✂️ SPLITTING » </b>\n\n<code>{filename}</code>\n"
    # Get the total size of the file
    total_size = os.path.getsize(file_path)

    with open(file_path, "rb") as f:
        chunk = f.read(max_size)
        i = 1
        bytes_written = 0

        while chunk:
            # Generate filename for this chunk
            ext = str(i).zfill(3)
            output_filename = "{}.{}".format(new_path, ext)

            # Write chunk to file
            with open(output_filename, "wb") as out:
                out.write(chunk)

            bytes_written += len(chunk)
            percentage = bytes_written / total_size * 100

            await status_bar(
                down_msg,
                "N/A",
                percentage,
                "N/A",
                size_measure(bytes_written),
                size_measure(total_size),
                "Xr-Split ✂️",
            )
            # Get next chunk
            chunk = f.read(max_size)
            i += 1 # Increment chunk counter


def is_time_over(current_time):
    ten_sec_passed = time.time() - current_time[0] >= 3
    if ten_sec_passed:
        current_time[0] = time.time()
    return ten_sec_passed


# =================================================================
#    Direct Link Handler Functions
# =================================================================


async def on_output(output: str):
    # print("=" * 60 + f"\n\n{output}\n\n" + "*" * 60)

    total_size = "0B"
    progress_percentage = "0B"
    downloaded_bytes = "0B"
    chunk_size = "0B"
    eta = "0S"
    try:
        if "ETA:" in output:
            parts = output.split()
            total_size = parts[1].split("/")[1]
            total_size = total_size.split("(")[0]
            progress_percentage = parts[1][parts[1].find("(") + 1 : parts[1].find(")")]
            downloaded_bytes = parts[1].split("/")[0]
            eta = parts[4].split(":")[1][:-1]
    except Exception as do:
        print(f"Could't Get Info Due to: {do}")

    # print("Total download size:", total_size)
    # print("Progress percentage:", progress_percentage)
    # print("Downloaded bytes:", downloaded_bytes)
    # print("Estimated Time:", eta)

    percentage = re.findall("\d+\.\d+|\d+", progress_percentage)[0]
    down = re.findall("\d+\.\d+|\d+", downloaded_bytes)[0]
    down_unit = re.findall("[a-zA-Z]+", downloaded_bytes)[0]
    if "G" in down_unit:
        spd = 3
    elif "M" in down_unit:
        spd = 2
    elif "K" in down_unit:
        spd = 1
    else:
        spd = 0

    # Only Do this if got Information
    if total_size != "0B":
        # Calculate download speed
        elapsed_time_seconds = (datetime.datetime.now() - start_time).seconds
        current_speed = (float(down) * 1024**spd) / elapsed_time_seconds
        speed_string = f"{size_measure(current_speed)}/s"

        await status_bar(
            down_msg,
            speed_string,
            int(percentage),
            eta,
            downloaded_bytes,
            total_size,
            "Aria2c 🧨",
        )


async def aria2_Download(link):
    # Create a command to run aria2p with the link
    command = [
        "aria2c",
        "-x10",
        "--seed-time=0",
        "--summary-interval=1",
        "--console-log-level=notice",
        "-d",
        d_fol_path,
        link,
    ]

    # Run the command using subprocess.Popen
    process = subprocess.Popen(
        command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Read and print output in real-time
    while True:
        output = process.stdout.readline()

        if output == b"" and process.poll() is not None:
            break
        if output:
            # sys.stdout.write(output.decode("utf-8"))
            # sys.stdout.flush()
            await on_output(output.decode("utf-8"))

    # Retrieve exit code and any error output
    exit_code = process.wait()
    error_output = process.stderr.read()
    if exit_code != 0:
        raise Exception(
            f"aria2c command failed with return code {exit_code}\n\nError: {error_output}"
        )


# =================================================================
#    G Drive Functions
# =================================================================


def build_service():
    # create credentials object from token.pickle file
    creds = None
    if os.path.exists("/content/token.pickle"):
        with open("/content/token.pickle", "rb") as token:
            creds = pickle.load(token)
    else:
        exit(1)

    # create drive API client
    service = build("drive", "v3", credentials=creds)

    return service


async def g_DownLoad(link):
    global d_fol_path, start_time, d_name

    file_id = getIDFromURL(link)

    meta = getFileMetadata(file_id)

    d_name = meta["name"]


    d_fol_path = f"{d_path}/{d_name}"

    if meta.get("mimeType") == "application/vnd.google-apps.folder":
        folder_info[0] = get_Gfolder_size(file_id)
        print(f"\nTotal Download size is: {size_measure(folder_info[0])}")
        current_time[0] = time.time()
        start_time = datetime.datetime.now()
        await gDownloadFolder(file_id, d_path)
        clear_output()
        print("*" * 40 + "\n Folder Download Complete\n" + "*" * 40)

    else:
        file_metadata = getFileMetadata(file_id)
        folder_info[0] = int(
            file_metadata["size"]
        )  # Get the file size from the metadata:
        print(f"\nTotal Download size is: {size_measure(folder_info[0])}")

        if not ospath.exists(d_fol_path):
            makedirs(d_fol_path)
        current_time[0] = time.time()
        start_time = datetime.datetime.now()
        await gDownloadFile(file_id, d_fol_path)
        clear_output()
        print("*" * 40 + "\n File Download Complete\n" + "*" * 40)


def getIDFromURL(link: str):
    if "folders" in link or "file" in link:
        regex = r"https:\/\/drive\.google\.com\/(?:drive(.*?)\/folders\/|file(.*?)?\/d\/)([-\w]+)"
        res = re_search(regex, link)
        if res is None:
            raise IndexError("G-Drive ID not found.")
        return res.group(3)
    parsed = urlparse(link)
    return parse_qs(parsed.query)["id"][0]


def getFilesByFolderID(folder_id):
    page_token = None
    files = []
    while True:
        response = (
            service.files()
            .list(
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                q=f"'{folder_id}' in parents and trashed = false",
                spaces="drive",
                pageSize=200,
                fields="nextPageToken, files(id, name, mimeType, size, shortcutDetails)",
                orderBy="folder, name",
                pageToken=page_token,
            )
            .execute()
        )
        files.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if page_token is None:
            break
    return files


def getFileMetadata(file_id):
    return (
        service.files()
        .get(fileId=file_id, supportsAllDrives=True, fields="name, id, mimeType, size")
        .execute()
    )


def get_Gfolder_size(folder_id):
    try:
        query = "trashed = false and '{0}' in parents".format(folder_id)
        results = (
            service.files()
            .list(
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                q=query,
                fields="files(id, mimeType, size)",
            )
            .execute()
        )

        total_size = 0
        items = results.get("files", [])

        folders_without_size = (
            item["id"]
            for item in items
            if item.get("size") is None
            and item["mimeType"] == "application/vnd.google-apps.folder"
        )

        for item in items:
            # If the item has a size attribute
            if "size" in item:
                total_size += int(item["size"])

        # Recursively call the function for folders whose size is not found
        for folder_id in folders_without_size:
            total_size += get_Gfolder_size(folder_id)

        return total_size

    except HttpError as error:
        print(f"Error while checking size: {error}")
        return -1


async def downloadProgress(file_size):
    global start_time

    down_done = sum(down_bytes) + file_size

    speed_string = ""

    if down_done > 0:
        elapsed_time_seconds = (datetime.datetime.now() - start_time).seconds
        down_speed = down_done / elapsed_time_seconds
        speed_string = f"{size_measure(down_speed)}/s"

    eta = (folder_info[0] - down_done) / down_speed

    down_msg = f"<b>📥 DOWNLOADING » </b>\n\n<code>{d_name}</code>\n"

    percentage = down_done / folder_info[0] * 100

    await status_bar(
        down_msg=down_msg,
        speed=speed_string,
        percentage=percentage,
        eta=convert_seconds(eta),
        done=size_measure(down_done),
        left=size_measure(folder_info[0]),
        engine="G-API ♻️",
    )


async def gDownloadFile(file_id, path):
    # Check if the specified file or folder exists and is downloadable.
    try:
        file = getFileMetadata(file_id)
    except HttpError as error:
        print("An error occurred: {0}".format(error))
        file = None
    if file is None:
        print(
            "Sorry, the specified file or folder does not exist or is not accessible."
        )
    else:
        if file["mimeType"].startswith("application/vnd.google-apps"):
            print(
                "Sorry, the specified ID is for a Google Docs, Sheets, Slides, or Forms document. You can only download these types of files in specific formats."
            )
        else:
            try:
                file_name = file.get("name", f"untitleddrivefile_{file_id}")
                file_name = os.path.join(path, file_name)
                # Create a BytesIO stream to hold the downloaded file data.
                file_contents = io.BytesIO()

                # Download the file or folder contents to the BytesIO stream.
                request = service.files().get_media(
                    fileId=file_id, supportsAllDrives=True
                )
                file_downloader = MediaIoBaseDownload(
                    file_contents, request, chunksize=50 * 1024 * 1024
                )
                done = False
                while done is False:
                    status, done = file_downloader.next_chunk()
                    # Get current value from file_contents.
                    file_contents.seek(0)
                    with open(file_name, "ab") as f:
                        f.write(file_contents.getvalue())
                    # Reset the buffer for the next chunk.
                    file_contents.seek(0)
                    file_contents.truncate()
                    # The saved bytes till now
                    file_d_size = int(status.progress() * int(file["size"]))
                    await downloadProgress(file_d_size)

                print(f"DOWNLOADED  =>   {os.path.basename(file_name)}")
                down_bytes.append(int(file["size"]))
                down_count[0] += 1

            except Exception as e:
                print("Error downloading: {0}".format(e))


async def gDownloadFolder(folder_id, path):
    folder_meta = getFileMetadata(folder_id)
    folder_name = folder_meta["name"]
    if not ospath.exists(f"{path}/{folder_name}"):
        makedirs(f"{path}/{folder_name}")
    path += f"/{folder_name}"
    result = getFilesByFolderID(folder_id)
    if len(result) == 0:
        return
    result = natsorted(result, key=lambda k: k["name"])
    for item in result:
        file_id = item["id"]
        shortcut_details = item.get("shortcutDetails")
        if shortcut_details is not None:
            file_id = shortcut_details["targetId"]
            mime_type = shortcut_details["targetMimeType"]
        else:
            mime_type = item.get("mimeType")
        if mime_type == "application/vnd.google-apps.folder":
            await gDownloadFolder(file_id, path)
        else:
            await gDownloadFile(file_id, path)


# =================================================================
#    Telegram Upload Functions
# =================================================================


async def status_bar(down_msg, speed, percentage, eta, done, left, engine):
    bar_length = 12
    filled_length = int(percentage / 100 * bar_length)
    # bar = "⬢" * filled_length + "⬡" * (bar_length - filled_length)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    message = (
        f"\n╭|{bar}| » {percentage:.2f}%\n├⚡️ **Speed »** __{speed}__\n├⚙️ **Engine »** {engine}"
        + f"\n├⏳ **Esti Time »** __{eta}__"
        + f"\n├🍃 **Active Time »** __{convert_seconds((datetime.datetime.now() - task_start).seconds)}__"
        + f"\n├✅ **Processed »** __{done}__\n╰💾 **Total Size »** __{left}__"
    )
    sys_text = system_info()
    try:
        clear_output()
        print(message)
        # Edit the message with updated progress information.
        if is_time_over(current_time):
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.id,
                text=task_msg + down_msg + message + sys_text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # Opens a web URL
                                "BOT REPO 🪲",
                                url="https://github.com/XronTrix10/Telegram-Leecher",
                            ),
                        ],
                    ]
                ),
            )

    except Exception as e:
        # Catch any exceptions that might occur while editing the message.
        print(f"Error Updating Status bar: {str(e)}")


async def progress_bar(current, total):
    global start_time

    speed_string = ""
    upload_speed = 0

    if current > 0:
        elapsed_time_seconds = (datetime.datetime.now() - start_time).seconds
        upload_speed = current / elapsed_time_seconds
        speed_string = f"{size_measure(upload_speed)}/s"

    eta = (total_down_size - current - sum(up_bytes)) / upload_speed

    percentage = (current + sum(up_bytes)) / total_down_size * 100

    await status_bar(
        down_msg=text_msg,
        speed=speed_string,
        percentage=percentage,
        eta=convert_seconds(eta),
        done=size_measure(current + sum(up_bytes)),
        left=size_measure(total_down_size),
        engine="Pyrogram 💥",
    )


async def upload_file(file_path, type, file_name):
    global sent
    # Upload the file
    try:
        caption = f"<code>{file_name}</code>"

        if type == "video":
            with Image.open(thumb_path) as img:
                width, height = img.size

            data = cv2.VideoCapture(file_path)
            frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = data.get(cv2.CAP_PROP_FPS)
            seconds = 0
            if fps != 0:
                seconds = round(frames / fps)

            sent = await sent.reply_video(
                video=file_path,
                supports_streaming=True,
                width=width,
                height=height,
                caption=caption,
                thumb=thumb_path,
                duration=seconds,
                progress=progress_bar,
                reply_to_message_id=sent.id,
            )

        elif type == "audio":
            sent = await sent.reply_audio(
                audio=file_path,
                caption=caption,
                thumb=thumb_path,
                progress=progress_bar,
                reply_to_message_id=sent.id,
            )

        elif type == "document":
            sent = await sent.reply_document(
                document=file_path,
                caption=caption,
                thumb=thumb_path,
                progress=progress_bar,
                reply_to_message_id=sent.id,
            )

        elif type == "photo":
            sent = await sent.reply_photo(
                photo=file_path,
                caption=caption,
                progress=progress_bar,
                reply_to_message_id=sent.id,
            )

        clear_output()

        sent_file.append(sent)
        sent_fileName.append(file_name)
        print(f"\n{file_name} Sent !")

    except Exception as e:
        print(e)


async def Leecher(file_path):
    global text_msg, start_time, msg, sent

    file_type = get_file_type(file_path)
    file_name = os.path.basename(file_path)

    leech = await size_checker(file_path)

    if leech:  # File was splitted
        if ospath.exists(file_path):
            os.remove(file_path)  # Delete original Big Zip file
        print("Big Zip File Deleted !")
        # print('\nNow uploading multiple splitted zip files..........\n')

        dir_list = natsorted(os.listdir(temp_lpath))

        count = 1

        for dir_path in dir_list:
            short_path = os.path.join(temp_lpath, dir_path)
            file_type = get_file_type(short_path)
            file_name = os.path.basename(short_path)
            print(f"\nNow uploading {file_name}\n")
            start_time = datetime.datetime.now()
            current_time[0] = time.time()
            text_msg = f"<b>📤 UPLOADING » {count} OF {len(dir_list)} Files</b>\n\n<code>{file_name}</code>\n"
            msg = await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.id,
                text=task_msg + text_msg + "\n⏳ __Starting.....__",
            )
            await upload_file(short_path, file_type, file_name)
            up_bytes.append(os.stat(short_path).st_size)

            count += 1

        shutil.rmtree(temp_lpath)

    else:
        file_type = get_file_type(file_path)
        file_name = os.path.basename(file_path)
        print(f"\nNow uploading {file_name}\n")
        start_time = datetime.datetime.now()
        current_time[0] = time.time()
        text_msg = f"<b>📤 UPLOADING » </b>\n\n<code>{file_name}</code>\n"
        msg = await bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.id,
            text=task_msg + text_msg + "\n⏳ __Starting.....__",
        )
        await upload_file(file_path, file_type, file_name)
        up_bytes.append(os.stat(file_path).st_size)

        os.remove(file_path)


async def Leech(folder_path):
    global sent

    dump_text = (
        f"<b>📛 Name » </b>  <code>{d_name}</code>\n\n<b>📦 Size » </b> <code>{size_measure(total_down_size)}</code>"
        + f"\n\n<b>📂 Total Files » </b>  <code>{get_file_count(folder_path)}</code>\n"
    )

    sent = await bot.send_photo(chat_id=dump_id, photo=thumb_path, caption=dump_text)

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in natsorted(filenames):
            file_path = os.path.join(dirpath, f)
            print(f"\nNow uploading {os.path.basename(file_path)}\n")
            await Leecher(file_path)

    shutil.rmtree(folder_path)


async def ZipLeech(d_fol_path):
    global msg, down_msg, start_time, d_name, total_down_size, sent

    down_msg = f"<b>🔐 ZIPPING » </b>\n\n<code>{d_name}</code>\n"

    try:
        msg = await bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.id,
            text=task_msg + down_msg,
        )
    except Exception as e2:
        print(f"Problem in ZipLeech !{e2}")

    print("\nNow Zipping the folder...")
    current_time[0] = time.time()
    start_time = datetime.datetime.now()

    z_file_path = await zip_folder(d_fol_path)
    clear_output()

    total_down_size = os.stat(z_file_path).st_size

    if total_down_size > 2000 * 1024**2:
        leech_count = (total_down_size // (2000 * 1024**2)) + 1
    else:
        leech_count = 1

    dump_text = (
        f"<b>📛 Name » </b>  <code>{d_name}</code>\n\n<b>📦 Size » </b> <code>{size_measure(total_down_size)}</code>"
        + f"\n\n<b>📂 Total Files » </b>  <code>{leech_count}</code>\n"
    )

    sent = await bot.send_photo(
        chat_id=dump_id,
        photo=thumb_path,
        caption=dump_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton(
                        "BOT REPO 🪲",
                        url="https://github.com/XronTrix10/Telegram-Leecher",
                    )  # Opens a web URL
                ]
            ]
        ),
    )

    shutil.rmtree(d_fol_path)

    await Leecher(z_file_path)


async def UnzipLeech(d_fol_path):
    global msg

    down_msg = f"\n<b>📂 UNZIPPING » </b>\n\n<code>{d_name}</code>\n"

    msg = await bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg.id,
        text=task_msg + down_msg,
    )

    for dirpath, dirnames, filenames in os.walk(d_fol_path):
        for f in natsorted(filenames):
            short_path = os.path.join(dirpath, f)
            name, extension = os.path.splitext(short_path)

            if extension == ".zip":
                await extract_zip(short_path)
                clear_output()
                os.remove(short_path)
                await Leech(temp_unzip_path)

            else:
                clear_output()
                print(f"Unable to extract a {extension} file. Starting Leeching !")
                await Leecher(short_path)

    shutil.rmtree(d_fol_path)


async def FinalStep(msg):
    final_text = (
        f"<b>📂 Total Files:</b>  <code>{len(sent_file)}</code>\n\n<b>📜 LOG:</b>\n"
    )

    final_texts = []

    for i in range(len(sent_file)):
        file_link = f"https://t.me/c/{link_p}/{sent_file[i].id}"
        fileName = sent_fileName[i]
        fileText = f"\n{i+1}. <a href={file_link}>{fileName}</a>"
        if len(final_text + fileText) >= 4096:
            final_texts.append(final_text)
            final_text = fileText
        else:
            final_text += fileText
    final_texts.append(final_text)

    last_text = (
        f"<b>{task} COMPLETE 🔥</b>\n\n"
        + f"<b>📛 Name » </b>  <code>{d_name}</code>\n\n"
        + f"<b>📦 Size » </b><code>{size_measure(total_down_size)}</code>\n\n"
        + f"<b>🍃 Elapsed Time »</b> <code>{convert_seconds((datetime.datetime.now() - task_start).seconds)}</code>\n\n"
    )
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg.id,
        text=task_msg + last_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton(  # Opens a web URL
                        "BOT REPO 🦀",
                        url="https://github.com/XronTrix10/Telegram-Leecher",
                    ),
                ]
            ]
        ),
    )

    for fn_txt in final_texts:
        msg = await bot.send_message(
            chat_id=chat_id, reply_to_message_id=msg.id, text=fn_txt
        )


# ****************************************************************
#    Main Functions, function calls and variable declarations
# ****************************************************************

link_p = str(dump_id)[4:]
thumb_path = "/content/thmb.jpg"
d_path = "/content/Downloads"
d_name = ""
d_fol_path = d_path  # Initial Declaration
temp_lpath = f"{d_path}/Leeched_Files"
temp_unzip_path = f"{d_path}/Unzipped_Files"
sent_file = []
sent_fileName = []
down_bytes = []
down_bytes.append(0)
up_bytes = []
up_bytes.append(0)
current_time = []
current_time.append(time.time())
folder_info = []
folder_info.extend([0, 1])
down_count = []
down_count.append(1)
start_time = datetime.datetime.now()
text_msg = ""
links = []
link = "something"
task_msg = ""

service = build_service()

if not os.path.exists(thumb_path):
    thumb_path = "/content/Telegram-Leecher/custom_thmb.jpg"
    print("Didn't find thumbnail, So switching to default thumbnail")
if not ospath.exists(d_path):
    makedirs(d_path)


choice = input(
    "Choose the Operation: \n\t(1) Leech\n\t(2) Zipleech\n\t(3) Unzipleech\n\nEnter: "
)

if choice not in ["1", "2", "3"]:
    print("Wrong Choice ! 🦥\n")
    exit(1)

if choice == "1":
    task = "Leech"
elif choice == "2":
    task = "Zipleech"
else:
    task = "Unzipleech"

print("TASK MODE: " + task)

# Getting Download Links
while link.lower() != "c":
    link = input(f"Download link [ Enter c to Terminate]: ")
    if link.lower() != "c":
        links.append(link)

# enter the link for the file or folder that you want to download
d_name = input("Enter the name of the File/Folder: ")

task_start = datetime.datetime.now()

down_msg = f"\n<b>📥 DOWNLOADING » </b>\n"
task_msg = f"<b>🦞 TASK MODE »</b> __{task}__\n\n|  "

for a in range(len(links)):
    if "magnet" in links[a]:
        proxy_magnet = "https://mag.net/" + links[a]
        task_msg += f"<a href={proxy_magnet}>🔗 Link {a+1}</a>  |  "
    else:
        task_msg += f"<a href={links[a]}>🔗 Link {a+1}</a>  |  "
    task_msg += "\n\n"


async with Client(
    "my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token
) as bot:
    try:
        msg = await bot.send_photo(
            chat_id=chat_id,
            photo=thumb_path,
            caption=task_msg + down_msg + f"\n📝 __Calculating DOWNLOAD SIZE...__",
        )

        sent = msg
        
        for link in links:
            if "drive.google.com" in link:
                await g_DownLoad(link)
            else:
                aria2_dn = f"<b>PLEASE WAIT ⌛</b>\n\n__Getting Download Info For__\n\n<code>{link}</code>"
                try:
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=msg.id,
                        text=aria2_dn,
                    )
                except Exception as e1:
                    print(f"Couldn't Update text ! Because: {e1}")

                await aria2_Download(link)

        total_down_size = get_folder_size(d_fol_path)

        clear_output()

        if choice == "1":
            await Leech(d_fol_path)

        elif choice == "2":
            await ZipLeech(d_fol_path)

        elif choice == "3":
            await UnzipLeech(d_fol_path)

        await FinalStep(msg)

    except Exception as e:
        if "Failed to retrieve" in str(e):
            clear_output()
            print("Authorization Error with token.pickle ! Maybe file not present !")

        else:
            Error_Text = (
                "<b>TASK FAILED TO COMPLETE 💔</b>\n\n🍃 Elapsed Time: "
                + f"__{convert_seconds((datetime.datetime.now() - task_start).seconds)}__\n\n"
                + f"<b>REASEON:</b>\t\t__{e}__"
            )

            print(f"Error Occured: {e}")
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.id,
                text=task_msg + Error_Text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # Opens a web URL
                                "Report Issue 🥺",
                                url="https://github.com/XronTrix10/Telegram-Leecher/issues",
                            )
                        ],
                    ]
                ),
            )