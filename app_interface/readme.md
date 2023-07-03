<div align="center">
<h1 align="center">
<img src="ui/assets/logo.png" width="400" />
<br>DeepTrain App
</h1>

<h3>Developed with the software and tools listed below</h3>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/TensorFlow-FF6F00.svg?style&logo=TensorFlow&logoColor=white" alt="TensorFlow" />
<img src="https://img.shields.io/badge/pandas-150458.svg?style&logo=pandas&logoColor=white" alt="pandas" />
<img src="https://img.shields.io/badge/NumPy-013243.svg?style&logo=NumPy&logoColor=white" alt="NumPy" />
<img src="https://img.shields.io/badge/JSON-000000.svg?style&logo=JSON&logoColor=white" alt="JSON" />
<img src="https://img.shields.io/badge/Mediapipe-00C6FF.svg?style&logo=Mediapipe&logoColor=white" alt="Mediapipe" />
</p>
<img src="https://img.shields.io/github/languages/top/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos?style&color=5D6D7E" alt="GitHub top language" />
<img src="https://img.shields.io/github/languages/code-size/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos?style&color=5D6D7E" alt="GitHub code size in bytes" />
<img src="https://img.shields.io/github/commit-activity/m/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos?style&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/license/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos?style&color=5D6D7E" alt="GitHub license" />
</div>


---

