from flask import Flask, render_template, request, redirect, session
from pytube.exceptions import RegexMatchError, VideoUnavailable
from pytube import YouTube
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/search', methods=['POST', 'GET'])
def search_video():
    if request.method == 'POST':
        video_url = request.form['videoURL']
        try:
            if video_url:
                yt = YouTube(video_url)
                video_stream = yt.streams.get_highest_resolution()
                download_link = video_stream.url
                video_title = yt.title

                session['download_link'] = download_link

                return render_template("download.html", video_title=video_title)
            else:
                return redirect('/')
        except (RegexMatchError, VideoUnavailable):
            video_title = "Please, Insert a Valid URL."
            return render_template('error.html', video_title=video_title)
    else:
        return redirect('/')


@app.route('/download', methods=['POST', 'GET'])
def download_video():
    download_link = session.get('download_link')
    if download_link:
        return redirect(download_link)
    else:
        return redirect('/')

@app.route("/about_us")
def about_page():
    return render_template("about.html")

@app.route("/policy")
def policy_page():
    return render_template("privacy.html")

@app.route("/terms")
def terms_of_use_page():
    return render_template("terms.html")


if __name__ == '__main__':
    app.run(debug=True)
