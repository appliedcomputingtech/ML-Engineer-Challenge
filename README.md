# Machine Learning Engineer Coding Challenge

Welcome! you are a super star for making it here. This is your time to shine, an opportunity to show off your skills, understanding and more importantly coding abilities 😉. So relax, grab some coffee / whiskey (depending on time of day) and start developing on this take-home exercise.


## Overview

This coding test is divided into three parts, each testing different aspects of your machine learning engineering skills. You will need to use PyTorch, TensorRT, ONNX, and various hyperparameter tuning libraries to complete these tasks. 

Please ensure you have the necessary libraries installed. If you do not have a GPU environment, please let `nick@kashmirintelligence.com` know, and one will be created for you.

## Part 1: Model Quantisation and Benchmarking

**Objective**: Take a complex computer vision model from Torch Hub, quantise it, and benchmark the speed of inference on the test subset of [tiny-ImageNet dataset](https://www.kaggle.com/datasets/akash2sharma/tiny-imagenet).

To download the dataset, use the following utility script:

```shell
python ./utils/download_tiny_imagenet.py
```

### Instructions 📃

1. Select a complex computer vision model from Torch Hub (e.g., Dinov2).
2. Prepare a small subset of ImageNet images for inference.
3. Apply dynamic quantisation to the model.
4. Measure and compare the inference time of the original and quantized models.
5. Report the inference times and any differences in accuracy.

### Submission 💻
- Python script with code for loading, quantising, and benchmarking the model.
- A brief analysis report (ipynb, markdown or PDF) with inference time comparisons and accuracy differences.

---

## Part 2: Automated Hyperparameter Tuning

**Objective**: Conduct automated hyperparameter tuning to identify the optimal hyperparameters for a small CNN trained on the [CIFAR100](https://pytorch.org/vision/stable/generated/torchvision.datasets.CIFAR100.html) training dataset. (Refer to instructions in Part 1 for downloading the data)

### Instructions 📃

1. Define a small CNN architecture of choice for the CIFAR-100 dataset.
2. Set up a training loop for the CNN model.
3. Choose hyperparameters to tune (e.g., learning rate, batch size, number of layers, etc.).
4. Use a hyperparameter optimization library (e.g., Optuna, Hyperopt, or Scikit-Optimize) to find the best hyperparameters.
5. Train the model using the optimal hyperparameters and report the final accuracy.

### Submission 💻

- Python script with the model definition, training loop, and hyperparameter tuning setup.
- A brief report (markdown or PDF) detailing the hyperparameter tuning process and final model accuracy.

---

## Part 3: Model Conversion to TensorRT and ONNX

Objective: Convert a trained model to TensorRT format and serialize it in ONNX for fast inference on Nvidia GPUs.

### Instructions 📃

1. Train or use a pre-trained model (it can be the model from Part 1 or another model).
2. Export the model to ONNX format.
3. Convert the ONNX model to TensorRT using TensorRT tools.
4. Measure the inference time of the TensorRT model on an Nvidia GPU.
5. Report the inference times and any speedup achieved.

### Submission 💻

- Python script with code for model training/loading, ONNX export, and TensorRT conversion.
- A brief report (markdown or PDF) with inference time benchmarks and any observed improvements.

## General Submission Guidelines

- Ensure all code is well-documented and follows best practices.
- Include a requirements.txt file with all dependencies required to run your code.
- Submit your code and reports in a zip file or through a GitHub repository link.

## Evaluation Criteria
- Correctness: Does the code achieve the desired outcomes?
- Efficiency: Are the implementations optimized for performance?
- Clarity: Is the code well-structured and documented?
- Reporting: Are the reports clear and do they adequately explain the results?

Good luck, and we look forward to seeing your solutions!