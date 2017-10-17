Installing from Source Code
===========================
Hutts Verification can also be installed completely from the source code available at `<https://github.com/javaTheHutts/Java-the-Hutts>`_

**NOTE:** This installation may take anything from 30 minutes to 3 hours, depending on which requirements have already been installed on the user's computer.

1. Install OpenCV 3.2.0, Python3 and all virtual environments as explained `here <https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/>`_. Please note that the version in the tutorial is different from the required version (3.2.0).
2. Clone the repository for the source code with ``git clone https://github.com/javaTheHutts/Java-the-Hutts.git``
3. Run the following commands after the successful installation and linking of OpenCV to your virtual environment::

    sudo apt-get install -y libzbar0 libzbar-dev libboost-all-dev tesseract-ocr

4. Run the following commands while your OpenCV virtual environment is activated (this installs all the dependencies of the project)::

    pip3 install pybuilder
    pip3 install pyzbar==0.1.4 pyzbar[scripts] zbar-py==1.0.4
    pip3 install -r requirements.txt
    pyb install_dependencies

5. Install the project with the following commands::

    pyb analyze full publish
    cd target/dist/Java-the-Hutts-1.0.dev0/
    python3 setup.py install

6. In order to test whether the installation was successful, the user should be able to execute the ``import hutts_verification`` statement in any Python 3 shell without error.
