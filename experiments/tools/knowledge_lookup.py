KNOWLEDGE_BASE = {
    "population of france": "67 million",
    "population of germany": "83 million",
    "population of italy": "59 million",
    "capital of japan": "Tokyo"
}


def knowledge_lookup(query):

    query = query.lower()

    for key in KNOWLEDGE_BASE:
        if key in query:
            return KNOWLEDGE_BASE[key]

    return "No information found in knowledge base."