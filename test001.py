from sentence_transformers import SentenceTransformer
import neo4j
import streamlit as st


URI = st.secrets["NEO4J_URI"]
AUTH = (st.secrets["NEO4J_USERNAME"], st.secrets["NEO4J_PASSWORD"])

driver = neo4j.GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()

model = SentenceTransformer('all-MiniLM-L6-v2')

query_prompt = 'ZSAC.ZBDG.ZRETAIL.ZHS and CVHSB006_S0'
query_embedding = model.encode(query_prompt)

related_movies, _, _ = driver.execute_query('''
    CALL db.index.vector.queryNodes('cvname', 1, $queryEmbedding)
    YIELD node, score
    RETURN node.name, node.package, score
    ''', queryEmbedding=query_embedding)
print(f'Cv with name or package like `{query_prompt}`:')
for record in related_movies:
    print(record)