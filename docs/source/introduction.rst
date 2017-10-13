Introduction
============
Hutts Verification is a Web API that performs electronic ID extraction and verification. The primary purpose of the system
is to reduce the time that it takes to manually capture a user's personal information by automatically extracting it
from the person's official identification documentation. This information includes both the facial and the textual data
that is evident on such documentation. The system can then also use this extracted information to compare it to
data that it is provided with in order to give a percentage match of the two sets of data.

Due to the main target market of Hutts Verification being developers, the system is designed as an easily pluggable
API for any Python-based system. A server and a graphical interface is also provided so that a user can experiment
with the system in a clean and simple manner without needing any previous development experience.

At this stage of development, the system is configured to only work with South African ID cards and books as well as student cards
from the University of Pretoria. It is, however, possible to add a template for another type of documentation to the system.
