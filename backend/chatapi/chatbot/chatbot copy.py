from vector_db import initialize_vector_store
from utils import print_messages, format_docs
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import ChatMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from dotenv import load_dotenv
from operator import itemgetter
import yaml


load_dotenv()
chroma_db = initialize_vector_store()

# YAML 파일에서 프롬프트 불러오기
with open('prompts.yaml', 'r', encoding='utf-8') as file:
    prompts = yaml.safe_load(file)

def get_session_history(session_ids: str) -> BaseChatMessageHistory:
    print(session_ids)
    # if session_ids not in st.session_state["store"]:
    #     st.session_state["store"][session_ids] = ChatMessageHistory()
    # return st.session_state["store"][session_ids]

retriever = chroma_db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.7}
    )

def chatbot_response(user_input):

    model = ChatOpenAI(model='gpt-4o-mini', temperature=1)
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompts['system_prompt_1']),
        ('human', prompts['human_prompt_1']),
        ("ai", prompts['ai_prompt_1']),
        ("system", prompts['system_prompt_2']),
        ('human', prompts['human_prompt_2']),
        ("ai", prompts['ai_prompt_2']),
        ("system", prompts['system_prompt_3']),
        ('human', prompts['human_prompt_3']),
        ("ai", prompts['ai_prompt_3']),
        ("system", prompts['system_prompt_4']),
        ('human', prompts['human_prompt_4']),
        ("ai", prompts['ai_prompt_4']),
        MessagesPlaceholder(variable_name='history'),
        (
            'human', "{question}"),
        
        ])
        
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

    answer = chain_with_memory.invoke(
        {"question": user_input },
        config={"configurable": {"session_id": "abc123"}}
    )
    
    print("answer.content", answer.content)




    
    


