from sentence_transformers import SentenceTransformer
import neo4j
import streamlit as st


def main():

    URI = st.secrets["NEO4J_URI"]
    AUTH = (st.secrets["NEO4J_USERNAME"], st.secrets["NEO4J_PASSWORD"])

    driver = neo4j.GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    model = SentenceTransformer('all-MiniLM-L6-v2')  # vector size 384

    batch_size = 100
    batch_n = 1
    cv_embeddings = []
    with driver.session() as session:
        # Fetch `CV` nodes
        result = session.run('MATCH (cv:CalculationView) RETURN cv.name as name, cv.package as package')
        for record in result:
            name = record.get('name')
            package = record.get('package')

            # Create embedding
            if name is not None:
                cv_embeddings.append({
                    'name': name,
                    'package': package,
                    'embedding': model.encode(f'''
                        name: {name}\n
                        package: {package}
                    '''),
                })

            import_batch(driver, cv_embeddings, batch_n)
            cv_embeddings = []

    # Import complete, show counters
    records, _, _ = driver.execute_query('''
    MATCH (cv:CalculationView WHERE cv.embedding IS NOT NULL)
    RETURN count(*) AS count, size(cv.embedding) AS embeddingSize
    ''')


def import_batch(driver, nodes_with_embeddings, batch_n):
    # Add embeddings to Movie nodes
    driver.execute_query('''
    UNWIND $calc as calc
    MATCH (m:CalculationView {name: calc.name, package: calc.package})
    CALL db.create.setNodeVectorProperty(m, 'embedding', calc.embedding)
    ''', calc=nodes_with_embeddings)
    print(f'Processed batch {batch_n}.')


if __name__ == '__main__':
    main()

'''
Movie nodes with embeddings: 9083.
Embedding size: 384.
'''