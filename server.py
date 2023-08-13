from flask import Flask, render_template, request, redirect, session
from yt_dlp import YoutubeDL
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
                ydl_opts = {'format': 'best'}
                with YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=False)
                    download_link = info_dict['url']
                    video_title = info_dict['title']

                session['download_link'] = download_link

                return render_template("download.html", video_title=video_title)
            else:
                return redirect('/')
        except Exception as e:
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
    app.run()
