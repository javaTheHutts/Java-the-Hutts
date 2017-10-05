FROM bash:4.4
# basics
RUN apt-get update
RUN apt-get install build-essential cmake pkg-config -y
# image processing libraries
RUN sudo apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev -y
# vieo processing libraries
RUN sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
RUN sudo apt-get install libxvidcore-dev libx264-dev -y
# GUI operations for OpenCV
RUN sudo apt-get install libgtk-3-dev -y
# optimization libraries
RUN sudo apt-get install libatlas-base-dev gfortran -y
# Python
RUN sudo apt-get install python2.7-dev python3.5-dev -y
# Download OpenCV
WORKDIR ~
RUN wget -0 opencv.zip https://github.com/Itseez/opencv/archive/3.2.0.zip
RUN unzip opencv.zip
# Get pip
RUN apt-get install python3-pip -y
# Install dependencies for OpenCV
RUN pip3 install numpy
# Compile OpenCV
WORKDIR ~/opencv-3.2.0
RUN mkdir build
WORKDIR ~/opencv-3.2.0/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D PYTHON_EXECUTABLE=/usr/bin/python3 \
    -D BUILD_EXAMPLES=ON ..
RUN make
# Install OpenCV
RUN make install
RUN ldconfig
# Setup installation to work with Python
WORKDIR /usr/local/lib/python3.5/site-packages/
RUN mv cv2.cpython-35m-x86_64-linux-gnu.so cv2.so
