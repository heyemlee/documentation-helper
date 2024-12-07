# LangChain Documentation Helper
![Image](public/i.jpg)
A repository for learning LangChain by building a generative ai application.

This is a web application is using a Pinecone as a vectorsotre and answers questions about LangChain.

## Tech Stack

Client: Streamlit

Server Side: LangChain

Vectorstore: Pinecone

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PINECONE_API_KEY`
`OPENAI_API_KEY`


Install dependencies

```bash
  pipenv install
  pip install streamlit
  pip install streamlit-chat
  pip install langchain-pinecone

```

Start the flask server

```bash
  streamlit run main.py
```

## Running Tests

To run tests, run the following command

```bash
  pipenv run pytest .
```
