from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from dotenv import load_dotenv

load_dotenv()
doc1 = Document(
    page_content="Eren Yeager is the main protagonist of Attack on Titan who transforms into the Attack Titan and Founding Titan. Known for his fierce determination to achieve freedom and destroy all Titans, his journey takes him from seeking revenge to becoming a complex revolutionary figure.",
    metadata={"affiliation": "Survey Corps"}
)

doc2 = Document(
    page_content="Mikasa Ackerman is one of the strongest soldiers in the Survey Corps and Eren's adoptive sister. Known for her exceptional combat skills and unwavering loyalty to Eren, she possesses Ackerman abilities that make her a formidable warrior against Titans.",
    metadata={"affiliation": "Survey Corps"}
)

doc3 = Document(
    page_content="Armin Arlert is the strategic genius of the Survey Corps who later inherits the Colossal Titan. His brilliant tactical mind and ability to analyze situations make him invaluable despite not being the strongest physical fighter.",
    metadata={"affiliation": "Survey Corps"}
)

doc4 = Document(
    page_content="Levi Ackerman is known as humanity's strongest soldier and captain of the Survey Corps Special Operations Squad. His unparalleled combat skills, cleanliness obsession, and Ackerman abilities make him a legendary figure in the fight against Titans.",
    metadata={"affiliation": "Survey Corps"}
)

doc5 = Document(
    page_content="Erwin Smith was the 13th commander of the Survey Corps, known for his brilliant strategic mind and willingness to sacrifice everything for humanity's freedom. His leadership and famous speeches inspired soldiers to follow him into certain death.",
    metadata={"affiliation": "Survey Corps"}
)

docs = [doc1, doc2, doc3, doc4, doc5]

vector_store = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
    persist_directory='my_chroma_db',
    collection_name='sample'
)
vector_store.add_documents(docs)