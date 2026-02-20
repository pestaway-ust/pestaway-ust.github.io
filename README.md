<h1 align="center">Pestaway</h1>

<p align="center">
  <strong>Pest Management Chatbot with Integrated Speech Capability</strong>
</p>

<p align="center">
  IEEE TENCON 2025 &nbsp;•&nbsp; FUSERS 2025 1st Runner-Up
</p>

<p align="center">
  <a href="https://ieeexplore.ieee.org/document/11375077">Paper</a> |
  <a href="https://pestaway-ust.github.io/">Project Page</a> |
  <a href="https://github.com/pestaway-ust/pestaway-ust.github.io/tree/main/docs/codes">Code</a>
</p>

---

## Overview

Pestaway is a bilingual (English–Tagalog) conversational assistant designed to support Filipino farmers in pest identification and safe mitigation. The system integrates speech recognition, large language model fine-tuning, and text-to-speech generation to enable natural multimodal interaction in field environments.

Core components:

- Whisper (Speech-to-Text)
- SeaLLM-v3-1.5B-Chat (fine-tuned via SFT, DPO, ORPO)
- Google Text-to-Speech

The system is designed for accessibility, modest hardware deployment, and practical agricultural use.

---

## System Architecture

<p align="center">
  <img src="docs/architecture.png" width="900">
</p>

---

## User Interface

<p align="center">
  <img src="docs/pestaway-gui.png" width="900">
</p>

---

## Repository Structure

```
.
├── README.md
└── docs/
    ├── index.html
    ├── architecture.png
    ├── pestaway-gui.png
    └── codes/
        ├── sft_training.py
        ├── orpo.py
        ├── dpotrainer3.py
        ├── evaluate_model.py
        ├── data_metrics.py
        ├── coh_metrix*.py
        ├── WEReval.py
        ├── cleaner.py
        ├── count.py
        ├── testing_gradio.py
        └── requirements.txt
```

GitHub Pages is served from the `/docs` directory.

---

## Reproducibility

### Environment Setup

```bash
python -m venv venv
source venv/bin/activate          # macOS / Linux
# or
venv\Scripts\activate             # Windows

pip install -r docs/codes/requirements.txt
```

### Environment Variables

```bash
export HF_TOKEN="your_huggingface_token"
export TRAIN_PARQUET="./data/train.parquet"
export TEST_PARQUET="./data/test.parquet"
```

Windows PowerShell:

```powershell
setx HF_TOKEN "your_huggingface_token"
setx TRAIN_PARQUET ".\data\train.parquet"
setx TEST_PARQUET ".\data\test.parquet"
```

Datasets and model weights are not included.

---

## Training

```bash
python docs/codes/sft_training.py
python docs/codes/orpo.py
python docs/codes/dpotrainer3.py
```

---

## Evaluation

```bash
python docs/codes/evaluate_model.py
```

Evaluation metrics include:

- METEOR
- BERTScore
- Average Perplexity
- Coh-Metrix features

---

## Results

| Method     | METEOR | BERTScore | Avg. Perplexity |
|------------|--------|-----------|-----------------|
| SFT        | 0.2909 | 0.6250    | 2.6040          |
| SFT + DPO  | 0.2896 | 0.6596    | 2.0501          |
| ORPO       | **0.3271** | **0.7316** | **1.5185** |

---

## Citation

```bibtex
@inproceedings{delacruz2025pestaway,
  title     = {Pestaway: A Pest Management Chatbot with Integrated Speech Capability},
  author    = {Dela Cruz, Rachel Hannah C. and Aguarin, Joshua Carlo C. and
               Ling, Nickolas Chase P. and Magsaysay, Maveric S. and
               Villanueva, Jastin Brylle C. and Pangaliman, Ma. Madecheen S.},
  booktitle = {2025 IEEE Region 10 Conference (TENCON)},
  year      = {2025},
  month     = {October},
  address   = {Kota Kinabalu, Sabah, Malaysia},
  doi       = {10.1109/TENCON66050.2025.11375077},
  url       = {https://ieeexplore.ieee.org/document/11375077}
}
```

---

## Acknowledgment

Department of Electronics Engineering  
Faculty of Engineering  
University of Santo Tomas  
Bulacan Agricultural State College and collaborating farming communities
