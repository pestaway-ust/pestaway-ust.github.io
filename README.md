# 🌾 Pestaway  
### *Pest Management Chatbot with Integrated Speech Capability*

[![IEEE TENCON 2025 Accepted](https://img.shields.io/badge/🎓-TENCON%202025%20Accepted-blue)](https://ieeexplore.ieee.org/document/11375077)
[![FUSERS 2025 • Runner-up](https://img.shields.io/badge/🏆-FUSERS%202025%201st%20Runner%20Up-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

<p align="center">
  <img src="docs/pestaway-gui.png" alt="Pestaway UI Screenshot" width="60%">
</p>

---

## 📌 About

**Pestaway** is an interactive, bilingual chatbot (English & Tagalog) that helps Filipino farmers:

- 🐛 identify agricultural pests
- 📘 learn safe mitigation strategies
- 🎙 interact with natural speech input/output

It combines state-of-the-art components — Whisper STT, SeaLLM fine-tuning, and Google TTS — for a seamless field experience. :contentReference[oaicite:0]{index=0}

---

## 🧠 Features

- 🗣️ Speech-enabled conversational pest support  
- 🔡 Text and voice interaction (English & Tagalog)  
- 📊 Evaluation metrics: METEOR, BERTScore, perplexity, Coh-Metrix  
- 🛠️ Modular training pipeline for SFT, DPO, ORPO

---

## 📂 Repository Layout

```
📦 pestaway-ust.github.io
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

---

## 🚀 Quick Start

### 🐍 Setup

Create a Python environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate            # macOS / Linux
venv\Scripts\activate               # Windows PowerShell

pip install -r docs/codes/requirements.txt
```

---

## 🔐 Environment Variables

⚠️ Tokens must NOT be hard-coded.

**macOS / Linux**
```bash
export HF_TOKEN="your_huggingface_token"
```

**Windows PowerShell**
```powershell
setx HF_TOKEN "your_huggingface_token"
```

---

## 🧪 Training & Evaluation

Train with different strategies:

- 🟦 Supervised Fine-Tuning (SFT)
```bash
python docs/codes/sft_training.py
```

- 🟨 ORPO
```bash
python docs/codes/orpo.py
```

- 🟩 DPO
```bash
python docs/codes/dpotrainer3.py
```

Evaluate with:
```bash
python docs/codes/evaluate_model.py
```

---

## 🧾 Results

| Method      | METEOR | BERTScore | Perplexity |
|-------------|--------|-----------|------------|
| SFT         | 0.2909 | 0.6250    | 2.6040     |
| SFT + DPO   | 0.2896 | 0.6596    | 2.0501     |
| ORPO        | **0.3271** | **0.7316** | **1.5185** |

---

## 📖 Paper & Citation

📄 **Pestaway: A Pest Management Chatbot with Integrated Speech Capability**  
Accepted at IEEE Region 10 Conference (TENCON 2025)

Cite as:

```bibtex
@inproceedings{delacruz2025pestaway,
  title     = {Pestaway: A Pest Management Chatbot with Integrated Speech Capability},
  author    = {Dela Cruz, Rachel Hannah C. and Aguarin, Joshua Carlo C. and Ling, Nickolas Chase P. and
               Magsaysay, Maveric S. and Villanueva, Jastin Brylle C. and Pangaliman, Ma. Madecheen S.},
  booktitle = {2025 IEEE Region 10 Conference (TENCON)},
  year      = {2025},
  month     = {October},
  address   = {Kota Kinabalu, Sabah, Malaysia},
  doi       = {10.1109/TENCON66050.2025.11375077},
  url       = {https://ieeexplore.ieee.org/document/11375077}
}
```

---

## 📫 Contact

**Team Pestaway** — University of Santo Tomas  
Feel free to open issues, discuss, or contribute.

---

## ⭐ Support

If you find this useful, please ⭐ the repo!
