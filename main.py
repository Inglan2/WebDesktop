import os

os.system("pip install docker flask")

import docker, time, webbrowser, subprocess
from flask import Flask, render_template

app = Flask(__name__)

client = docker.from_env()

client.images.pull("lscr.io/linuxserver/webtop:ubuntu-kde")


def resetContainer():
    try:
        client.containers.list()[0].stop()
        client.containers.list()[0].remove()
    except:
        pass

    client.containers.run(
        "lscr.io/linuxserver/webtop:ubuntu-kde",
        detach=True,
        name="webdesktop",
        security_opt=["seccomp:unconfined"],
        environment=[
            "PUID=1000",
            "PGID=1000",
            "TZ=Etc/UTC",
            "SUBFOLDER=/",
            "TITLE=WebDesktop",
        ],
        volumes=["/workspace/WebDesktop/files:/config"],
        ports={"3000": "3000"},
    )

@app.route("/")
def index():
    return "home"

@app.route("/embed")
def embed():
    return """
    <style>
        * {
            width: 100%;
            height: 100%;
            padding: 0;
            margin: 0;
            background-color: #1F1F1F;
            color: white;
            font-size: 30px;
            outline: 0;
            border: 0;
            cursor: pointer;
        }
    </style>
    <button onclick="window.open('/')">Open</button>
    """

if __name__ == "__main__":
    subprocess.Popen(["sleep 5 && gp preview http://localhost:8000/embed"], shell=True)
    app.run(port=8000)
