import os
from tqdm import tqdm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import re

# 환경변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def load_data(folder_path):
    """
    지정된 폴더에서 PDF 파일을 로드하여 문서 목록을 반환
    """
    documents = []
    for filename in tqdm(os.listdir(folder_path), desc="loading PDF"):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            try:
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                documents.append(docs)
                print(f"{filename}에서 {len(documents)}번째의 문서를 로드했습니다.")
            except Exception as e:
                print(f"{filename} 로드 중 오류 발생: {e}")
    return documents

def data_cleaning(documents):
    # 문서 내용 정제
    for page in documents:
        page_content = page.page_content
        page_content = re.sub(r'\s+', ' ', page_content)  # 여러 줄바꿈, 공백을 하나로 줄임
        page_content = re.sub(r'[^\w\s가-힣]', '', page_content)  # 한글, 영문자, 숫자, 공백만 남기고 제거
        page_content = page_content.strip()
        page.page_content = page_content
    # 빈 페이지 제거
    filtered_documents = [doc for doc in documents if doc.page_content.strip()]
    
    return filtered_documents

def build_vector_store():
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY가 설정되지 않았습니다.")
        print("1. .env 파일에 OPENAI_API_KEY=your-api-key를 추가하거나")
        print("2. 환경변수에 OPENAI_API_KEY를 설정해주세요.")
        return

    folder_path = './data'
    
    # data 폴더 존재 여부 확인
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"'{folder_path}' 폴더가 생성되었습니다. PDF 파일을 이 폴더에 넣어주세요.")
        return

    # PDF 파일 존재 여부 확인
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"'{folder_path}' 폴더에 PDF 파일이 없습니다.")
        return

    try:
        embeddings = OpenAIEmbeddings(
            model='text-embedding-3-small',
            openai_api_key=OPENAI_API_KEY
        )
    except Exception as e:
        print(f"OpenAI API 초기화 중 오류 발생: {e}")
        return

    documents = load_data(folder_path)
    if not documents:
        print("로드된 문서가 없습니다.")
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )

    for document in documents:
        filtered_documents = data_cleaning(document)
        chunks = text_splitter.split_documents(filtered_documents)
        
        # Chroma 데이터베이스 초기화
        chroma_db = Chroma.from_documents(
            documents=chunks,  
            embedding=embeddings,
            persist_directory='./chroma_db',
        )
        chroma_db.persist()

def initialize_vector_store():
    if not os.path.exists('./chroma_db'):
        build_vector_store()
    embeddings = OpenAIEmbeddings(
        model='text-embedding-3-small',
        openai_api_key=OPENAI_API_KEY
    )
    return Chroma(persist_directory='./chroma_db', embedding_function=embeddings)

# 메인 실행 코드 추가
# if __name__ == '__main__':
#     print("벡터 데이터베이스 초기화를 시작합니다...")
#     initialize_vector_store()
#     print("벡터 데이터베이스 초기화가 완료되었습니다.")




