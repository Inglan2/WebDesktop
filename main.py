import os


def cls():
    os.system("clear")


cls()

print("Installing...")

os.system("pip install docker flask textual pyloaders > /dev/null")

print("Installed")
print("Importing...")

import docker, time, webbrowser, subprocess, threading
from flask import Flask, render_template
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Label
from loaders import BarLoader

print("Imported")
print("Create server")

app = Flask(__name__)

serverthread = threading.Thread(
    target=lambda: app.run(host="0.0.0.0", port=6969, debug=False, use_reloader=False)
)

serverthread.daemon = True

print("Server created")
print("Create Textual App")


class WebDesktop(App):
    CSS = """
    Screen {
        align: center middle;
    }

    .bigbtn {
        margin: 1;
        align: center middle;
        width: 69
    }
    """

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "open":
            webbrowser.open("http://localhost:6969")
        elif event.button.id == "stop":
            exit()

    def compose(self) -> ComposeResult:
        yield Label("WebDesktop is running")
        yield Button("Open", id="open", variant="success", classes="bigbtn")
        yield Button("Stop", id="stop", variant="error", classes="bigbtn")


print("Created Textual App")
print("Init docker")

client = docker.from_env()

cls()

print("Pull container")
print("This may take a while")
loader = BarLoader(complete_text="Pulled container")
loader.start()

client.images.pull("lscr.io/linuxserver/webtop:ubuntu-kde")

loader.stop()


def resetContainer():
    try:
        client.containers.list()[0].stop()
    except:
        pass
    try:
        client.containers.list()[0].remove()
    except:
        pass
    client.containers.prune()
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


print("Installing container")

if not os.path.exists("/workspace/WebDesktop/files"):
    resetContainer()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    resetContainer()
    serverthread.start()
    txapp = WebDesktop()
    txapp.run()
