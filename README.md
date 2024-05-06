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

## Examples

### Example 1:

![example 1](<images/Example 1.png>)

#### **Question:**

> I am a Data Scientist.
> What is the NOC code closest to my background?
> Give me the closest 5-digit NOC code and job duties even if there is not a direct match.

#### **Answer:**

Based on the provided context, the closest NOC code to your background as a Data Scientist is:

**21211**

Job Duties:

* Implement cutting-edge techniques and tools in machine learning, deep learning, and artificial intelligence to make data analysis more efficient
* Perform large-scale experimentation to identify hidden relationships between variables in large datasets
* Create advanced machine learning algorithms such as regression, simulation, scenario analysis, modeling, clustering, decision trees, and neural networks
* Prepare and extract data using programming language
* Implement new statistical, machine learning, or other mathematical methodologies to solve specific business problems
* Visualize data in a way that allows a business to quickly draw conclusions and make decisions
* Develop artificial intelligence models and algorithms and implement them to meet the needs of the organization.

This NOC code is closest to your background as a Data Scientist because it involves implementing machine learning, deep learning, and artificial intelligence techniques, performing large-scale experimentation, creating advanced machine learning algorithms, preparing and extracting data using programming language, and developing AI models and algorithms.

### Example 2:

![example 2](<images/Example 2.png>)

#### **Question:**

> I am a merchandising buyer and responsible for managing retail stocks.
> What is the NOC code closest to my background?
> Give me the closest 5-digit NOC code and job duties even if there is not a direct match.

#### **Answer:**

Based on your description of being a merchandising buyer and responsible for managing retail stocks, I would suggest that the NOC (National Occupational Classification) code closest to your background is:

65102 - Store shelf stockers, clerks, and order fillers

This job duties include:

* Unpacking products received by store and counting, weighing or sorting items
* Using barcode scanning equipment to record incoming stock, verify pricing and maintain computerized stock inventory
* Stocking shelves and display areas and keeping stock clean and in order
* Labeling and documenting orders, and preparing shipping, customs and courier documentation when required

While this NOC code is primarily focused on the day-to-day operations of a retail store, it's possible that your role as a merchandising buyer may involve some or all of these duties.

The other two NOC codes mentioned (62010 - Retail sales supervisors and 60020 - Retail and wholesale trade managers) are more focused on management and supervision roles, which don't seem to be directly applicable to your background.

## Credits

Some code snippets used in this project are adapted from [pixegami/rag-tutorial-v2](https://github.com/pixegami/rag-tutorial-v2). We express our gratitude to the contributors of that repository for their valuable contributions.

## License

This project is licensed under the MIT License - see the [LICENSE](https://chatgpt.com/c/LICENSE) file for details.
