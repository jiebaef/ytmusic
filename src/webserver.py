from flask import Flask, render_template, redirect, url_for, session, request
from flask_bootstrap import Bootstrap

from youtube import YouTubeApi
from videoplayer import VideoPlayer

api = YouTubeApi()
player = VideoPlayer()

users = {
    "admin": {
        "username": "admin",
        "password": "Finn12470"
    }
}
host =  {"localhost": "127.0.0.1", "networkhost": "0.0.0.0"}
class Webserver():
    app = Flask(__name__, static_url_path='/static', template_folder='templates')
    Bootstrap(app)

    def __init__(self, playlist):
        player.init(playlist)
        
# sites
    @app.route('/')
    @app.route('/index')
    def index(self = None):
        return render_template('index.html')

    @app.route('/admin')
    def admin(self = None):
        if not session.get("USERNAME") is None:
            username = session.get("USERNAME")
            user = users[username]
            return render_template("admin.html", user=user)
        else:
            print("No username found in session")
            return redirect(url_for("index"))

# admin dashboard actions
    @app.route('/startSelenium')
    def startSelenium(self = None):
        if not player.started():
            player.startPlaylist()
        else:
            print("player has been started already")
        return ("")

    @app.route('/pausePlay')
    def pauseplay(self = None):
        player.pauseplay()
        return ("")
    
    @app.route('/skipSong')
    def skipSong(self = None):
        player.nextSong()
        return ("")

# form actions
    @app.route('/search', methods=["POST"])
    def search(self=None):
        if request.method == "POST":
            req = request.form

            query = req.get('query')

            videos = api.getYoutubeVideos(query)
            data = {
                "videos": videos
            }
            return render_template('results.html', **data)
    
    @app.route('/add', methods=["POST"])
    def add(self=None):
        if request.method == "POST":
            req = request.form
            
            videoId = req.get("videoId")

            api.addVideoToPlaylist(videoId)

        return redirect(url_for('index'))

# Session and login stuff
    @app.route('/login')
    def login(self = None):
        return render_template('login.html')
    
    @app.route('/sign-in', methods=["POST"])
    def sign_in(self = None):
        if request.method == "POST":
    
            req = request.form

            username = req.get("username")
            password = req.get("password")

            # mocked db
            if not username in users:
                print("Username not found")
                return redirect(request.url)
            else:
                user = users[username]

            # test if user is correctly logged in
            if not password == user["password"]:
                print("Incorrect password")
                return redirect(request.url)
            else:
                session["USERNAME"] = user["username"]
                print("session username set")
                return redirect(url_for("admin"))

        return redirect(url_for("index"))

    @app.route('/logout')
    def logout(self = None):
        session.pop("USERNAME", None)
        return redirect(url_for("index"))
    
# run webserver method
    def run(self):
        self.app.config["SECRET_KEY"] = "tOvjjy_Ladh_D9OlHxZjWg"
        self.app.run(host=host["networkhost"], port=8080)
