# Day 29: Transfer Learning with MobileNetV2 & ResNet50 Fine-Tuning

> **Week 6 – Day 29 | CTPL AI/ML Internship Program**

---

# 📖 Overview

Transfer Learning is one of the most effective techniques in modern Deep Learning and Computer Vision. Instead of training a Convolutional Neural Network (CNN) from scratch, Transfer Learning utilizes knowledge learned from large-scale datasets such as **ImageNet** and applies it to new tasks.

In this project, two widely used pre-trained CNN architectures—**MobileNetV2** and **ResNet50**—are applied to the **CIFAR-10** image classification dataset. Both models are evaluated using two Transfer Learning strategies:

- **Feature Extraction**
- **Fine-Tuning**

To make the implementation memory-efficient, the project uses TensorFlow's **tf.data** pipeline for preprocessing, batching, and prefetching images dynamically instead of loading the entire resized dataset into memory.

This notebook demonstrates how Transfer Learning can significantly improve model accuracy while reducing training time and computational requirements.

---

# 📌 Project Information

| Item | Details |
|------|---------|
| **Internship** | CTPL AI/ML Internship Program |
| **Week** | 6 |
| **Day** | 29 |
| **Topic** | Transfer Learning |
| **Dataset** | CIFAR-10 |
| **Framework** | TensorFlow / Keras |
| **Models** | MobileNetV2, ResNet50 |

---

# 🎯 Learning Objectives

After completing this project, you will be able to:

- Understand the concept of Transfer Learning.
- Explain why pre-trained models perform better than training from scratch.
- Build image classification models using MobileNetV2.
- Implement Feature Extraction.
- Apply Fine-Tuning with lower learning rates.
- Compare MobileNetV2 and ResNet50.
- Evaluate model performance using multiple metrics.
- Generate confusion matrices and classification reports.
- Build memory-efficient TensorFlow data pipelines.

---

# 🧠 What is Transfer Learning?

Transfer Learning is a Deep Learning technique where knowledge learned from one task is reused for another related task.

Instead of initializing a neural network with random weights, Transfer Learning starts with a model already trained on millions of images. These pre-trained weights contain valuable visual knowledge such as:

- Edge detection
- Texture recognition
- Shape identification
- Color patterns
- Object structures

These learned representations can then be adapted to solve a completely different image classification problem with significantly less training time.

---

# 🚀 Why Transfer Learning Works

Transfer Learning works because early convolutional layers learn universal image features that are useful across almost every computer vision task.

For example:

- First layers detect edges and lines.
- Middle layers learn textures and shapes.
- Final layers recognize high-level objects.

Rather than relearning these patterns from scratch, Transfer Learning simply reuses them and only learns the task-specific information.

### Benefits

- Faster training
- Higher accuracy
- Better generalization
- Requires less data
- Reduces computational cost

---

# 🔄 Transfer Learning Approaches

Two approaches are implemented in this project.

## 1. Feature Extraction

Feature Extraction freezes the entire pre-trained network and trains only the newly added classification layers.

### Advantages

- Very fast
- Low computational cost
- Less overfitting
- Ideal for small datasets

---

## 2. Fine-Tuning

Fine-Tuning unfreezes the upper layers of the pre-trained model and retrains them using a very small learning rate.

### Advantages

- Higher accuracy
- Better adaptation
- Learns task-specific features
- Improves performance on target dataset

---

# 📊 Pre-trained Models

## MobileNetV2

MobileNetV2 is a lightweight convolutional neural network designed for mobile and embedded devices.

### Characteristics

| Property | Value |
|----------|-------|
| Architecture | Depthwise Separable CNN |
| Parameters | ~3.5 Million |
| ImageNet Accuracy | ~71.8% |
| Speed | Very Fast |
| Memory Usage | Low |
| Best Use Case | Mobile Deployment |

### Advantages

- Lightweight architecture
- Fast inference
- Low memory consumption
- Suitable for edge devices

---

## ResNet50

ResNet50 is a deep residual network that uses skip connections to enable very deep neural networks without suffering from vanishing gradients.

### Characteristics

| Property | Value |
|----------|-------|
| Architecture | Residual CNN |
| Parameters | ~25.6 Million |
| ImageNet Accuracy | ~74.9% |
| Speed | Moderate |
| Memory Usage | Higher |
| Best Use Case | High-Accuracy Applications |

### Advantages

