<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>test_model_analyze
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
<img src="https://img.shields.io/github/languages/top/HicH987/app_interface?style&color=5D6D7E" alt="GitHub top language" />
<img src="https://img.shields.io/github/languages/code-size/HicH987/app_interface?style&color=5D6D7E" alt="GitHub code size in bytes" />
<img src="https://img.shields.io/github/commit-activity/m/HicH987/app_interface?style&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/license/HicH987/app_interface?style&color=5D6D7E" alt="GitHub license" />
</div>

---

## 📒 Table of Contents
- [📒 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📂 Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🚀 Getting Started](#-getting-started)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---

## 📍 Overview

This project is an implementation of a workout classification model for 16 different workouts. The project uses the Mediapipe library to extract 2D points from workout videos or live streams. These 2D points are then fed into the classification model, which predicts the type of workout being performed. After the prediction, a workout analysis is performed using the predicted label and Mediapipe pose as input. This analysis calculates different angles of the body to count repetitions of the workout, duration, and provides feedback on the movement.

The supported workout labels are as follows:
```
LABELS = [
    "arm-raise",
    "basic-curl",
    "biceps-curl-bar",
    "bicycle-crunch",
    "bird-dog",
    "deadlift",
    "fly",
    "leg-raise",
    "overhead-press",
    "plank",
    "pushup",
    "russian-twist",
    "squat",
    "superman",
    "bench-press",
    "pullup",
]
```

---

## 📂 Project Structure

```bash
repo
├── helpers
│   ├── analyse.py
│   ├── DeepFitClassifier.py
│   ├── global_vars.py
│   ├── normlization.py
│   └── utils.py
├── main.py
├── models
│   ├── model_1_test.tflite
│   └── model_2_test.tflite
└── requirements.txt

2 directories, 9 files
```

---

## 🧩 Modules

<details closed><summary>Helpers</summary>

| File                                                                                               | Summary                                                                                                                                                                                                                                                    |
| ---                                                                                                | ---                                                                                                                                                                                                                                                        |
| [global_vars.py](https://github.com/HicH987/test_model_analyze/blob/main/helpers/global_vars.py)   | The code snippet defines two important components. First, it assigns labels to various exercises. Second, it maps landmarks from the COCO pose model to specific body parts for analysis.                                                                  |
| [normlization.py](https://github.com/HicH987/test_model_analyze/blob/main/helpers/normlization.py) | The provided code snippet contains functions to calculate Euclidean distance between vectors and normalize coordinates relative to the length of the body and the center of gravity. It also handles error checking and transformations of the input data. |
| [DeepFitClassifier.py](https://github.com/HicH987/test_model_analyze/blob/main/helpers/DeepFitClassifier.py) | The provided code snippet defines the DeepFitClassifier class, which is used for loading and using a model to predict exercise labels based on pose keypoints. It supports both TensorFlow Lite and Keras models. |
| [utils.py](https://github.com/HicH987/test_model_analyze/blob/main/helpers/utils.py)         | The provided code snippet includes various utility functions for pose detection and analysis. It includes functions for initializing the pose model, performing pose detection on an image, drawing landmarks on an image, extracting 2D landmarks from the results, calling normaliztion.py landmarks, making predictions using a trained classifier, and more. |

</details>

---

## 🚀 Getting Started

### 📦 Installation

1. Clone the test_model_analyze repository:
```sh
git clone https://github.com/HicH987/test_model_analyze
```

2. Change to the project directory:
```sh
cd test_model_analyze
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🎮 Using test_model_analyze

```sh
python main.py
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository) file for additional information.

---

## 👏 Acknowledgments

> - [Matec-conferences.org](https://www.matec-conferences.org/articles/matecconf/abs/2017/46/matecconf_dts2017_05016/matecconf_dts2017_05016.html): A paper that inspired the pose data normalization.
> - [Learnopencv.com](https://learnopencv.com/introduction-to-video-classification-and-human-activity-recognition/): Inspiration for methods to make human action recognition.

---