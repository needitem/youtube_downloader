#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. AI시대, 필요한 인재 (14:43~16:45)
https://youtu.be/zQsaJJPlNps?si=H-d-7eDbMvtInw4m

2. 자기 주도성 (1:28~2:45)
https://youtu.be/o9gaQf_JfvE?si=-TcyBFvs_oRtz7wl

3. 우분트
https://youtu.be/3cm5pTBfgIg?feature=shared

4. 기후위기 환경
https://www.youtube.com/watch?v=vvgrdmjP1_g

5. 오일전사(편집본)
http://naver.me/GwpBqgA8
"""

from yt_dlp import YoutubeDL
import re
from moviepy.video.io.VideoFileClip import VideoFileClip
import tkinter as tk
from tkinter import simpledialog

def _parse_time_str(time_str):
    """'14:43' 형태의 문자열을 초 단위 정수로 변환합니다."""
    mins, secs = time_str.split(':')
    return int(mins) * 60 + int(secs)

def download_all_from_docstring():
    # __doc__를 통해 docstring(아래 주석) 내용을 불러옵니다.
    lines = __doc__.strip().splitlines()
    i = 0
    while i < len(lines):
        title_line = lines[i].strip()
        if not title_line:
            i += 1
            continue

        # 다음 줄(링크)을 확인, 없으면 중단
        if i + 1 >= len(lines):
            break
        link_line = lines[i + 1].strip()

        # (mm:ss~mm:ss) 구조 파악
        match = re.search(r"\((\d{1,2}:\d{2})~(\d{1,2}:\d{2})\)", title_line)
        start_sec, end_sec = None, None
        if match:
            start_sec = _parse_time_str(match.group(1))
            end_sec   = _parse_time_str(match.group(2))

        # 괄호 앞부분을 제목으로 삼음
        if '(' in title_line:
            title = title_line.split('(')[0].strip()
        else:
            title = title_line

        # 유튜브 링크가 아니면 건너뜀
        if 'youtu' not in link_line:
            print(f"Skipping non-YouTube link: {link_line}")
            i += 2
            continue

        print(f"Downloading: {title} ({link_line})")

        # yt-dlp 기본 옵션 설정
        ydl_opts = {
            "format": "mp4/bestaudio/best",
            "outtmpl": f"{title}.%(ext)s"  # 출력 파일명 템플릿
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([link_line])
        downloaded_path = f"{title}.mp4"  # yt-dlp가 mp4인지 여부에 따라 조정

        # 특정 구간만 잘라내기
        if start_sec is not None and end_sec is not None:
            cut_filename = f"{title}_cut.mp4"
            with VideoFileClip(downloaded_path) as video:
                cut_clip = video.subclip(start_sec, end_sec)
                cut_clip.write_videofile(cut_filename, codec="libx264")
            print(f"Partial saved: {cut_filename}")
        else:
            print("Downloaded full video.")

        i += 2

if __name__ == "__main__":
    download_all_from_docstring()
