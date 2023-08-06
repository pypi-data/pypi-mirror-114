import argparse
import asyncio
import concurrent.futures

from functools import partial
from pathlib import Path

from tqdm import tqdm
import cv2

__all__ = ["VideoFrame", "one_video", "many_videos"]


VIDEO_SUFFIX = [".mp4", ".3gp", ".avi"]


class VideoFrame:
    def __new__(cls, *args, **kwargs):
        self = cls._from_parts(*args, **kwargs)
        return self

    @classmethod
    def _from_parts(cls, *args, **kwargs):
        self = object.__new__(cls)
        self.filename, self.stride = cls._parse_args(*args, **kwargs)
        self._init()
        return self

    def _init(self):
        self._video = cv2.VideoCapture(self.filename)
        self.video_len = int(self._video.get(cv2.CAP_PROP_FRAME_COUNT))

    @classmethod
    def _parse_args(cls, *args, **kwargs):
        args_cnt = len(args)
        if args_cnt == 1:
            filename = args[0]
            stride = 1
        elif args_cnt == 2:
            filename, stride = args

        filename, stride = kwargs.get("filename", filename), kwargs.get(
            "stride", stride
        )
        return filename, stride

    def __init__(self, filename: str, stride: int = 1):
        self._pos_frame = -1

    @property
    def pos_frame(self):
        # Real Pos
        return self._pos_frame + 1

    def __len__(self):
        return self.video_len

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            rat, frame = self._video.read()
            if rat:
                self._pos_frame += 1
                if self._stride(self._pos_frame):
                    return frame
            else:
                raise StopIteration

    def __getitem__(self, idx):
        self._video.set(cv2.CAP_PROP_POS_FRAMES, idx)
        rat, frame = self._video.read()
        self._video.set(cv2.CAP_PROP_POS_FRAMES, self._pos_frame)
        if rat:
            return frame
        else:
            IndexError

    def _stride(self, frame_num):
        return frame_num % self.stride == 0


async def make_image(video_dir, frame, frame_num):
    video_dir = Path(video_dir)
    image_path = (
        video_dir.parent / video_dir.stem / f"{video_dir.stem}_{int(frame_num)}.jpg"
    )
    loop = asyncio.get_event_loop()
    imwrite_func = partial(cv2.imwrite, str(image_path), frame)
    with concurrent.futures.ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, imwrite_func)


async def one_video(video_path, stride):
    video_frames = VideoFrame(video_path, stride)
    try:
        await asyncio.wait(
            [
                make_image(video_path, frame, video_frames.pos_frame)
                for frame in video_frames
            ]
        )
    except:
        return


async def many_videos(video_paths, stride):
    for video in tqdm(video_paths):
        await one_video(video, stride)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path of file or folder", type=str)
    parser.add_argument(
        "stride",
        help="Stride Frames",
        type=int,
    )
    loop = asyncio.get_event_loop()

    args = parser.parse_args()

    if Path(args.path).is_dir():
        videos = [
            video for video in Path(args.path).glob("*") if video.suffix in VIDEO_SUFFIX
        ]
        for video in videos:
            video.with_suffix("").mkdir(exist_ok=True)
        loop.run_until_complete(many_videos(videos, args.stride))
    else:
        Path(args.path).with_suffix("").mkdir(exist_ok=True)
        loop.run_until_complete(one_video(args.path, args.stride))


if __name__ == "__main__":
    video_frame = VideoFrame("test.mp4", 5)
    frames = list(video_frame)
