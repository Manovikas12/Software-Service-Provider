from django.views.generic.base import TemplateView

from django.shortcuts import render, redirect

import requests
from django.http import JsonResponse
import random
class MainPageView(TemplateView):
    template_name = 'demo/index.html'

from django.views.generic import TemplateView
import requests
from django.http import HttpResponse  # Import HttpResponse for debugging


class EmbedWebsiteView(TemplateView):
    template_name = 'demo/demoarea.html'

    def post(self, request, *args, **kwargs):
        url = request.POST.get('url_input')  # Update to match the field name in the form
        if url is None:
            return HttpResponse("Error: 'url_input' parameter not found in POST data.")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                return self.render_to_response({'html_content': html_content})
            else:
                error_message = f'Failed to fetch HTML content. Status code: {response.status_code}'
                return self.render_to_response({'error_message': error_message})
        except requests.RequestException as e:
            error_message = f'Failed to fetch HTML content. Error: {str(e)}'
            return self.render_to_response({'error_message': error_message})

# Inside your Django app's views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process_chat_message(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        bot_response = get_answer_for_question(user_input)
        return JsonResponse({'bot_response': bot_response})
    return JsonResponse({'error': 'Invalid request method'}, status=400)



import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list[str] = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None  # Return None if question not found in knowledge base

def chat_bot():
    knowledge_base: dict = load_knowledge_base('responses.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        questions = [q["question"] for q in knowledge_base["questions"]]
        best_match: str | None = find_best_match(user_input, questions)

        if best_match:
            answer: str | None = get_answer_for_question(best_match, knowledge_base)
            if answer:
                print(f'Bot: {answer}')
            else:
                print('Bot: I don\'t have an answer for that question.')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('responses.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()

