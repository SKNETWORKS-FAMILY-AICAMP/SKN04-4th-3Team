import os

def format_docs(docs):
    formatted_results = []
    for doc in docs:
        content = doc.page_content
        source = os.path.splitext(os.path.basename(doc.metadata['source']))[0]
        page = doc.metadata['page']
        formatted_results.append(f"내용: {content}\n출처: {source}\n페이지: {page}\n")
        result = "\n".join(formatted_results)
        print(result)
        return result