from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
  chunk_size=700,
  chunk_overlap=80,
  separators=["\n\n", "\n```", "```\n", "\n", " "]
)

def chunk_article_body(body: str) -> list[str]:
    return splitter.split_text(body)