- Higher classification accuracy
- Strong feature extraction capability
- Excellent performance on complex datasets

---

# ⚖️ MobileNetV2 vs ResNet50

| Feature | MobileNetV2 | ResNet50 |
|----------|-------------|----------|
| Parameters | 3.5M | 25.6M |
| Speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Accuracy | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Memory Usage | Low | High |
| Deployment | Mobile | Server |
| Training Time | Short | Longer |

---

# 📁 Project Structure

```
day-29/
│
├── notebooks/
│   └── day_29_transfer_learning.ipynb
│
├── outputs/
│   ├── models/
│   │   ├── mobilenetv2_feature_extract.keras
│   │   ├── mobilenetv2_finetuned.keras
│   │   └── resnet50_feature_extract.keras
│   │
│   ├── plots/
│   │   ├── training_curves.png
│   │   ├── confusion_matrix.png
│   │   ├── comparison_chart.png
│   │   └── accuracy_plots.png
│   │
│   └── logs/
│       ├── classification_report.txt
│       ├── model_summary.txt
│       ├── results.pkl
│       └── reflection.txt
│
├── requirements.txt
└── README.md
```
# 🔧 Implementation

The project is divided into four main stages:

1. Data Preparation
2. Feature Extraction
3. Fine-Tuning
4. Model Evaluation

---

# 📂 Data Preparation

Before training, the CIFAR-10 dataset is prepared using TensorFlow.

### Steps

- Load CIFAR-10 dataset
- Resize images to **224 × 224**
- Normalize images using model-specific preprocessing
- Create TensorFlow `tf.data` pipelines
- Shuffle, batch, and prefetch data

This approach keeps memory usage low by processing images on demand instead of storing resized copies.

---

# 🚀 Phase 1: Feature Extraction

Feature Extraction uses a pre-trained model as a fixed feature extractor.

### Workflow

1. Load ImageNet pre-trained weights.
2. Remove the original classification head.
3. Freeze all backbone layers.
4. Add a custom classifier.
5. Train only the new classification layers.

```python
base_model = MobileNetV2(
    input_shape=(224,224,3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

x = GlobalAveragePooling2D()(base_model.output)
x = Dense(256, activation="relu")(x)
x = Dropout(0.5)(x)
outputs = Dense(10, activation="softmax")(x)

model = Model(base_model.input, outputs)
```

### Training Configuration

| Parameter | Value |
|-----------|-------|
| Optimizer | Adam |
| Learning Rate | 1e-3 |
| Loss | Categorical Crossentropy |
| Epochs | 15 |

---

# 🔥 Phase 2: Fine-Tuning

After Feature Extraction, the upper layers are unfrozen to improve performance.

Only the last few layers are retrained while keeping earlier layers frozen.

```python
base_model.trainable = True

for layer in base_model.layers[:-20]:
    layer.trainable = False

model.compile(
    optimizer=Adam(1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
```

### Fine-Tuning Configuration

| Parameter | Value |
|-----------|-------|
| Learning Rate | 1e-5 |
| Trainable Layers | Last 20 |
| Epochs | 10 |

---

# ⚡ Memory-Efficient Data Pipeline

Instead of resizing every image beforehand, TensorFlow processes images dynamically.

```python
dataset = tf.data.Dataset.from_tensor_slices((images, labels))

dataset = dataset.map(process_image)

dataset = dataset.batch(32)

dataset = dataset.prefetch(tf.data.AUTOTUNE)
```

### Advantages

- Low RAM usage
- Faster data loading
- Better GPU utilization
- Scalable for large datasets

---

# ▶️ How to Run

### Local Machine

```bash
pip install -r requirements.txt

jupyter notebook
```

Open:

```
notebooks/day_29_transfer_learning.ipynb
```

Run all cells.

---

### Google Colab

1. Upload the notebook.
2. Enable GPU.
3. Install required libraries.
4. Run all cells.

---

# 📈 Results

The project compares three approaches:

| Model | Performance |
|--------|-------------|
| CNN from Scratch | Baseline |
| MobileNetV2 Feature Extraction | Better Accuracy |
| MobileNetV2 Fine-Tuning | Best Overall |
| ResNet50 | High Accuracy with More Parameters |

Fine-Tuning consistently improves classification accuracy over Feature Extraction.

---

# 📊 Generated Outputs

The notebook generates:

- Training & Validation Curves
- Accuracy/Loss Graphs
- Confusion Matrices
- Classification Report
- Model Comparison Charts
- Saved Model Files

