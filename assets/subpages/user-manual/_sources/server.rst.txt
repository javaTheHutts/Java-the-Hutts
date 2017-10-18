Using the Server
================
This section deals on how to make requests to the built-in server that a user can run when Hutts Verification
has been installed.

.. note: This section assumes that you have already followed the instructions on how to install Hutts Verification
            and that you know how to run it.

All requests to the server should be made by making use of the ``POST`` method as well as setting the
MIME-type of the data to ``application/json`` (of course, this also implies that the data of the request should
be in JSON) in order to correctly send requests to and receive responses from the server.

.. note: All request can have certain fields appended to them in order to make use of other image processing
            techniques when performing extraction or verification. These fields are:
            ``remove_barcode``,
            ``remove_face``,
            ``threshold_technique`` and
            ``blur_technique``.

Extraction
----------

**Extract All**
This request extracts both the textual and the facial data from the ID document.

URL: http://localhost:5000/extractAll.

Sample Data::

    {
        "idPhoto": "data:image/jpeg;base64,/9j/4QTDRXh......"
    }

Response::

    {
        "extracted_face": "data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...",
        "text_extract_result": {
            "country_of_birth": <string>, 
            "date_of_birth": <string>, 
            "identity_number": <string>, 
            "names": <string>, 
            "sex": <string>, 
            "status": <string>, 
            "surname": <string>
        }
    }

**Extract Text**
This request only extracts the textual data from the ID document.

URL: http://localhost:5000/extractText.

Sample Data::

    {
        "idPhoto": "data:image/jpeg;base64,/9j/4QTDRXh..."
    }

Response::

    {
        "country_of_birth": <string>, 
        "date_of_birth": <string>, 
        "identity_number": <string>, 
        "names": <string>, 
        "sex": <string>, 
        "status": <string>, 
        "surname": <string>
    }

**Extract Face**
This request only extracts the image of the person's face from the ID document.

URL: http://localhost:5000/extractFace.

Sample Data::

    {
        "idPhoto": "data:image/jpeg;base64,/9j/4QTDRXh..."
    }

Response::

    {
        "extracted_face": "data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
    }

Verification
------------

**Verify ID**
This request verifies an image (containing a face) and provided textual information against the information that
can be extracted from an image of the relevant identification documentation (which should also be provided).4

URL: http://localhost:5000/verifyID.

Sample Data::

    {
        cob: <country of birth string>,
        dob: <date of birth string>,
        face_img: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...",
        gender: <gender string>,
        idNumber: <ID number string>,
        id_img: "data: image/jpeg;base64,/9j/4QTDRXhpZgAA...",
        names: <name string>,
        nationality: <nationality string>,
        status: <citizenship status string>,
        surname: <surname string>,
        verbose_verify: false,
        verification_threshold: 75
    }

Response::

    {
        "face_match": 84.15386465700645, 
        "is_match": true, 
        "is_pass": false, 
        "text_match": 14.29, 
        "total_match": 56.20831879420387
    }
