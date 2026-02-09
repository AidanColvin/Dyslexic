---
dataset_name: grammar-correction
description: >
  A refined subset of the liweili/c4_200m dataset, derived from Google's C4_200M
  Synthetic Dataset for Grammatical Error Correction.  Contains sentence pairs
  where the input is ungrammatical and the output is grammatical, suitable for
  training grammatical error correction (GEC) models.
train_size: 100000
validation_size: 25000
data_fields:
- input: Ungrammatical sentence (string)
- output: Corrected, grammatical sentence (string)
intended_uses: >
  Designed for training and evaluating GEC models to automatically identify and
  correct grammatical errors in text.
limitations:
- Synthetic data may not fully capture real-world grammatical errors.
- Filtering may introduce biases based on classifier performance.
- >-
  Focused on English grammar, limiting applicability to other languages or
  dialects.
task_categories:
- text2text-generation
- text-classification
language:
- en
tags:
- gec
- grammar
---
# grammar-correction

## Dataset Summary

The grammar-correction dataset is a refined subset of the [liweili/c4_200m](https://huggingface.co/datasets/liweili/c4_200m) dataset, 
derived from Google's [C4_200M Synthetic Dataset for Grammatical Error Correction](https://github.com/google-research-datasets/C4_200M-synthetic-dataset-for-grammatical-error-correction). 
It contains sentence pairs where the input is ungrammatical and the output is grammatical, making it suitable for training grammatical error correction (GEC) models.

## Dataset Structure

- **Train set**: 100&thinsp;000 entries
- **Validation set**: 25&thinsp;000 entries

### Data Fields

- **input**: Ungrammatical sentence (string)
- **output**: Corrected, grammatical sentence (string)

## Dataset Creation

### Source Data

This dataset is based on the liweili/c4_200m dataset, which includes 185 million sentence pairs generated from a cleaned English corpus.

### Filtering Methodology

Entries were filtered using the [agentlans/snowflake-arctic-xs-grammar-classifier](https://huggingface.co/agentlans/snowflake-arctic-xs-grammar-classifier) 
to retain only those with ungrammatical inputs and grammatical outputs, enhancing the quality of training data for GEC tasks.

## Considerations for Using the Data

### Intended Uses

Designed for training and evaluating GEC models to automatically identify and correct grammatical errors in text.

### Limitations and Biases

1. The dataset is synthetic and may not fully capture real-world grammatical errors.
2. Filtering may introduce biases based on classifier performance.
3. Focused on English grammar, limiting applicability to other languages or dialects.

## Additional Information

### Dataset Curators

- Curated by filtering the liweili/c4_200m dataset, based on Google's C4_200M dataset.
- Please check the licenses of those datasets for usage rights.
- Also acknowledge the use of the agentlans/snowflake-arctic-xs-grammar-classifier for filtering.

### Contributions

This dataset aims to provide high-quality resources for GEC model training and evaluation, building on the efforts of Google Research and the Hugging Face community.