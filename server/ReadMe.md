# MTU Fingerprint Recognition

> 🚧 **Status: Research & Development**

An exploration of fingerprint matching using image processing and machine learning.

The fingerprint image extraction stage has already been solved using open-source work. The major remaining problem is developing a reliable **matching algorithm**.

## Problem

The system needs to determine whether two fingerprint images belong to the same person.

The current direction is moving away from building a traditional fingerprint-matching algorithm completely from scratch and toward a neural-network-based approach.

---

# Proposed Approaches

## 1. Neural Network

### Pros

- Easier to modify
- Avoids having to manually implement all of the underlying matching mathematics
- Can be adapted as the project develops

### Cons / Open Questions

- Inference cost may be a problem
- TensorFlow Lite may help with deployment
- The relationship between model size and accuracy still needs to be investigated
- A very large model is probably unnecessary for a small dataset

---

## 2. Fingerprint Algorithm From Scratch

The alternative is to implement the fingerprint matching algorithm manually.

The current project notes identify this as:

- difficult
- mathematically intensive
- primarily useful as a learning/experimental challenge

The exact implementation has not yet been defined.

---

## 3. Traditional ML Algorithm

Traditional machine-learning approaches were also considered.

This direction is currently less attractive because of limitations around how much the algorithm can be customized for the problem.

---

# Feature Extraction Pipeline

The fingerprint images may be processed to extract useful features before matching.

Current ideas include:

```text
Fingerprint Image
       │
       ├──> Grayscale
       │
       ├──> Edge Extraction
       │
       ├──> Ridge Extraction
       │
       └──> Additional Fingerprint Feature Extraction
```

The exact feature-extraction algorithm is still being explored.

---

# Training

If the neural-network approach is used, the training pipeline is expected to include data augmentation.

## Proposed Technique 1

Use different representations of the same fingerprint image.

For example:

```text
Same Fingerprint
      │
      ├──> Grayscale
      ├──> Canny / Edge Representation
      └──> Other Representation
```

These representations can be provided to the model as additional information.

## Proposed Technique 2

Use a normal image-training pipeline with image augmentation.

> The final augmentation strategy has not yet been determined.

---

# Siamese Network Direction

The newest direction is a **Siamese network**.

Instead of treating every student as a separate classification class, the model compares two fingerprint images.

```text
Image 1 ──┐
          │
          ▼
       Model
          │
          ▼
     Similarity
          ▲
          │
Image 2 ──┘
```

The intended use is:

```text
Stored Fingerprint ──┐
                     ├──> Siamese Model ──> Similarity
Captured Fingerprint ┘
```

Here:

- `img_1` is the stored fingerprint image for the person
- `img_2` is the fingerprint image currently being inferred

This changes the overall system design from direct classification to image-to-image verification.

---

# System Design 1

## Enrollment

The original concept was:

```text
Capture
   │
   ▼
Model Training
   │
   ▼
Store
```

## Inference

```text
Capture
   │
   ▼
Server
   │
   ├──────────────> Database
   │                    │
   │                    ▼
   │                Stored Images
   │                    │
   ▼                    │
  Model <────────────────┘
   │
   ▼
Compare Images
   │
   ▼
Similarity
```

Cosine similarity was also considered as a possible comparison/output method.

---

# System Design 2 — Current Direction

The newer design separates **sample collection** from **inference**.

## Enrollment / Sample Collection

Student information is attached to fingerprint samples:

```text
Name
Department
Matric
Samples
```

The intended flow is:

```text
Student Information + Samples
             │
             ▼
           Capture
             │
             ▼
          Database
```

The project also considers building a UI/algorithm that can determine whether a captured fingerprint image is good enough before adding it to the dataset.

## Inference / Deployment

```text
Captured Fingerprint
        │
        ▼
      Server
        │
        ▼
     Database
        │
        ▼
      Model
        │
        ▼
      Output
```

---

# Additional System Changes

The server implementation may need keypad/button controls for:

1. assigning IDs to students
2. reducing search time
3. avoiding the need to repeatedly use long matriculation numbers

One proposed idea is to generate a shorter integer ID that is unique to each student.

---

# Current Progress

- [x] Fingerprint image extraction
- [x] Initial system architecture
- [x] Enrollment concept
- [x] Verification concept
- [x] Siamese-network direction identified
- [ ] Final feature-extraction pipeline
- [ ] Dataset-quality checking
- [ ] Data augmentation strategy
- [ ] Siamese model implementation
- [ ] Similarity metric selection
- [ ] Training pipeline
- [ ] Deployment/inference pipeline

---

# Roadmap

```text
Fingerprint Capture
        │
        ▼
Image Preprocessing
        │
        ▼
Quality Check
        │
        ▼
Sample Collection
        │
        ▼
Database
        │
        ▼
Siamese Matching Model
        │
        ▼
Similarity
        │
        ▼
Fingerprint Verification
```

---

# Project Status

The project is currently in the **matching-algorithm and system-design stage**.

Fingerprint image extraction has already been addressed. The major remaining work is building and evaluating a reliable matching system, with the Siamese-network approach currently being the main direction.
