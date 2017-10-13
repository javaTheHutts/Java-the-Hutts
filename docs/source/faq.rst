Frequently Asked Questions
==========================

Can Hutts Verification extract data from a passport?
----------------------------------------------------
No, at this stage in development the system can only extract data from a South African
ID card, ID book and student card from the University of Pretoria.
We do plan on adding this feature in the future, however.

Can Hutts Verification extract data from a driver's license?
------------------------------------------------------------
No, at this stage in development the system can only extract data from a South African
ID card, ID book and student card from the University of Pretoria.

A South African driver's license is especially difficult to work with, due to the
watermarks present on the lamination and the extremely poor quality font that is used
on the document.

Why does some processes take longer than others?
------------------------------------------------
This can be due to a number of reasons. They may include:

- The larger the picture that is uploaded, the longer it takes the system to process the image.
- The system cannot identify the documentation type and cannot work with optimized parameters, therefore making use of default processing mechanisms.
- The network speed is slow. This affects the uploading and downloading of files.
- If you are running the server on your local computer, the hardware that is present on your computer has a large impact on the maximum potential of the system.
- The busier the background, the more data the system has to scan through in order to extract the correct data, which can lead to speed issues.
- Lower quality images also tend to take longer than higher quality images, due to the system having to try and take a best guess effort to determine what kind of data is extracted.

Why is the Docker image so large?
---------------------------------
This is due to the large number of libraries that are used to process an image in the Hutts Verification system.
OpenCV, which is the backbone of our system, is already a very large installation inside its own Docker container.
The Hutts Verification container builds on top of that container, and therefore the size of the final Docker image
is extremely large due to the large number of dependencies.

Why do some types of documentation work better than others?
-----------------------------------------------------------
Each type of documentation looks different to another. This means that some types of documentation are easier to process than others, leading to a speed increase.
