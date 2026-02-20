# 🌾 Pestaway  
### A Pest Management Chatbot with Integrated Speech Capability  
📍 IEEE TENCON 2025  
🏆 FUSERS 2025 • 1st Runner-up • Best Video Presentation  

---

## 📖 Overview

**Pestaway** is a bilingual conversational assistant designed to support Filipino farmers in pest identification and mitigation.

The system integrates:

- 🎙 Whisper (Speech-to-Text)
- 🧠 Fine-tuned SeaLLM (SFT / DPO / ORPO)
- 🔊 Google Text-to-Speech
- 🌐 English–Tagalog bilingual support

It enables natural voice or text interaction in field environments and supports deployment on modest hardware.

📄 **Paper:**  
https://ieeexplore.ieee.org/document/11375077

---

## 🗂 Repository Structure

```
.
├── README.md
├── docs/
│   ├── index.html
│   ├── architecture.png
│   ├── pestaway-gui.png
│   └── codes/
│       ├── sft_training.py
│       ├── orpo.py
│       ├── dpotrainer3.py
│       ├── evaluate_model.py
│       ├── data_metrics.py
│       ├── coh_metrixdpo.py
│       ├── coh_metrixsft.py
│       ├── coh_metrixqa.py
│       ├── WEReval.py
│       ├── cleaner.py
│       ├── count.py
│       ├── testing_gradio.py
│       └── requirements.txt
```

The project website is served via GitHub Pages from the `/docs` directory.

---

## 🚀 Reproducibility

### 1️⃣ Environment Setup

Create a virtual environment:

**macOS/Linux**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows**
```powershell
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r docs/codes/requirements.txt
```

---

### 2️⃣ Environment Variables

For security reasons, access tokens must NOT be hardcoded.

Set your Hugging Face token:

**macOS/Linux**
```bash
export HF_TOKEN="your_token_here"
```

**Windows PowerShell**
```powershell
setx HF_TOKEN "your_token_here"
```

Restart your terminal after setting environment variables.

---

### 3️⃣ Dataset Configuration

Set dataset paths:

**macOS/Linux**
```bash
export TRAIN_PARQUET="./data/train.parquet"
export TEST_PARQUET="./data/test.parquet"
```

**Windows PowerShell**
```powershell
setx TRAIN_PARQUET ".\data\train.parquet"
setx TEST_PARQUET ".\data\test.parquet"
```

Datasets are not included in this repository.

---

### 4️⃣ Training

Run Supervised Fine-Tuning (SFT):

```bash
python docs/codes/sft_training.py
```

Run ORPO:

```bash
python docs/codes/orpo.py
```

Run DPO:

```bash
python docs/codes/dpotrainer3.py
```

---

### 5️⃣ Evaluation

```bash
python docs/codes/evaluate_model.py
```

Metrics computed:

- 📊 METEOR  
- 📈 BERTScore  
- 📉 Average Perplexity  
- 🔎 Coh-Metrix features  

---

## 📊 Experimental Setup

- Base Model: SeaLLM-v3-1.5B-Chat  
- Fine-tuning Strategies: SFT, DPO, ORPO  
- Evaluation Metrics: Translation quality, semantic similarity, perplexity  
- Hardware: Single-GPU training environment  

---

## 🛡 Security & Data Policy

- No access tokens included  
- No private datasets included  
- No model weights included  
- Users must provide their own credentials and datasets  

---

## 🙏 Acknowledgment

This research was conducted at the Department of Electronics Engineering,  
Faculty of Engineering, University of Santo Tomas.

We thank Bulacan Agricultural State College and the local farming communities in Bulacan for their support and collaboration.

---

## 📜 Citation

If you find this work useful, please consider citing:

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

## ⭐ Support

If this repository supports your research or extension work, please consider starring the project.
