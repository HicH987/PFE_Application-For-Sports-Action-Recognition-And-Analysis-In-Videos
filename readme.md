
<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>PFE: Application For Sports Action Recognition And Analysis In Videos
</h1>
<h3>Developed with the software and tools listed below</h3>

<p align="center">
<img src="https://img.shields.io/badge/TensorFlow-FF6F00.svg?style&logo=TensorFlow&logoColor=white" alt="TensorFlow" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style&logo=Python&logoColor=white" alt="Python" />
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
- [📂 Project Structure](#project-structure)
- [🚀 Getting Started](#-getting-started)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---


## 📍 Overview
Overview of the README for the repository containing two projects:

- **App Project:**
This repository contains the DeepTrain App, a desktop application that utilizes the "test_model_analyze" project. The app is specifically designed for sports action recognition and analysis in videos. It leverages the MediaPipe library to extract 2D points from workout videos or live streams. These extracted 2D points are then fed into a classification model to predict the type of workout being performed. The app provides a user interface (UI) that ensures a seamless experience for the users.

- **Test_Model_Analyze Project:**
This project implements a workout classification model for 16 different types of workouts. It also utilizes the Mediapipe library to extract 2D points from workout videos or live streams. These extracted 2D points are then fed into the classification model, which accurately predicts the type of workout being performed. After the prediction, the project performs a comprehensive workout analysis using the predicted label and Mediapipe pose as input. This analysis includes the calculation of various body angles to count repetitions, determine the duration of the workout, and provide feedback on the movement.

The supported workout labels for this project are as follows:
- arm-raise
- basic-curl
- biceps-curl-bar
- bicycle-crunch
- bird-dog
- deadlift
- fly
- leg-raise
- overhead-press
- plank
- pushup
- russian-twist
- squat
- superman
- bench-press
- pullup

These projects collectively provide a powerful and user-friendly solution for sports action recognition, analysis, and workout classification.


---


## 📂 Project Structure


```bash
repo
├── app_interface
│
└── test_model_analyze
│
├── readme.md

```

---

## 🚀 Getting Started

### 📦 Installation

1. Clone the `pfe--application-for-sports-action-recognition-and-analysis-in-videos` repository:
```sh
git clone https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos
```

2. Change to the project directory:
```sh
cd pfe--application-for-sports-action-recognition-and-analysis-in-videos
```

#### For the `app_interface` project:

3. Change to the `app_interface` directory:
```sh
cd app_interface
```

4. Install the dependencies for the `app_interface` project:
```sh
pip install -r requirements.txt
```

#### For the `test_model_analyze` project:

3. Change to the `test_model_analyze` directory:
```sh
cd test_model_analyze
```

4. Install the dependencies for the `test_model_analyze` project:
```sh
pip install -r requirements.txt
```

### 🎮 Using pfe--application-for-sports-action-recognition-and-analysis-in-videos

```sh
python main.py
```

---


---

## 📄 License

[MIT](./LICENSE)

---

## 👏 Acknowledgments

> - [Matec-conferences.org](https://www.matec-conferences.org/articles/matecconf/abs/2017/46/matecconf_dts2017_05016/matecconf_dts2017_05016.html): A paper that inspired the pose data normalization.
> - [Learnopencv.com](https://learnopencv.com/introduction-to-video-classification-and-human-activity-recognition/): Inspiration for methods to make human action recognition.
> - [Face_Recognition](https://github.com/ageitgey/face_recognition): A helpful library that facilitated the implementation of face identification for the login feature.
---