---

# 💾 Memory Optimization

The implementation avoids loading all resized images into RAM.

Instead, TensorFlow resizes and preprocesses each batch during training using the `tf.data` pipeline.

This makes the notebook suitable for systems with limited memory while maintaining efficient training performance.

# 🔑 Key Takeaways

This project highlights the practical advantages of Transfer Learning for image classification tasks.

- Transfer Learning significantly reduces training time.
- Pre-trained models provide better feature representations than training from scratch.
- Feature Extraction offers a fast and efficient baseline.
- Fine-Tuning further improves model performance by adapting high-level features.
- The `tf.data` pipeline enables efficient preprocessing with lower memory usage.
- MobileNetV2 is ideal for lightweight applications, while ResNet50 provides higher accuracy for more powerful systems.

---

# 🌍 Real-World Applications

Transfer Learning is widely used across various industries.

| Domain | Example Applications |
|---------|----------------------|
| Healthcare | Medical image diagnosis, disease detection |
| Agriculture | Plant disease identification |
| Retail | Product recognition and inventory management |
| Manufacturing | Defect detection and quality inspection |
| Security | Object detection and facial recognition |
| Autonomous Systems | Traffic sign and object classification |

---

# 📚 Resources

Useful references for further learning:

- TensorFlow Transfer Learning Guide
- TensorFlow Keras Documentation
- MobileNetV2 Research Paper
- ResNet Research Paper
- TensorFlow `tf.data` Guide
- CIFAR-10 Dataset Documentation

---

# ❓ Reflection Questions

### 1. Why is Transfer Learning more effective than training from scratch?

Because the model already contains useful visual features learned from millions of images, reducing both training time and data requirements.

---

### 2. When should Feature Extraction be used?

Feature Extraction is suitable when the dataset is small or when quick model development is required.

---

### 3. Why is a lower learning rate used during Fine-Tuning?

A smaller learning rate prevents large weight updates that could damage the useful knowledge learned during pre-training.

---

### 4. Why does MobileNetV2 train faster than ResNet50?

MobileNetV2 has a lightweight architecture with significantly fewer parameters, making it computationally efficient.

---

### 5. How does the `tf.data` pipeline improve training?

It preprocesses data dynamically, reducing memory usage and improving training performance.

---

# 🐞 Common Issues

## Memory Error (OOM)

**Cause**

- Large batch size
- Limited system memory

**Solution**

- Reduce batch size (32 → 16)
- Use the `tf.data` pipeline
- Prefer MobileNetV2 for lower memory usage

---

## Overfitting

**Cause**

The model memorizes the training data instead of learning general patterns.

**Solution**

- Increase Dropout
- Apply Data Augmentation
- Reduce training epochs
- Use Early Stopping

---

## Slow Training

**Solution**

- Enable GPU acceleration
- Use smaller batch sizes if memory is limited
- Use MobileNetV2 instead of larger models
- Enable TensorFlow AUTOTUNE

---

## Low Accuracy

**Solution**

- Increase Fine-Tuning epochs
- Verify image preprocessing
- Adjust the learning rate
- Experiment with different pre-trained models

---

# ⚡ Performance Tips

- Start with **Feature Extraction** before Fine-Tuning.
- Fine-Tune only the top layers instead of the entire network.
- Always use a smaller learning rate during Fine-Tuning.
- Save model checkpoints during long training sessions.
- Use `tf.data` with `prefetch()` and `AUTOTUNE` for better performance.

---

# 📈 Future Improvements

Possible extensions for this project include:

- Experiment with EfficientNet and Vision Transformers (ViT).
- Apply advanced data augmentation techniques.
- Perform hyperparameter tuning.
- Train on larger image datasets.
- Deploy the trained model using Streamlit or Flask.
- Convert the model to TensorFlow Lite for mobile deployment.

---

# 📌 Conclusion

This project demonstrates how Transfer Learning can efficiently solve image classification problems using pre-trained deep learning models.

Both **MobileNetV2** and **ResNet50** achieved strong performance on the CIFAR-10 dataset while requiring significantly less training time than a CNN built from scratch. Feature Extraction provided a fast baseline, while Fine-Tuning further improved accuracy by adapting the learned features to the target dataset.

The use of TensorFlow's `tf.data` pipeline also ensured efficient memory utilization, making the implementation suitable even for systems with limited hardware resources.
