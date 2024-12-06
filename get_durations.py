import yt_dlp
from datetime import timedelta

def get_video_duration(url, speed=1):
    try:
        ydl_opts = {
            # 'cookiefile': "cookies.txt",
            'quiet': False,
            'verbose': True,
            'extract_flat': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            duration = info_dict.get('duration', None)
            original_duration = None
            id = info_dict.get('id', None)
            title = info_dict.get('title', None)
            if duration is not None:
                original_duration = str(timedelta(seconds=int(duration)))
                duration = duration / speed
                formatted_duration = str(timedelta(seconds=int(duration)))
                return formatted_duration, duration, id, title, original_duration
            else:
                return "Duration not available.", None, None, None, None
    except Exception as e:
        return f"Invalid Video Link", None, None, None, None


def get_playlist_duration(playlist_url, speed=1, si=1, ei=5000):
    try:
        ydl_opts = {
            # 'cookiefile': "cookies.txt",
            'quiet': False,
            'verbose': True,
            'extract_flat': True,
        }
        si_gt_tot_vids_flg = False
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
            id = result.get('id', None)
            total_vids = result.get('playlist_count', None)
            if total_vids < si:
                si = 1
                si_gt_tot_vids_flg = True
            title = result.get('title', None)
            total_duration = 0
            entries = result['entries'][si - 1:ei]
            for video in entries:
                if 'duration' in video:
                    total_duration += video['duration']
            original_duration = str(timedelta(seconds=int(total_duration)))
            total_duration = total_duration / speed
            formatted_duration = str(timedelta(seconds=int(total_duration)))
            return formatted_duration, total_duration, id, title, original_duration, si_gt_tot_vids_flg
    except Exception as e:
        return f"Invalid Playlist Link", None, None, None, None, None


def calculate_pomodoro_sessions(duration_seconds):
    study_time = 25 * 60  # 25 minutes of study
    break_time = 5 * 60   # 5 minutes of break
    total_time_per_pomodoro = study_time + break_time

    full_sessions = duration_seconds // study_time
    remainder = duration_seconds % study_time

    if duration_seconds <= study_time:
        return 1, duration_seconds

    if remainder > 0:
        full_sessions += 1
    
    total_pomodoro_time = full_sessions * total_time_per_pomodoro
    
    return full_sessions, total_pomodoro_time