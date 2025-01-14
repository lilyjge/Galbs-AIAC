# Galbs-AIAC

## About

The Artificially Intelligent and Automated Companion, Galbs, is a functional companion capable of engaging in conversation and providing high-availability emotional support to a wide audience of users. Using a camera, microphone, and speaker, Galbs is capable of analyzing and interpreting visual and auditory data highly effectively–generating appropriate responses using modern machine learning technologies. Additionally, Galbs can detect a person's presence and accurately determine their mood to advise responses. The companion is equipped with adaptable and customizable personalities, to suit the needs of each individual user. Galbs incorporates small gestures into its speech, bringing more life to the companion.

Read more about the project in our [report](https://docs.google.com/document/d/1PVMq5yzujTvwzG0pw4Gjc-sdwjeTVPDN7BOnSVzINY8/edit?usp=sharing).

This project utilizes Llama 3 of Meta Platforms, Inc.; in particular, "Llama 3 is licensed under the LLAMA 3 Community License, Copyright © Meta Platforms, Inc. All Rights Reserved."

Link: [https://www.llama.com/license/](https://www.llama.com/license/)

## Setup and Usage

### Server

1. Portaudio must be installed prior to setup, or else `ERROR: Failed building wheel for pyaudio` will occur
   while installing Python dependencies.
2. Create a virtual environment and install the dependencies from `requirements.txt`.
3. Run the server on the local network with `python manage.py runserver 0.0.0.0:8000`.
   Note: the client and server must be running on the same wifi network for communication to work.
   Certain wifi networks, such as school wifi, may cause issues due to network restrictions.

### Client

1. Install python dependencies on the raspberry pi virtual environment.
2. Update the webscoket uri in `main.py` at the root of the client directory.
3. Run `main.py`.

## Contact

For any inquiries, email l2ge@uwaterloo.ca.
