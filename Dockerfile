FROM phusion/baseimage:0.9.22
# basics
RUN apt-get update
# image processing libraries
# vieo processing libraries
# GUI operations for OpenCV
# optimization libraries
RUN apt-get install build-essential cmake pkg-config \
    libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev \
    libgtk-3-dev \
    libatlas-base-dev gfortran \
    unzip wget -y
# Python
RUN apt-get install python2.7-dev python3.5-dev -y && apt-get install python3-pip -y
RUN pip3 install numpy
# Download OpenCV
RUN wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.2.0.zip
RUN unzip opencv.zip
WORKDIR opencv-3.2.0
RUN mkdir build
WORKDIR build
RUN cmake -D WITH_TBB=ON \
    -D WITH_OPENMP=ON \
    -D WITH_IPP=ON \
    -D CMAKE_BUILD_TYPE=RELEASE \
    -D BUILD_EXAMPLES=OFF \
    -D WITH_NVCUVID=ON \
    -D WITH_CUDA=ON \
    -D BUILD_DOCS=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D BUILD_TESTS=OFF \
    -D WITH_CSTRIPES=ON \
    -D WITH_OPENCL=ON CMAKE_INSTALL_PREFIX=/usr/local/ ..
# RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
#     -D CMAKE_INSTALL_PREFIX=/usr/local \
#     -D INSTALL_PYTHON_EXAMPLES=ON \
#     -D INSTALL_C_EXAMPLES=OFF \
#     -D PYTHON_EXECUTABLE=/usr/bin/python3 \
#     -D BUILD_EXAMPLES=ON ..
# Install OpenCV
RUN make && make install
RUN ldconfig
RUN cd ../.. && rm -r opencv.zip opencv-3.2.0
RUN apt-get clean && apt-get autoremove
# Setup installation to work with Python
WORKDIR /usr/local/lib/python3.5/dist-packages/
RUN mv cv2.cpython-35m-x86_64-linux-gnu.so cv2.so
