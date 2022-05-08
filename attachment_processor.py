import temp
import utils
import os
import requests
import process_video
from ffmpeg import FFmpeg

def process_attachment(attachment, accept):
    url = attachment.url
    split_url = url.split("/")
    file_name = split_url[len(split_url) - 1]
    split_name = utils.split_name(file_name)
    for ex in accept:
        if split_name[1] == ex:
            return next(attachment, split_name[0], split_name[1], file_name)

    raise Exception("Invalid file!")

async def next(attachment, name, ex, full_name):
    response = requests.get(attachment.url, allow_redirects=True)
    temp_dir = temp.create_temp_directory(name, True)
    download = temp.create_temp_directory(name + os.path.sep + "download", True)
    temp_path = download + os.path.sep + full_name
    open(temp_path, 'wb').write(response.content)

    output_video = process_video.process_video(temp_dir, (name, ex, full_name))

    input_video = temp_dir + os.path.sep + "download" + os.path.sep + full_name

    merged = temp.create_temp_directory(name + os.path.sep + "merged", True)
    render_video = merged + os.path.sep + full_name

    ffmpeg = FFmpeg().option('y').input(
        output_video,
        an=None,
    ).input(
        input_video,
        vn=None,
    ).output(
        render_video, {
        "-c:a": "copy",
        "-c:v": "libvpx-vp9"
        }, 
    )
    await ffmpeg.execute()
    return [render_video, name]


