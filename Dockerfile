FROM andreasnel/opencv-source:latest
WORKDIR /app
EXPOSE 5000
RUN apt-get install -y libzbar0 libzbar-dev
RUN pip3 install virtualenv
RUN virtualenv -p python3 venv
RUN /bin/bash -c "source venv/bin/activate"
RUN pip3 install pyzbar==0.1.4 pyzbar[scripts] zbar-py==1.0.4
ADD requirements.txt .
RUN apt-get install -y libboost-all-dev
RUN pip3 install -r requirements.txt
RUN apt-get install -y tesseract-ocr
ADD 301Cert/javathehutts_me.crt /etc/ssl/certs/javathehutts/javathehutts_me.crt
ADD 301Cert/javathehutts_me.key /etc/ssl/certs/javathehutts/javathehutts_me.key
ADD 301Cert/javathehutts_me.p7b /etc/ssl/certs/javathehutts/javathehutts_me.p7b
ADD 301Cert/javathehutts_me.ca-bundle /etc/ssl/certs/javathehutts/javathehutts_me.ca-bundle
ADD target/dist/Java-the-Hutts-1.0.dev0/ /app
RUN python3 setup.py install
CMD [ "python3", "scripts/run.py" ]
