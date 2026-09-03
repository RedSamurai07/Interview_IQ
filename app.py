import gradio as gr
from interview_bank import QUESTIONS as INTERVIEW_BANK

# A dummy mock bank of questions (In reality, import from interview_bank.py as required)
INTERVIEW_BANK = [
    {"question": "Tell me about a time you had to scale a system.", "keywords": ["database", "architecture", "load balancing"]},
    {"question": "How do you handle conflict in a team?", "keywords": ["communication", "empathy", "resolution"]},
    {"question": "Describe a time you failed.", "keywords": ["learned", "accountability", "improved"]}
]

current_question_idx = 0
scorecard_data = []

def get_current_question():
    """Returns the current question text."""
    if current_question_idx < len(INTERVIEW_BANK):
        return INTERVIEW_BANK[current_question_idx]["question"]
    return "Interview Complete! Generate your final report."

def submit_answer(answer):
    """Processes the candidate's answer, gets feedback, and updates the scorecard."""
    global current_question_idx
    
    if current_question_idx >= len(INTERVIEW_BANK):
        return "Interview is over.", scorecard_data, get_current_question()
        
    current_q = INTERVIEW_BANK[current_question_idx]["question"]
    expected_kw = INTERVIEW_BANK[current_question_idx]["keywords"]
    
    # 1. Call the Agent (Uncomment when agent.py is ready)
    # feedback = coach.evaluate(current_q, answer, expected_kw)
    feedback = f"Mock Feedback for: {answer}" # Placeholder
    
    # 2. Update Scorecard 
    # (In a real scenario, you could fetch the specific score from coach.session_data)
    scorecard_data.append([current_q, answer, "Evaluated"]) 
    
    # 3. Advance to next question
    current_question_idx += 1
    
    return feedback, scorecard_data, get_current_question()

def ask_meta_question(question):
    """Passes a meta-question to the agent using session history."""
    # response = coach.ask_agent(question)
    response = "Mock Response: You are doing great, but focus on the STAR method!" # Placeholder
    return response

def generate_report():
    """Generates the final aggregated report."""
    # report = coach.generate_final_report()
    # return f"Average Score: {report['average_relevance_score']}\nWeakest Area: {report['weakest_area']}"
    return "Mock Final Report\nAverage Score: 85\nWeakest Area: Conflict Resolution" # Placeholder

# Building the Gradio Interface
with gr.Blocks(title="InterviewIQ Coach") as demo:
    gr.Markdown("# InterviewIQ - AI Mock Interview Coach")
    
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### Current Question")
            question_display = gr.Markdown(f"**{get_current_question()}**")
            
            answer_input = gr.Textbox(label="Your Answer", lines=5, placeholder="Type your answer here...")
            submit_btn = gr.Button("Submit Answer", variant="primary")
            
            feedback_output = gr.Textbox(label="Coach Feedback", lines=3, interactive=False)
            
        with gr.Column(scale=1):
            gr.Markdown("### Live Scorecard")
            scorecard_display = gr.Dataframe(
                headers=["Question", "Answer Snippet", "Status"], 
                value=scorecard_data,
                interactive=False
            )
            
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Ask the Coach (Mid-Session)")
            meta_input = gr.Textbox(label="Ask a question (e.g., 'How am I doing?')", lines=1)
            meta_btn = gr.Button("Ask")
            meta_output = gr.Textbox(label="Coach Response", lines=2, interactive=False)
            
        with gr.Column():
            gr.Markdown("### Final Evaluation")
            report_btn = gr.Button("Generate Final Report", variant="stop")
            report_output = gr.Textbox(label="Aggregated Report", lines=4, interactive=False)

    # Wire up the button clicks to the functions
    submit_btn.click(
        fn=submit_answer, 
        inputs=answer_input, 
        outputs=[feedback_output, scorecard_display, question_display]
    )
    
    meta_btn.click(
        fn=ask_meta_question,
        inputs=meta_input,
        outputs=meta_output
    )
    
    report_btn.click(
        fn=generate_report,
        inputs=None,
        outputs=report_output
    )

if __name__ == "__main__":
    # Run the application
    demo.launch()