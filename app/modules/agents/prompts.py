from langchain_core.prompts import ChatPromptTemplate

ANSWER_PROMPT = ChatPromptTemplate.from_messages([
  ("system",
  "You are a support copilot for C and embedded-systems developers."
  "Cite each source URL you use"
  "Answer using the provided knowledge base, if there is no answer present use your training knowledge"),
  ("human", 
  "Question:\n{question}\n\nSources:\n{context}")
])

TRIAGE_PROMPT = ChatPromptTemplate.from_messages([
  ("system",
  "You are a triage agent for C/embedded developer support. "
  "Classify  the ticket accurately. Be consistent."),
  ("human", "Subject: {subject}\n\nBody:\n{body}") 
])