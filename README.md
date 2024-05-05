# **NOC Search RAG**

This repository applies RAG (Retrieval Augmented Generation) techniques with LLM (Large Language Models) to assist in selecting the Canada visa [National Occupation Classification (NOC)](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/eligibility/find-national-occupation-code.html) closest to your background.

Running locally on the cutting-edge Llama 3 model, facilitated by Ollama, this tool ensures data privacy and confidentiality while delivering precise and tailored outcomes.

## Tutorial

To set up NOC Search RAG, follow these steps:

1. Clone this repository.
2. Set up your environment:
   * You can use Anaconda or create a virtual environment using `python -m venv <your-env-name>`.
3. Download [Ollama](https://ollama.com/download).
4. Install Llama3 and the embedding function:

```shell
ollama pull nomic-embed-text
ollama pull llama3
```

5. Open Ollama and activate your environment:
   * Mac: `source venv/bin/activate`
   * Windows: `venv/Scripts/activate`
6. Install all required libraries with `pip install -r requirements.txt`
7. Run the following code:

```python
python populate_db.py
python query.py
```

7. in the browser, open window `http://127.0.0.1:7860`

## Example vedio

Coming soon ... 

## Credits

Some code snippets used in this project are adapted from [pixegami/rag-tutorial-v2](https://github.com/pixegami/rag-tutorial-v2). We express our gratitude to the contributors of that repository for their valuable contributions.

## License

This project is licensed under the MIT License - see the [LICENSE](https://chatgpt.com/c/LICENSE) file for details.
