from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings


def get_embedding_function(embedding_type="ollama", model_name="nomic-embed-text"):
    if embedding_type == "ollama":
        embeddings = OllamaEmbeddings(model=model_name)
    elif embedding_type == "bedrock":
        embeddings = BedrockEmbeddings(
            credentials_profile_name="default", region_name="us-east-1"
        )
    else:
        raise ValueError("Invalid embedding type. Choose between 'ollama' and 'bedrock'.")
    return embeddings