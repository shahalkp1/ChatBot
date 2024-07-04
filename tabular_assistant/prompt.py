from langchain.prompts import PromptTemplate

tabular_assistant = """you are an assistant which will learn a tabular data and 
                        answer user query based on it
                        Question:{question}
                        Answer:"""
tabular_helper = PromptTemplate(
                input_variables=["questions"],
                template=tabular_assistant
            )