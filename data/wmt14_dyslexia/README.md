---
license: cc-by-sa-4.0
language:
- en
- fr
tags:
- dyslexia
- neurips24
- machine translation
- MT
---
## Dataset Summary
The WMT14 injected synthetic dyslexia dataset is a modified version of the WMT14 English test set. This dataset was created to test the capabilities of SOTA machine translations models on dyslexic style text. This research was supported by [AImpower.org](https://aimpower.org/).
## How the data is structured
- In "Data/French_translated_data", each file within the dataset consists of a “.txt” or “.docx” file containing the translated sentences from AWS, Google, Azure and OpenAI.
- In "Data/French_translated_data", each line in every file represents a translated sentence. 
- The file names indicate the type of synthetic injection that was done to the English version and the associated injection probability.
- The "Data/English_input_data" directory consists of the English versions that were submitted to the translation services.
- Each file is the same but with different varying levels/types of injections. E.g. the file name "wmt14_en_p_homophone_0.2_p_letter_0.0_p_confusing_word_0.0" has a probability of 20% to inject a homophone in a sentence, 0 % of injecting a confusing letter and 0% to inject a confusing word.
- The injection process can be found [here](https://github.com/aimpowered/NLPdisparity/blob/main/Injecting_Dyslexia.ipynb)

The related github repository can be found [here](https://github.com/aimpowered/NLPdisparity)