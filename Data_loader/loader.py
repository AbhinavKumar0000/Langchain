import google.generativeai as genai
from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader, WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser = StrOutputParser()

# text file loader
loader1 = TextLoader("one_piece.txt", encoding="utf-8")
docs1 = loader1.load()

# pdf file loader
loader2 = PyPDFLoader("pdf_sample.pdf")
docs2 = loader2.load()

# csv loader
loader3 = CSVLoader("Social_Network_Ads.csv")
docs3 = loader3.load()

# web loader
loader4 = WebBaseLoader("https://en.wikipedia.org/wiki/Artificial_intelligence")
docs4 = loader4.load()

prompt = PromptTemplate(
    template='Explain this to me like I am 5 years old\n {text}',
    input_variables=['text']
)



chain = prompt | model | parser

print(chain.invoke({'text':docs4[0].page_content}))
