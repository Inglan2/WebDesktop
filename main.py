import os

os.system("pip install docker")

import docker, time

client = docker.from_env()

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

input()

client.containers.list()[0].stop()
client.containers.list()[0].remove()