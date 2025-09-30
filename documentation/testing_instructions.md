# Testing Instructions for Audio Analysis Tools

This document outlines the setup and usage of the test files located in the `tests` directory.

## Directory Structure

The `tests` directory contains the following files and folders:

- **audio_samples/**
- **crisis_toolchain_test.py**
- **test_wer.py**
- **transcripts/**
- **wer_results.txt**

## Prerequisites

Before running the test scripts, ensure the following steps are completed:

1. **Install Dependencies**:
   - Install all required dependencies listed in the `requirements.txt` file. Run the following command in your terminal:
     ```bash
     pip install -r requirements.txt
     ```

2. **Set Up API Keys**:
   - Ensure all necessary API key variables are properly configured and loaded in your environment. Test files rely on OpenAI API keys.

## Test Scripts Overview

- **`test_wer.py`**:
  - Purpose: Generates a Word Error Rate (WER) report to evaluate transcription accuracy.
  - Output: Results are saved in `wer_results.txt` (in tests dir) and ``wer_report.md` (in documentation dir)`.

- **`crisis_toolchain_test.py`**:
  - Purpose: Tests the crisis toolchain, which evaluates user input based on intent and emotion.
  - Note: The specific numerical values assigned to risk levels are not critical for testing purposes.
