import os
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.llms import GoogleGenerativeAI

# ====== Set Gemini API Key ======
os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"

# ====== Initialize Gemini Flash LLM and Embedding Model ======
llm = GoogleGenerativeAI(
    model="gemini-1.5-flash-latest",  # Using Gemini Flash 2.0 for speed and efficiency
    temperature=0.3  # Lower temperature for more deterministic outputs
)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)

# ====== Load and Chunk the Text File ======
def load_and_chunk_text(file_path):
    print(f"\n Loading file: {file_path}")
    loader = TextLoader(file_path)
    raw_documents = loader.load()

    splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    documents = splitter.split_documents(raw_documents)

    print(f"Total chunks created: {len(documents)}")
    return documents

# ====== Convert Chunks into Vector Store ======
def create_vectorstore(documents):
    print(" Embedding and indexing chunks into vector store...")
    vectordb = FAISS.from_documents(documents, embedding_model)
    return vectordb

# ====== Build the RAG QA Chain ======
def create_rag_chain(vectordb):
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}  # Retrieve the top 4 most similar chunks
    )

    print("Creating RAG pipeline with Gemini Flash and Retriever...")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

# ====== Summarize the Text File Using Retrieved Chunks ======
def summarize_text(file_path):
    documents = load_and_chunk_text(file_path)
    vectordb = create_vectorstore(documents)
    rag_chain = create_rag_chain(vectordb)

    query = "Please summarize the content of this document."
    print(f"\n💬 Querying: {query}")
    response = rag_chain(query)

    print("\n📄 Summary:\n")
    print(response['result'])

    print("\n Retrieved Context Chunks:")
    for i, doc in enumerate(response['source_documents']):
        preview = doc.page_content[:500].replace("\n", " ")  # Preview first 500 characters
        print(f"\n--- Chunk {i + 1} ---\n{preview}...")

# ====== Choose a Note File from the User's Folder ======
def get_user_selected_file():
    notes_dir = "C:/Users/Priyanshi/Datasets/Notes"
    txt_files = [f for f in os.listdir(notes_dir) if f.endswith(".txt")]

    if not txt_files:
        print("No .txt files found in the folder.")
        exit()

    print("\ Notes Found in Folder:")
    for i, file in enumerate(txt_files):
        print(f"{i + 1}. {file}")

    selected_index = int(input("\nEnter the number of the file to summarize: ")) - 1
    selected_file_path = os.path.join(notes_dir, txt_files[selected_index])
    return selected_file_path

# ====== Main Entry Point ======
if __name__ == "__main__":
    file_path = get_user_selected_file()
    summarize_text(file_path)
