import yt_dlp
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor


def _fetch_video_duration(video_id):
    opts = {'quiet': True, 'verbose': False, 'skip_download': True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=False
            )
            return info.get('duration') or 0
    except Exception as e:
        print(f"Failed to fetch duration for {video_id}: {e}")
        return 0


def get_playlist_duration(playlist_url, speed=1, si=1, ei=5000):
    try:
        ydl_opts = {
            'quiet': True,
            'verbose': False,
            'extract_flat': True,
        }
        si_gt_tot_vids_flg = False
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)

        id = result.get('id')
        title = result.get('title')
        entries = [e for e in (result.get('entries') or []) if e]

        total_vids = result.get('playlist_count') or len(entries)
        if total_vids < si:
            si = 1
            si_gt_tot_vids_flg = True

        entries = entries[si - 1:ei]

        total_duration = 0
        missing_ids = []
        for video in entries:
            d = video.get('duration')
            if d:
                total_duration += d
            elif video.get('id'):
                missing_ids.append(video['id'])

        if missing_ids:
            with ThreadPoolExecutor(max_workers=8) as pool:
                total_duration += sum(pool.map(_fetch_video_duration, missing_ids))

        original_duration = str(timedelta(seconds=int(total_duration)))
        total_duration = total_duration / speed
        formatted_duration = str(timedelta(seconds=int(total_duration)))
        return formatted_duration, total_duration, id, title, original_duration, si_gt_tot_vids_flg
    except Exception as e:
        print(f"get_playlist_duration failed: {e}")
        return "Invalid Playlist Link", None, None, None, None, None

def calculate_pomodoro_sessions(duration_seconds):
    partial_pomodoro_session = False
    study_time = 25 * 60  # 25 minutes of study
    break_time = 5 * 60   # 5 minutes of break
    total_time_per_pomodoro = study_time + break_time

    full_sessions = duration_seconds // study_time
    remainder = duration_seconds % study_time

    if duration_seconds <= study_time:
        return 1, duration_seconds, partial_pomodoro_session

    if remainder > 0:
        partial_pomodoro_session = True
        full_sessions += 1
    total_pomodoro_time = full_sessions * total_time_per_pomodoro
    return full_sessions, total_pomodoro_time, partial_pomodoro_session