FROM nvcr.io/nvidia/pytorch:21.05-py3

ARG UNAME=vscode
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID $UNAME
RUN useradd -m -u $UID -g $GID -s /bin/bash $UNAME

ENV PATH="${PATH}:/home/vscode/.local/bin"

USER $UNAME