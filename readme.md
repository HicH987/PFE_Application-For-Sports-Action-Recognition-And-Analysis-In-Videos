
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
<img src="https://img.shields.io/badge/Markdown-000000.svg?style&logo=Markdown&logoColor=white" alt="Markdown" />
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
- [🤝 Contributing](#-contributing)
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
│   ├── data
│   │   └── database.db
│   ├── helpers
│   │   ├── __init__.py
│   │   ├── face_id.py
│   │   ├── global_vars.py
│   │   ├── normlization.py
│   │   ├── DeepFitClassifier.py
│   │   ├── prediction.py
│   │   ├── analyse.py
│   │   └── utils.py
│   ├── models
│   │   ├── model_1_test.tflite
│   │   └── model_2_test.tflite
│   |── ui
│   |    ├── assets
│   |    │   ├── beep.mp3
│   |    │   ├── custom_dark_teal.xml
│   |    │   ├── exercises_audio/*.mp3
│   |    │   ├── exercises_gif/*.gif
│   |    │   ├── icon.ico
│   |    │   ├── icon.png
│   |    │   ├── logo.png
│   |    │   └── tuto.json
│   |    ├── Config.py
│   |    ├── CustomStuffs.py
│   |    ├── __init__.py
│   |    ├── LoginPage.py
│   |    ├── MainPage.py
│   |    ├── PageController.py
│   |    └── Tabs.py
│   ├── gui.py
│   ├── DeepTrain-AI.bat
│   ├── readme.md
│   ├── requirements.txt
└── test_model_analyze
│   ├── helpers
│   │   ├── global_vars.py
│   │   ├── normlization.py
│   │   ├── DeepFitClassifier.py
│   │   ├── analyse.py
│   │   └── utils.py
│   ├── models
│   │   ├── model_1_test.tflite
│   │   └── model_2_test.tflite
│   ├── main.py
│   ├── readme.md
│   └── requirements.txt
├── readme.md

11 directories, 71 files
```

---


## 🚀 Getting Started

### 📦 Installation

1. Clone the pfe--application-for-sports-action-recognition-and-analysis-in-videos repository:
```sh
git clone https://github.com/HicH987/pfe--application-for-sports-action-recognition-and-analysis-in-videos
```

2. Change to the project directory:
```sh
cd pfe--application-for-sports-action-recognition-and-analysis-in-videos
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🎮 Using pfe--application-for-sports-action-recognition-and-analysis-in-videos

```sh
python main.py
```

---

## 🤝 Contributing

Contributions are always welcome! Please follow these steps:
1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).
```sh
git checkout -b new-feature-branch
```
4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.
```sh
git commit -m 'Implemented new feature.'
```
6. Push your changes to your forked repository on GitHub using the following command
```sh
git push origin new-feature-branch
```
7. Create a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.
The project maintainers will review your changes and provide feedback or merge them into the main branch.

---

## 📄 License

[MIT](./LICENSE)

---

## 👏 Acknowledgments

> - [Matec-conferences.org](https://www.matec-conferences.org/articles/matecconf/abs/2017/46/matecconf_dts2017_05016/matecconf_dts2017_05016.html): A paper that inspired the pose data normalization.
> - [Learnopencv.com](https://learnopencv.com/introduction-to-video-classification-and-human-activity-recognition/): Inspiration for methods to make human action recognition.
> - [Face_Recognition](https://github.com/ageitgey/face_recognition): A helpful library that facilitated the implementation of face identification for the login feature.
---
