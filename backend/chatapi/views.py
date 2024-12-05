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
import time
import logging

client = OpenAI()

load_dotenv()

@method_decorator(csrf_exempt, name='dispatch')
class ChatBotView(APIView):
    
    # format_response 함수 추가
    def format_response(self, text):
        # 마크다운 볼드 표시와 줄바꿈 수정
        for i in range(1, 6):
            text = text.replace(f"{i}.\n**", f"{i}. ")
        return text.replace("**", "")    
    
    def post(self, request):
        print('request.data1:', request.data)
        user_message = request.data.get('message')
        
        # OpenAI API 호출 부분
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

            start_time = time.time()
            
            print(f"요청 받음: {request.data.get('message')}")
            
            # API 호출 전
            pre_api_time = time.time()

            bot_response = process_user_input(user_message, session_store, session_id)

            # bot_response = bot_response.replace('. ', '.\n')  # 문장 끝에서 줄바꿈
            bot_response = self.format_response(bot_response)

            # API 호출 후
            post_api_time = time.time()
            print("API 호출 시간: {:.2f}초".format(post_api_time - pre_api_time))
                        
            print("요청 받음:", request.data.get('message'))
            
            # 전체 처리 시간
            print("전체 처리 시간: {:.2f}초".format(time.time() - start_time))

            # print('response---->',response.choices[0].message.content)
            # bot_response = response.choices[0].message.content
            
            chat_message = ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)
            serializer = ChatMessageSerializer(chat_message)
        return Response(serializer.data)

