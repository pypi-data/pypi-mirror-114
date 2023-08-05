FROM docker.io/archlinux

MAINTAINER Portmod

USER root
RUN yes | pacman -Sy rustup bubblewrap python python-pip git gcc make patch python-virtualenv unzip pandoc pkgconf
RUN rustup toolchain install stable
RUN rustup component add clippy
RUN rustup component add rustfmt
RUN yes | pacman -S icu which wget
