QUESTIONS = [
    {
        "category": "Behavioral",
        "question": "Tell me about a time you had to manage conflicting priorities.",
        "keywords": ["prioritize", "communicate", "deadline", "manager", "urgent", "schedule", "impact"]
    },
    {
        "category": "System Design",
        "question": "How would you design a highly available and scalable web application?",
        "keywords": ["load balancer", "database", "cache", "microservices", "horizontal scaling", "redundancy", "latency"]
    },
    {
        "category": "Teamwork",
        "question": "Describe a situation where you disagreed with a team member. How did you handle it?",
        "keywords": ["listen", "compromise", "empathy", "perspective", "solution", "discussed", "respect"]
    },
    {
        "category": "Problem Solving",
        "question": "Walk me through a time when you had to learn a new technology or tool quickly.",
        "keywords": ["documentation", "hands-on", "tutorial", "practice", "applied", "fast", "adapt"]
    },
    {
        "category": "Behavioral",
        "question": "Tell me about a time you failed and what you learned from the experience.",
        "keywords": ["accountability", "mistake", "learned", "improve", "prevent", "responsibility", "growth"]
    }
]

def get_all_questions():
    """Returns the entire bank of questions."""
    return QUESTIONS