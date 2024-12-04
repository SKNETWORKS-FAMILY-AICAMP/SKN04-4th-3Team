from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
# from python_decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ChatMessageSerializer
from .models import ChatMessage
from openai import OpenAI
import os
from dotenv import load_dotenv
from django.utils.decorators import method_decorator
from .chatbot.chatbot import process_user_input
client = OpenAI()

load_dotenv()


@method_decorator(csrf_exempt, name='dispatch')
class ChatBotView(APIView):
    def post(self, request):
        print('request.data1:', request.data)
        user_message = request.data.get('message')
        
        if request.method == 'POST':
            # openai.api_key = os.getenv('OPENAI_API_KEY')
            
            # response = client.chat.completions.create(
            #     model="gpt-4o-mini",
            #     messages=[
            #         {"role": "system", "content": "You are a helpful assistant."},
            #         {"role": "user", "content": user_message}
            #     ]
            # )
            session_store = {}
            session_id = "test-session"

            bot_response = process_user_input(user_message, session_store, session_id)

            # print('response---->',response.choices[0].message.content)
            # bot_response = response.choices[0].message.content
            
            chat_message = ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)
            serializer = ChatMessageSerializer(chat_message)
        return Response(serializer.data)
