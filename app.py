from flask import Flask, render_template, request
from flask_cors import CORS
from datetime import timedelta
from get_durations import get_playlist_duration, calculate_pomodoro_sessions

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"].strip()
        speed = float(request.form["speed"])
        si = ei = original_duration = None
        
        # print(url)
        if "playlist?list" in url:
            si = int(request.form["start_index"])
            ei = int(request.form["end_index"])
            formatted_duration, total_duration, id, title, original_duration, flg = get_playlist_duration(url, speed, si, ei)
            if flg:
                si = 1
        # elif "watch?v" in url or "youtu.be/" in url:
            # formatted_duration, total_duration, id, title, original_duration = get_video_duration(url, speed)
        else:
            formatted_duration = "Invalid URL"
            total_duration = None
        
        if total_duration is not None:
            pomodoro_sessions, pomodoro_time, partial_pomodoro_session = calculate_pomodoro_sessions(total_duration)

            
            if partial_pomodoro_session:
                pomodoro_time = pomodoro_time - 1800 + ((total_duration - ((pomodoro_sessions - 1)*1500)) % 1500)
                # total_pomodoro_time = total_pomodoro_time - 1800 + ((total_duration - (pomodoro_sessions - 1)*25) % 25)

            total_pomodoro_time = pomodoro_time + (int(pomodoro_sessions) // 4) * 3600
            if pomodoro_sessions % 4 == 0:
                total_pomodoro_time -= 3600

            pomodoro_time = str(timedelta(seconds=int(pomodoro_time)))
            total_pomodoro_time = str(timedelta(seconds=int(total_pomodoro_time)))

            if pomodoro_sessions <= 4:
                total_pomodoro_time = pomodoro_time

        else:
            pomodoro_sessions = pomodoro_time = total_pomodoro_time = id = title = None

        return render_template("index.html", duration=formatted_duration,
                               pomodoro_sessions=pomodoro_sessions,
                               pomodoro_time=pomodoro_time,
                               total_pomodoro_time=total_pomodoro_time,
                               id=id,
                               title=title,
                               start_index=si,
                               end_index=ei,
                               original_duration=original_duration)

    return render_template("index.html", duration=None,
                           pomodoro_sessions=None,
                           pomodoro_time=None)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)