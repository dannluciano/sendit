FROM ubuntu:24.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    # Tools
    build-essential \
    tmux \
    htop \
    btop \
    tree \
    curl \
    wget \
    httpie \
    git \
    openssh-client \
    # Program Languages Runtimes
    nodejs \
    npm \
    python3 \
    python3-pip \
    python3-venv \
    openjdk-21-jdk-headless \
    php-cli \
    # Database
    sqlite3 \
    # Editors
    nano \
    vim \
    emacs \
    # TUI
    neofetch \
    nyancat \
    cmatrix \
    # Remove APT CACHE
    && rm -rf /var/lib/apt/lists/*

COPY ./bin/ /usr/local/bin

ENV PORT=8080
ENV HOST=0.0.0.0
ENV PIP_BREAK_SYSTEM_PACKAGES=1

CMD ["bash"]