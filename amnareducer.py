import sys

# Function to calculate IDF
def calculate_idf(total_documents, document_frequency):
    if document_frequency == 0:
        return 0
    else:
        idf = total_documents / document_frequency
        idf = 1 + (idf ** (1 / 3))  #cube root 
        return idf


# Initialize variables
current_document = None
document_tf_idf = {}
query_vector = {}
idf_values = {}  # IDF values received from the mapper
document_count = 0

# Read input from stdin
for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')
    if len(parts) == 3:
        if parts[0] == 'Query':
            word_id, count = int(parts[1]), int(parts[2])
            query_vector[word_id] = count
        elif parts[0] == 'WordInfo':
            word, word_id, count = parts[1], int(parts[2]), int(parts[3])
            idf_values[word_id] = calculate_idf(document_count, count)
        elif parts[0] == 'DocumentCount':
            document_count = int(parts[1])
        elif parts[0] == 'WordDF':
            word_id, df = int(parts[1]), int(parts[2])
            idf_values[word_id] = calculate_idf(document_count, df)
    elif len(parts) == 3:
        document_id, word_id, count = parts[0], int(parts[1]), int(parts[2])  # Convert count to integer
        tf_idf = count * idf_values.get(word_id, 0)
        if current_document == document_id:
            document_tf_idf[word_id] = tf_idf
        else:                              # Don't forget the last word
            if current_document is not None:  
                # Calculate relevance score for the current document
                relevance_score = sum(query_vector.get(word_id, 0) * tf_idf for word_id, tf_idf in
                                      document_tf_idf.items())
                print(f"{current_document}\t{relevance_score}")
            current_document = document_id
            document_tf_idf = {word_id: tf_idf for word_id, tf_idf in [(word_id, count * idf_values.get(word_id, 0))]}
# Calculate relevance score for the last document
if current_document is not None:
    relevance_score = sum(query_vector.get(word_id, 0) * tf_idf for word_id, tf_idf in document_tf_idf.items())
    print(f"{current_document}\t{relevance_score}")
