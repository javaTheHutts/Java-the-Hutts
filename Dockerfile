FROM andreasnel/opencv-source:latest
WORKDIR /app
ADD target/dist/Java-the-Hutts-1.0.dev0/ /app
EXPOSE 5000
RUN apt-get install -y libzbar0 libzbar-dev
RUN pip3 install virtualenv
RUN virtualenv -p python3 venv
RUN /bin/bash -c "source venv/bin/activate"
RUN pip3 install pyzbar==0.1.4 pyzbar[scripts] zbar-py==1.0.4
ADD requirements.txt .
RUN apt-get install -y libboost-all-dev
RUN pip3 install -r requirements.txt
RUN python3 setup.py install
# CMD [ "python3", "scripts/run.py" ]
