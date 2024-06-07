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

if __name__ == "__main__":
    subprocess.Popen(["gp", "preview", "http://localhost:8000/embed"])
    app.run(port=8000)
