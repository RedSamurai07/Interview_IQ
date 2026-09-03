import re
from langchain_core.tools import tool

# detecting filler words
@tool
def detect_filler_words(text: str) -> dict:
    """Detects common filler words such as 'um', 'like', and 'basically' in the candidate's answer."""
    fillers = [
        'um', 'uh', 'like', 'you know', 'basically', 'actually', 'literally',
        'i mean', 'so', 'well', 'right', 'okay', 'just', 'kind of', 'sort of',
        'you see', 'i guess', 'i suppose', 'i think', 'i feel', 'i believe'
    ]
    answer_lower = text.lower()
    # Safely count exact phrase matches in the lowercase text
    found_fillers = {filler: answer_lower.count(filler) for filler in fillers if answer_lower.count(filler) > 0}

    return {
        "tool": "detect_filler_words",
        "filler_words": found_fillers,
        "total_fillers": sum(found_fillers.values()),
        "flagged": len(found_fillers) > 0
    }

# detect repetitive phrases
@tool
def detect_repetitive_phrases(text: str) -> dict:
    """Detects repetitive phrases in the candidate's answer."""
    phrases = re.findall(r'\b(\w+\s+\w+)\b', text.lower())
    phrase_counts = {phrase: phrases.count(phrase) for phrase in set(phrases) if phrases.count(phrase) > 1}

    return {
        "tool": "detect_repetitive_phrases",
        "repetitive_phrases": phrase_counts,
        "total_repetitions": sum(phrase_counts.values()),
        "flagged": len(phrase_counts) > 0
    }

# detecting long sentences
@tool
def detect_long_sentences(text: str) -> dict:
    """Detects long sentences in the candidate's answer."""
    sentences = re.split(r'[.!?]', text)
    long_sentences = [sentence.strip() for sentence in sentences if len(sentence.split()) > 20]

    return {
        "tool": "detect_long_sentences",
        "long_sentences": long_sentences,
        "total_long_sentences": len(long_sentences),
        "flagged": len(long_sentences) > 0
    }

# detecting long pauses
@tool
def detect_long_pauses(text: str) -> dict:
    """Detects long pauses in the candidate's answer."""
    long_pauses = re.findall(r'(\.\.\.|---)', text)
    
    return {
        "tool": "detect_long_pauses",
        "long_pauses": len(long_pauses),
        "flagged": len(long_pauses) > 0
    }

# checks if answers are in STAR structure format
@tool
def check_star_structure(text: str) -> dict:
    """Checks if the candidate's answer follows the STAR (Situation, Task, Action, Result) structure."""
    answer_lower = text.lower()

    components = {
        "Situation": any(w in answer_lower for w in ["situation", "context", "background", "when i was"]),
        "Task": any(w in answer_lower for w in ["task", "goal", "objective", "needed", "assigned"]),
        "Action": any(w in answer_lower for w in ["action", "steps", "what i did", "how i handled", "created"]),
        "Result": any(w in answer_lower for w in ["result", "outcome", "achieved", "increased", "decreased"])
    }

    present = [k for k, v in components.items() if v]
    missing = [k for k, v in components.items() if not v]

    return {
        "tool": "check_star_structure",
        "components_present": present,
        "components_missing": missing,
        "is_complete_star": len(missing) == 0
    }

# Score based on the presence of expected keywords
@tool
def score_relevance(text: str, expected_keywords: list) -> dict:
    """Scores the relevance of the candidate's answer based on the presence of the expected keywords."""
    if not expected_keywords:
        return {"tool": "score_relevance", "score": 0, "matched_keywords": [], "missing_keywords": []}

    answer_lower = text.lower()
    matched = [keyword for keyword in expected_keywords if keyword.lower() in answer_lower]
    missing = [keyword for keyword in expected_keywords if keyword.lower() not in answer_lower]
    
    score = int((len(matched) / len(expected_keywords)) * 100)

    return {
        "tool": "score_relevance",
        "matched_keywords": matched,
        "missing_keywords": missing,
        "relevance_score": score    
    }