# Simple Flutter web development server
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV FLUTTER_VERSION=3.24.0
ENV FLUTTER_HOME=/opt/flutter
ENV PATH=$PATH:$FLUTTER_HOME/bin
ENV API_BASE_URL=http://backend:5000
ENV CHROME_EXECUTABLE=/usr/bin/chromium-browser

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    xz-utils \
    zip \
    libglu1-mesa \
    wget \
    ca-certificates \
    chromium-browser \
    chromium-codecs-ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Flutter
RUN wget -O flutter.tar.xz https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz \
    && mkdir -p $FLUTTER_HOME \
    && tar xf flutter.tar.xz -C $FLUTTER_HOME --strip-components=1 \
    && rm flutter.tar.xz

# Fix git ownership issues
RUN git config --global --add safe.directory /opt/flutter

# Create a non-root user
RUN useradd -m -s /bin/bash flutter && \
    chown -R flutter:flutter /opt/flutter

# Set working directory
WORKDIR /app

# Copy pubspec files
COPY pubspec.yaml pubspec.lock ./

# Change ownership to flutter user
RUN chown -R flutter:flutter /app

# Switch to flutter user
USER flutter

RUN /bin/sh -c flutter pub get

# If you get an conflict for sdk you can remove these comment lines
# RUN /bin/sh -c flutter pub outdatedd
# RUN /bin/sh -c flutter pub upgrade --major-versions
# Copy source code
COPY --chown=flutter:flutter . .

# Enable web support
RUN flutter config --enable-web

# Expose port
EXPOSE 3000

# Start Flutter web development server
CMD ["flutter", "run", "-d", "web-server", "--web-port", "3000", "--web-hostname", "0.0.0.0"]
