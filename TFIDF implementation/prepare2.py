import os

# Open the index file for reading
with open(r"Leetcodescrapped\Qdata\index.txt", 'r') as f:
    lines = f.readlines()

def preprocess(document_text):
    # remove the leading numbers from the string, remove not alpha numeric characters, make everything lowercase
    terms = [term.lower() for term in document_text.strip().split()[1:]]
    return terms

def preprocess1(document_text):
        
        document_text = document_text.strip()  # Remove leading and trailing whitespace

        # Find the index of "example" in the line
        end_index = document_text.find("Example")

        # Extract the text segment from the starting letter to "example"
        if end_index != -1:
            text_segment = document_text[:end_index]
        else:
            text_segment = document_text  # If "example" is not found, use the entire line

        return text_segment

innertext = []
for i in range(1,2406):
    with open(f"Leetcodescrapped\Qdata\{i}\{i}.txt","r",encoding='latin-1') as f :
        title = f.read()
        innertext.append(preprocess1(title))

     
vocab1 = {}
documents1 = []
for index, line in enumerate(lines):
    # read statement and add it to the line and then preprocess
    line = line + innertext[index]
    tokens = preprocess(line)
    documents1.append(tokens)
    tokens = set(tokens)
    for token in tokens:
        if token not in vocab1:
            vocab1[token] = 1
        else:
            vocab1[token] += 1

# reverse sort the vocab by the values
vocab1 = dict(sorted(vocab1.items(), key=lambda item: item[1], reverse=True))

print('Number of documents: ', len(documents1))
print('Size of vocab: ', len(vocab1))
print('Sample document: ', documents1[0]) 

# save the vocab in a text file
with open(r'TFIDF implementation\tf-idf\vocab1.txt', 'w',encoding='utf-8') as f:
    for key in vocab1.keys():
        f.write("%s\n" % key)

# save the idf values in a text file
with open(r'TFIDF implementation\tf-idf\idf-values1.txt', 'w',encoding='utf-8') as f:
    for key in vocab1.keys():
        f.write("%s\n" % vocab1[key])

# save the documents in a text file
with open(r'TFIDF implementation\tf-idf\documents1.txt', 'w',encoding='utf-8') as f:
    for document in documents1:
        f.write("%s\n" % ' '.join(document))

inverted_index = {}
for index, document in enumerate(documents1):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

# save the inverted index in a text file
with open(r'TFIDF implementation\tf-idf\inverted-index1.txt', 'w',encoding='utf-8') as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))
