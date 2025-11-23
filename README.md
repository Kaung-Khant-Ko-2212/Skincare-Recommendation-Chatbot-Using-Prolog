# Skincare-Recommendation-Chatbot-Using-Prolog
The Skincare Recommendation Chatbot is a Python program that uses a Prolog knowledge base to provide personalized skincare routine tips and product suggestions based on a user's specified skin type.

---

## Table of Contents

- Overview
- Features
- Repo layout
- Requirements
- Quick start
- Data & model notes
- Development
- Contributing
- License
- External link

---

## Overview

This repository is part of a multi-repo project that classifies skin types from images. It contains small scripts and helpers (Perl/Python) that were used during development and testing. Use this repository for quick local checks or to integrate simple tooling into the larger project.

## Features

- Lightweight utilities for dataset sanity checks and experiment scaffolding.
- Quick test script for environment verification (`Test.py`).
- Minimal, portable scripts intended for cross-platform use.

## Repo layout

- `skincare.pl` — Perl utility script (processing or automation helper).
- `skincare.pl~` — editor/backup copy.
- `Test.py` — Python test / quick-run example used during development.

## Requirements

- Perl (5.x) — for `skincare.pl`.
- Python 3.8+ — for `Test.py` and any Python-based helpers.
- Optional: `pip` for installing Python dependencies if you extend `Test.py`.

## Quick start

1. Clone or download this repo:

  ```powershell
  cd 'C:\path\to\your\workspace'
  git clone <this-repo-url>
  cd skincare
  ```

2. Run the Perl utility (example):

  ```powershell
  perl .\skincare.pl
  ```

3. Run the Python test:

  ```powershell
  python .\Test.py
  ```

Adjust the commands depending on your environment and scripts' expected arguments.

## Data & model notes

- This repository does not contain the main dataset or trained models. It is intended to complement the main project where dataset curation, model training, and frontend inference live.
- For details on the dataset, training setup, model architecture, and evaluation metrics, see the main project repository linked below.

## Development

- To extend this repository, create well-documented scripts and add unit tests where appropriate.
- If you add Python dependencies, include a `requirements.txt` or `pyproject.toml`.

Development checklist (suggested):

- [ ] Add `requirements.txt` for Python dependencies.
- [ ] Add usage examples for each script.
- [ ] Add automated tests for helper utilities.

## Contributing

Contributions are welcome. Please open issues for bugs or feature requests and submit pull requests for fixes and improvements. Keep changes small and documented.

## License

This repository does not include a license file yet. Add a `LICENSE` (e.g., MIT) if you want to define reuse rights.

## External link

The frontend and the primary project (dataset, training, and inference code) are available here:

https://github.com/taite-ang-saiyin/Skin-Type-Classification

---
