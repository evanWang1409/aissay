"""Test module for OpenAIUtils class."""
import argparse
from src.agents.writer_agent import WriterAgent
from src.utils.gptzero_utils import GPTZeroUtils
from src.utils.test.gptzero_utils_test import test_gptzero_utils
import json
import os
import time

test_config_path = "configs/test/test_input.json"
PASSWORD = None


def agent_conversation(agent):
    while True:
        user_input = input("You: ")
        if user_input == "exit":
            break
        response = agent.generate_response(user_input)
        print("Assistant: ", response)
        
def get_test_writer_agent():
    # read test config
    with open(test_config_path, "r", encoding="utf-8") as f:
        test_config = json.load(f)
    # Need to run from main directory
    student_context_path = os.path.join(os.getcwd(), test_config["student_context"]['student_1']) #change student context 
    essay_prompt = test_config["essay_prompt"]['mit_personal_journey'] #change essay prompt
    style_preference_path = os.path.join(os.getcwd(), test_config["style_preference"]['style_preference_1'])
    student_context = open(student_context_path, "r", encoding="utf-8").read()
    style_preference = open(style_preference_path, "r", encoding="utf-8").read()
    writing_context = {
        "student_context": student_context,
        "essay_prompt": essay_prompt,
        "style_preference": style_preference
    }
        
    # initialize writer agent
    writer_agent = WriterAgent("configs/agents/writer_agent.json", PASSWORD)
    writer_agent.set_writing_context(writing_context)
    
    return writer_agent


def test_writer_agent():
    writer_agent = get_test_writer_agent()
    
    # writer_agent.execute_action("generate_outline")
    # print(f"Outline: {writer_agent.latest_response}")
    writer_agent.execute_action("write")
    print(f"Essay: {writer_agent.latest_response}")
    
    # print(f"Time taken: {time.time() - start_time} seconds")
    return writer_agent.latest_response
    
def test_write_and_detect(num_iter: int = 3):
    writer_agent = get_test_writer_agent()
    gptzero_util = GPTZeroUtils(PASSWORD, 0.8)
    
    writer_agent.execute_action("write")
    result = gptzero_util.analyze_text(writer_agent.latest_response)
    sentences_prob = gptzero_util.get_sentence_ai_probabilities(result)
    print("@@@@ Iteration 1 @@@@\n")
    print("-"*100, "\n")
    print(writer_agent.latest_response)
    print("="*100, "\n")
    print("Sentences Pred: ", sentences_prob)
    print("-"*100, "\n")
    
    for i in range(num_iter):
        prompt = "This version is too ai. Rewrite it to be more human and avoid common ai writing patterns and phrases." #change prompt to add humanize instruction
        writer_agent.generate_response(prompt)
        result = gptzero_util.analyze_text(writer_agent.latest_response)
        sentences_prob = gptzero_util.get_sentence_ai_probabilities(result)
        print(f"@@@@ Iteration {i+2} @@@@\n")
        print("-"*100, "\n")
        print(writer_agent.latest_response)
        print("="*100, "\n")
        print("Sentences Pred: ", sentences_prob)
        print("-"*100, "\n")
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--password', '-p',
                       required=True,
                       help='Password for encryption/decryption')
    PASSWORD = parser.parse_args().password
    test_write_and_detect(1)