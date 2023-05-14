import nltk
import string
import gensim
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def preprocess(reviews, level_1):
    # 1. lowercase all content, str() for float has no attribute lower()
    reviews = list(str(review).lower() for review in reviews)
    # 2. choose only those reviews that contain the level 1 keyword with spaces
    reviews = list(filter(lambda review: (" " + level_1 + " ") in review, reviews))
    # 3. remove punctuations
    reviews = list(review.translate(str.maketrans("","",string.punctuation)) for review in reviews)
    # 4. remove stop words, eg: the, a, i, it
    reviews = list(map(lambda x: " ".join(x for x in x.split() if x not in nltk.corpus.stopwords.words("english")), reviews))
    # 5. lemmatize
    reviews = list(map(lemmatize, reviews))
    return reviews

def lemmatize(text):    
    lemmatizer = nltk.stem.WordNetLemmatizer()
    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    tag_dict = {"J": nltk.corpus.wordnet.ADJ,   
                "N": nltk.corpus.wordnet.NOUN,
                "V": nltk.corpus.wordnet.VERB,
                "R": nltk.corpus.wordnet.ADV}
    lemmatized_text = " ".join([lemmatizer.lemmatize(w, 
                                tag_dict.get(nltk.pos_tag([w])[0][1][0].upper(), 
                                             nltk.corpus.wordnet.NOUN)) 
                                for w in w_tokenizer.tokenize(text)])
    return lemmatized_text

def get_nodes(reviews, parent_node):
    # topic modelling
    list_of_list_of_tokens = list(i.split() for i in reviews)
    dictionary_LDA = gensim.corpora.Dictionary(list_of_list_of_tokens)
    corpus = [dictionary_LDA.doc2bow(list_of_tokens) for list_of_tokens in list_of_list_of_tokens]
    num_topics = 7 # the number of keyword in level 2 or 3
    num_words = 10 # the number of words to "render" a topic, which is not shown in the network
    lda_model = gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary_LDA, passes=4, alpha=[0.01]*num_topics, eta=[0.01]*len(dictionary_LDA.keys()))
    
    child_nodes = set()
    for i,topic in lda_model.show_topics(formatted=False, num_topics=num_topics, num_words=num_words):
        for keyword in topic:
            child_nodes.add(keyword[0]) # keyword is of the form ('child', 0.026235294)
    child_nodes = list(child_nodes)
    
    if parent_node in child_nodes:
        child_nodes.remove(parent_node)
    return child_nodes

def get_edges(parent_node, child_nodes):
    edges = []
    for child_node in child_nodes:
        edges.append([parent_node, child_node])        
    return pd.DataFrame(data = edges,columns = ["parent_node","child_node"])

def get_network(reviews, level_1_node):
    network = []    
    level_2_nodes = get_nodes(reviews, level_1_node)
    level_1_edges = get_edges(level_1_node, level_2_nodes)
    network.append(level_1_edges)
    for level_2_node in level_2_nodes:
        reviews_level_2 = list(filter(lambda review: (" " + level_2_node + " ") in review, reviews))
        if len(reviews_level_2) == 0:
            continue
        level_3_nodes = get_nodes(reviews_level_2, level_2_node)
        level_2_edges = get_edges(level_2_node, level_3_nodes)
        network.append(level_2_edges)
    network = pd.concat(network).reset_index(drop=True)
    return network

def get_eigenvector_centralities(network):
    level_1_node = network["parent_node"][0]
    level_2_nodes = set(network[network["parent_node"] != level_1_node]["parent_node"])
    network = nx.from_pandas_edgelist(network,
                                source = "parent_node",
                                target = "child_node",)
    centralities = nx.eigenvector_centrality(network)    
    centralities = {level_2_node: round(centrality,4) 
                    for level_2_node, centrality in 
                    sorted(centralities.items(), key = lambda item:item[1]) 
                    if level_2_node in level_2_nodes}
    return centralities

def simplify_network(network, chosen_nodes):
    level_1_edges = network[network.child_node.isin(chosen_nodes)]
    level_1_node = level_1_edges.reset_index(drop=True)["parent_node"][0]
    level_1_edges = level_1_edges[level_1_edges["parent_node"] == level_1_node]
    simplified_network = [level_1_edges, ]
    num_level_3 = 7
    for chosen_node in chosen_nodes:
        level_2_edges = network[network["parent_node"] == chosen_node]
        if len(level_2_edges) > num_level_3:
            level_2_edges = level_2_edges.sample(num_level_3, replace = False)
        simplified_network.append(level_2_edges)
    return pd.concat(simplified_network)

def visualize_network(network): # the first row is assured to be level 1 node. plz name it

    G = nx.from_pandas_edgelist(network,
                                source = "parent_node",
                                target = "child_node",)

    node_label = [i for i in dict(G.nodes).keys()]
    node_label = {i:i for i in dict(G.nodes).keys()}
    fig, ax = plt.subplots(figsize=(20, 20))

    df = pd.DataFrame(data = [[0,]*len(G.nodes()),]*len(G.nodes()), 
                                      index=G.nodes(), 
                                      columns=G.nodes())
    for row, data in nx.shortest_path_length(G):
        for col, dist in data.items():
            df.loc[row,col] = dist
    df = df.fillna(df.max().max())
    pos = nx.kamada_kawai_layout(G, dist=df.to_dict())
#    pos = nx.spring_layout(G, scale=0.2)

    pos_higher = {}
    y_off = 0.02
    for k, v in pos.items():
        pos_higher[k] = (v[0], v[1]+y_off)

    d = dict(G.degree)
    nx.draw_networkx_nodes(G, pos, node_color = ["blue",] + ["lightblue",] * (len(G.nodes())-1), ax = ax) # labels=True removed
#    nx.draw_networkx_nodes(G, pos, node_color = "lightblue", labels = True, ax = ax)
    nx.draw_networkx_edges(G, pos, node_size = 1000,edge_color = "grey", width = 3, ax=ax, alpha = 0.5)
    nx.draw_networkx_labels(G, pos_higher, node_label, font_size=24, font_family = "serif", ax=ax)
    return fig
    

