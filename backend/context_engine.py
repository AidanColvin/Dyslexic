from transformers import pipeline, AutoTokenizer, AutoModelForMaskedLM
from typing import List, Dict, Any, Optional
import torch
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = "distilroberta-base" # Fast and accurate for fill-mask
MAX_SEQ_LENGTH = 512 # BERT limit

class ContextRanker:
    """
    singleton class to manage the heavy transformer model
    handles caching, loading, and batch processing
    """
    _instance = None
    _pipeline = None
    _cache = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContextRanker, cls).__new__(cls)
            cls._load_model()
        return cls._instance

    @classmethod
    def _load_model(cls):
        """
        loads model to gpu if available, otherwise cpu
        """
        try:
            device = 0 if torch.cuda.is_available() else -1
            logger.info(f"Loading Context Model {MODEL_NAME} on device {device}...")
            
            cls._pipeline = pipeline(
                "fill-mask", 
                model=MODEL_NAME, 
                device=device,
                top_k=None # We want scores for specific targets, not generic top k
            )
            logger.info("Context Model Loaded.")
        except Exception as e:
            logger.error(f"Failed to load context model: {e}")
            cls._pipeline = None

    def rank_candidates(self, sentence: str, target_word: str, candidates: List[str]) -> List[Dict[str, Any]]:
        """
        ranks a list of candidate words based on how well they fit into the sentence
        uses masked language modeling probability
        """
        if not self._pipeline:
            # Fallback if model failed to load: return unranked
            return [{"word": w, "score": 0.0} for w in candidates]

        # 1. Input Sanitization
        candidates = [c for c in candidates if c.strip()]
        if not candidates:
            return []

        # 2. Create Masked Sentence
        # We must locate the target word and replace it with <mask>
        # This is a naive replacement; production would use token alignment
        if target_word not in sentence:
            # If target not found exactly, try case-insensitive
            pattern = re.compile(re.escape(target_word), re.IGNORECASE)
            masked_sentence = pattern.sub(self._pipeline.tokenizer.mask_token, sentence, count=1)
        else:
            masked_sentence = sentence.replace(target_word, self._pipeline.tokenizer.mask_token, 1)

        # 3. Windowing (Robustness for Long Texts)
        # BERT crashes on >512 tokens. We slice a window around the mask.
        masked_sentence = self._window_sentence(masked_sentence)

        # 4. Batch Inference
        # Ask BERT: "What is the probability of each candidate filling the mask?"
        try:
            results = self._pipeline(masked_sentence, targets=candidates)
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            return [{"word": w, "score": 0.0} for w in candidates]

        # 5. Process Results
        ranked_output = []
        
        # Pipeline returns dict for single target, list for multiple
        if isinstance(results, dict):
            results = [results]
            
        for res in results:
            ranked_output.append({
                "word": res['token_str'].strip(),
                "score": float(res['score']),
                "confidence_pct": round(float(res['score']) * 100, 2)
            })

        # Sort by confidence score descending
        return sorted(ranked_output, key=lambda x: x['score'], reverse=True)

    def _window_sentence(self, masked_sentence: str, context_size: int = 30) -> str:
        """
        trims sentence to keep the <mask> token and 'context_size' words around it
        prevents tensor size errors on long paragraphs
        """
        mask_token = self._pipeline.tokenizer.mask_token
        if mask_token not in masked_sentence:
            return masked_sentence
            
        words = masked_sentence.split()
        try:
            mask_index = words.index(mask_token)
        except ValueError:
            return masked_sentence
            
        start = max(0, mask_index - context_size)
        end = min(len(words), mask_index + context_size + 1)
        
        return " ".join(words[start:end])

# --- MODULE LEVEL INTERFACE ---

def load_context_model():
    """public initialization hook"""
    ContextRanker()

def rank_candidates_by_context(sentence: str, target_word: str, candidates: List[str]) -> List[Dict[str, Any]]:
    """public wrapper for rank logic"""
    ranker = ContextRanker()
    return ranker.rank_candidates(sentence, target_word, candidates)
