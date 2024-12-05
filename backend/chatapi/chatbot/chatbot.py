# chatbot.py
from operator import itemgetter
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import ChatMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import yaml
from .vector_db import initialize_vector_store
from .utils import format_docs
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# Chroma 데이터베이스 초기화
chroma_db = initialize_vector_store()

# YAML 파일에서 프롬프트 불러오기
with open(os.path.abspath('chatapi/chatbot/prompts.yaml'), 'r', encoding='utf-8') as file:
    prompts = yaml.safe_load(file)

def get_session_history(session_store, session_ids: str) -> BaseChatMessageHistory:
    """
    세션 ID에 해당하는 채팅 메시지 히스토리를 반환합니다.
    세션 ID가 없으면 새로운 히스토리를 생성합니다.
    """
    if session_ids not in session_store:
        session_store[session_ids] = ChatMessageHistory()
    return session_store[session_ids]

def create_chain(prompts, retriever, format_docs, prompt, model, get_session_history):
    """
    주어진 프롬프트, 리트리버, 포맷 함수, 모델, 세션 히스토리 함수를 사용하여 체인을 생성합니다.
    """
    chain = (
        {
            'context': itemgetter('question') | retriever | format_docs,
            'question': itemgetter('question'),
            'history': itemgetter('history'),
        }
        | prompt
        | model
    )

    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key='question',
        history_messages_key='history'
    )
    return chain_with_memory

def run_chain(chain_with_memory, question, history, session_id):
    """
    주어진 체인과 입력 데이터를 사용하여 체인을 실행하고 결과를 반환합니다.
    """
    input_data = {
        'question': question,
        'history': history
    }
    config = {
        'configurable': {
            'session_id': session_id
        }
    }
    return chain_with_memory.invoke(input_data, config=config)

def process_user_input(user_input, session_store, session_id):
    """
    사용자 입력을 처리하고 응답을 생성합니다.
    """
    # 리트리버 초기화
    retriever = chroma_db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.7}
    )

    # 모델 및 프롬프트 초기화
    model = ChatOpenAI(model='gpt-4o-mini', temperature=0.3)
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompts['system_prompt_1']),
        ('human', prompts['human_prompt_1']),
        ("ai", prompts['ai_prompt_1']),
       
        MessagesPlaceholder(variable_name='history'),
        ('human', "{question}"),
    ])

    # 체인 생성 및 실행
    chain_with_memory = create_chain(prompts, retriever, format_docs, prompt, model, lambda x: get_session_history(session_store, x))
    answer = run_chain(chain_with_memory, user_input, session_store.get(session_id, []), session_id)

    return answer.content