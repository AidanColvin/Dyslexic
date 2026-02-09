---
language:
- si
license: cc-by-4.0
task_categories:
- text-generation
tags:
- sinhala
- dyslexia
- spelling-correction
- grammar-correction
- mbart
- text-normalization
---

# Sinhala Dyslexia Corrected (ID20)

This dataset is an augmented version of  
`SPEAK-ASR/akura-sinhala-dyslexia-corrected`, designed for training
robust sequence-to-sequence dyslexia correction models for Sinhala.

## Motivation
Neural text correction models (e.g., mBART, mT5) tend to over-correct
inputs that are already well-formed. To mitigate this behavior, we
introduce identity mappings that explicitly teach the model when **no
correction is required**.

## Dataset Construction
The dataset contains two types of sentence pairs:

1. **Correction pairs (original data)**  
   - `dyslexic_sentence → clean_sentence`

2. **Identity pairs (added augmentation)**  
   - `clean_sentence → clean_sentence`  
   - These identity pairs constitute **20% of the dataset**
   - Identity samples are labeled with `error_type = "no_error"`

All identity pairs are derived from the original clean sentences and
randomly sampled to preserve linguistic diversity.

## Fields
- `dyslexic_sentence` (string):  
  Input sentence containing dyslexic or noisy text, or a clean sentence
  in the case of identity mappings.
- `clean_sentence` (string):  
  Gold corrected Sinhala sentence.
- `error_type` (string):  
  Dyslexia-related error category or `no_error` for identity pairs.

## Intended Use
- Fine-tuning sequence-to-sequence correction models (mBART, mT5)
- Dyslexia-aware spelling and grammar correction
- Reducing over-correction in neural correction systems

## Notes
This dataset preserves backward compatibility with the original
column structure, allowing it to be used as a drop-in replacement
for existing training pipelines.