## 📒 Table of Contents
- [📒 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [⚙️ Features](#-features)
- [📂 Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🚀 Getting Started](#-getting-started)
- [🗺 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---


## 📍 Overview

This repository contains the DeepTrain App, a desktop application that utilizes the "test_model_analyze" project. The app is designed for sports action recognition and analysis in videos. It uses the MediaPipe library to extract 2D points from workout videos or live streams. These 2D points are then fed into a classification model to predict the type of workout being performed. The app provides a user interface (UI) for a seamless experience.

For more information on the "test_model_analyze" project, you can click [here](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/tree/master/test_model_analyze).

---

## ⚙️ Features


- Face identification is used for login authentication.\
  <img src="https://user-images.githubusercontent.com/62667537/250661802-6a159516-1a90-478e-86db-4a266f458327.png" width="300" height="200" alt="Face Identification"> <img src="https://user-images.githubusercontent.com/62667537/250662084-74daf019-9a15-4aef-a150-cd715ae75d71.png" width="300" height="200" alt="Face Identification">

- Welcome tab where we can find an illustration of each workout that is supported by the app.\
  <img src="https://user-images.githubusercontent.com/62667537/250662183-4a4e4924-4b6e-4108-bdf3-5c0ea67f81a3.png" width="300" height="200" alt="Welcome Tab"> <img src="https://user-images.githubusercontent.com/62667537/250662287-b56bfebd-134c-4b3f-8e67-0f9b7d8d8b05.png" width="300" height="200" alt="Welcome Tab">

- Real-time workout analysis in the Realtime tab.\
  <img src="https://user-images.githubusercontent.com/62667537/250662394-2ea939d5-2c99-4cb9-9d60-c5fff440f322.png" width="300" height="200" alt="Real-time Analysis"> <img src="https://user-images.githubusercontent.com/62667537/250662591-7b2cbf94-35ed-4c95-a86b-d73c509c7b98.png" width="300" height="200" alt="Real-time Analysis">

- Option to upload prerecorded workout videos for analysis in the Prerecorded tab.\
  <img src="https://user-images.githubusercontent.com/62667537/250662768-f5cdc183-d5ee-42cf-8c58-50a8d6983c5d.png" width="300" height="200" alt="Prerecorded Analysis"> <img src="https://user-images.githubusercontent.com/62667537/250662853-40867d6f-ed8c-48f5-8b22-59616eca95c3.png" width="300" height="200" alt="Prerecorded Analysis"> <img src="https://user-images.githubusercontent.com/62667537/250662919-a39c5a11-c592-4f47-b457-a25a3511a9fd.png" width="300" height="200" alt="Prerecorded Analysis">

- View statistics on workout progression in the Statistics tab.\
  <img src="https://user-images.githubusercontent.com/62667537/250663136-99b9399e-38a5-4e5a-b415-10522e46a4ce.png" width="300" height="200" alt="Workout Statistics">

- Logout option available in the Last tab.\
  <img src="https://user-images.githubusercontent.com/62667537/250663186-381bfd1a-14c3-4776-9da7-40c7ae0f0c08.png" width="300" height="200" alt="Logout">



---

## 📂 Project Structure

```bash
repo
├── data
│   └── database.db
├── helpers
│   ├── __init__.py
│   ├── analyse.py
│   ├── DeepFitClassifier.py
│   ├── face_id.py
│   ├── global_vars.py
│   ├── normlization.py
│   ├── prediction.py
│   └── utils.py
└── ui
│   ├── __init__.py
│   ├── Config.py
│   ├── CustomStuffs.py
│   ├── LoginPage.py
│   ├── MainPage.py
│   ├── PageController.py
│   └── Tabs.py
│   ├── assets
│   │   ├── beep.mp3
│   │   ├── custom_dark_teal.xml
│   │   ├── exercises_audio/*.mp3
│   │   ├── exercises_gif/*.gif
│   │   ├── icon.ico
│   │   ├── icon.png
│   │   ├── logo.png
│   │   └── tuto.json
├── models
│   ├── model_1_test.tflite
│   └── model_2_test.tflite
├── DeepTrain-AI.bat
├── gui.py
├── requirements.txt

7 directories, 59 files
```

---

## 🧩 Modules

<details closed><summary>Root</summary>

| File                                                                                    | Summary                                                                                                                                                                                                                |
| ---                                                                                     | ---                                                                                                                                                                                                                    |
| [DeepTrain-AI.bat](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/DeepTrain-AI.bat) | This code snippet is an example of a batch file that executes a Python script called "gui.py" using the "pythonw" command. The "pythonw" command runs the script in the background without showing the console window. |
| [gui.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/gui.py) | This code snippet is the main code that call and run all the pages of the ui and init the database

</details>

<details closed><summary>ui</summary>

| File                                                                                    | Summary                                                                                                                                                                                                                |
| ---                                                                                     | ---                                                                                                                                                                                                                    |
| [Config.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/ui/Config.py)            | This file contains the configuration settings, including CSS and global variables used across the UI components.                                                                                                        |
| [CustomStuffs.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/ui/CustomStuffs.py)  | This file provides custom implementations of components such as CustomButton and CustomInputDialog.                                                                                                                    |
| [LoginPage.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/ui/LoginPage.py)      | This file contains the LoginPage class, which represents the login page of the application.                                                                                                                           |
| [MainPage.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/ui/MainPage.py)        | This file contains the MainPage class, which represents the main page of the application. It includes tabs and serves as the main app interface.                                                                        |
| [PageController.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/ui/PageController.py) | This file contains the PageController class, which controls the switch between pages, such as LoginPage and MainPage.                                                                                                  |
| [Tabs.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/ui/Tabs.py)              | This file contains the four tabs: Welcome, realtime, pre-recorded, statistic, and logout. These tabs are part of the main app and provide different functionalities.                                                  |


</details>

<details closed><summary>Helpers</summary>

| File                                                                                      | Summary                                                                                                                                                                                                                                                                                                                                                      |
| ---                                                                                       | ---                                                                                                                                                                                                                                                                                                                                                          |
| [global_vars.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/helpers/global_vars.py)   | The code snippet defines two important components. First, it assigns labels to various exercises. Second, it maps landmarks from the COCO pose model to specific body parts for analysis.                                                                  |
| [normlization.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/helpers/normlization.py) | The provided code snippet contains functions to calculate Euclidean distance between vectors and normalize coordinates relative to the length of the body and the center of gravity. It also handles error checking and transformations of the input data. |
| [DeepFitClassifier.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/helpers/DeepFitClassifier.py) | The provided code snippet defines the DeepFitClassifier class, which is used for loading and using a model to predict exercise labels based on pose keypoints. It supports both TensorFlow Lite and Keras models. |
| [prediction.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/helpers/prediction.py) | This code snippet imports various helper functions and modules, including pose detection and analysis functions. It also initializes a deep learning classifier model. The main function "prediction" takes an image as input, detects pose landmarks using the MediaPipe library, makes predictions using the classifier, and returns the analyzed results. |
| [utils.py](https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos/blob/master/app_interface/helpers/utils.py)         | The provided code snippet includes various utility functions for pose detection and analysis. It includes functions for initializing the pose model, performing pose detection on an image, drawing landmarks on an image, extracting 2D landmarks from the results, calling normaliztion.py landmarks, making predictions using a trained classifier, and more. |
</details>

---

## 🚀 Getting Started

### 📦 Installation

1. Clone the app_interface repository:
```sh
git clone https://github.com/HicH987/app_interface
```

2. Change to the project directory:
```sh
cd app_interface
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🎮 Using test_model_analyze
```sh
python gui.py
```
or run the ```DeepTrain-AI.bat```

---

## 🤝 Contributing

Contributions are always welcome! Follow these steps to contribute:

1. Fork the project repository.
2. Clone the forked repository to your local machine.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).
```sh
git checkout -b new-feature-branch
```
4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.
```sh
git commit -m 'Implemented new feature'
```
6. Push your changes to your forked repository on GitHub.
```sh
git push origin new-feature-branch
```
7. Create a new pull request to the original project repository. Provide a description of your changes and why they're necessary.
The project maintainers will review your changes and provide feedback or merge them into the main branch.

---
## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository) file for additional information.

---

## 👏 Acknowledgments

> - [Matec-conferences.org](https://www.matec-conferences.org/articles/matecconf/abs/2017/46/matecconf_dts2017_05016/matecconf_dts2017_05016.html): A paper that inspired the pose data normalization.
> - [Learnopencv.com](https://learnopencv.com/introduction-to-video-classification-and-human-activity-recognition/): Inspiration for methods to make human action recognition.
> - [Face_Recognition](https://github.com/ageitgey/face_recognition): A helpful library that facilitated the implementation of face identification for the login feature.