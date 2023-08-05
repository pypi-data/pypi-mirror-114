from elasticsearch import Elasticsearch
import json

class UnivocElasticAPI(object):
    """
    A class used to interact with Elasticsearch API for UNIVOC

    ...

    Methods
    -------
    create(self, index: str, txt: str, txt_index: int, corpus: str, txt_lang: str, id: str = None) -> str
        Insert a document in Elasticsearch
    
    read(self, index: str, txt: str = None, txt_index: int = None, corpus: str = None, txt_lang: str = None, txt_index_range: range = None) -> list
        Search documents in Elasticshearch by arguments. If no arguments specified, will return first documents.
    
    readById(self, index: str, id: list) -> str
        Search documents in Elasticsearch by id.

    iterate(self, index: str, offset: int, size: int) -> list
        Iterate truth index.
    
    delete(self, index: str, id: str) -> bool
        Delete document from index.
    
    update(self, index: str, id: str, txt: str, txt_index: int, corpus: str, txt_lang: str) -> bool
        Update document from index.
    """

    def __init__(self, host: dict, login: str, password: str, max_hits: int = 10000) -> None:
        """
        Parameters
        ----------
        host : dict
            Elasticsearch host address. Example: {'host': 'localhost', 'port': 80}
        login: str
            login for Elasticsearch
        password: str
            password for Elasticsearch
        max_hits: int = 10000
            maximum hits that Elasticsearch will return on one request
        
        Return
        ----------
        None
        """
        self.__es = Elasticsearch([host], http_auth=(login, password))
        self.__hits_size = max_hits

    def create(self, index: str, txt: str, txt_index: int, corpus: str, txt_lang: str, id: str = None) -> str:
        """
        Parameters
        ----------
        index: str
            index where document will be inserted
        txt: str
            the text (sentence) to be entered 
        txt_index: int
            position of txt in corpus
        corpus: str
            txt corpus
        txt_lang: str
            txt language. Example: EN, RO
        id: str = None, optional
            id of document that will be inserted
        
        Return
        ----------
        id of inserted document, else None if error occured
        """
        data = {}
        data["txt_lang"] = txt_lang
        data["corpus"] = corpus
        data["txt"] = txt
        data["txt_index"] = txt_index
        if id: result = self.__es.index(index=index, doc_type='_doc', body=json.dumps(data), id=id)
        else: result = self.__es.index(index=index, doc_type='_doc', body=json.dumps(data))
        if result['result'] == 'created' or result['result'] == 'updated': return result['_id']
        return None
    
    def read(self, index: str, txt: str = None, txt_index: int = None, corpus: str = None, txt_lang: str = None, txt_index_range: range = None) -> list:
        """
        Parameters
        ----------
        index: str
            index where document will be searched
        txt: str
            the text (sentence) to be searched 
        txt_index: int
            position of txt in corpus
        corpus: str
            txt corpus
        txt_lang: str
            txt language. Example: EN, RO
        txt_index_range: range = None
            range of text index to be searched
        
        Return
        ----------
        list of foundet sentences, None if error occured or nothing was found
        """
        query = {'size': self.__hits_size,'query': {'bool': {'must': [], 'filter': []}}}
        if txt: query['query']['bool']['must'].append( {"match": {"txt": txt}} )
        if txt_index: query['query']['bool']['must'].append( {"match": {"txt_index": txt_index}} )
        if corpus: query['query']['bool']['must'].append( {"match": {"corpus": corpus}} )
        if txt_lang: query['query']['bool']['must'].append( {"match": {"txt_lang": txt_lang}} )
        if txt_index_range: query['query']['bool']['filter'].append({'range': {'txt_index': {'gte': txt_index_range[0], 'lte': txt_index_range[-1], 'boost': 2}}})
        result = self.__es.search(index=index, body=query)
        if result['hits']['total']['value'] == 0: return None
        return [elem['_source']['txt'] for elem in result['hits']['hits']]
    
    def readById(self, index: str, id: list) -> str:
        """
        Parameters
        ----------
        index: str
            index where document will be seeked
        id: list
            document id or multiple ids
        Return
        ----------
        None if nothing found, else list of sentences that was found
        """
        query = {'query': {'terms': {'_id': id}}}
        result = self.__es.search(index=index, body=query)
        if result['hits']['total']['value'] == 0: return None
        return [elem['_source']['txt'] for elem in result['hits']['hits']]
    
    def iterate(self, index: str, offset: int, size: int) -> list:
        """
        Parameters
        ----------
        index: str
            index where document will be inserted
        offset: int
            offset of index
        size: int
            nr of documents to get
        Return
        ----------
        None
        """
        query = {'from': offset, 'size': size, 'query': {'match_all': {}}}
        result = self.__es.search(index=index, body=query)
        return [elem['_source']['txt'] for elem in result['hits']['hits']]

    def delete(self, index: str, id: str) -> bool:
        """
        Parameters
        ----------
        index: str
            index where document will be deleted
        id: str
            document id
        Return
        ----------
        True if deleted, False if error occured
        """
        result = self.__es.delete(index=index, id=id)
        if result['result'] == 'deleted': return True
        else: return False

    def update(self, index: str, id: str, txt: str, txt_index: int, corpus: str, txt_lang: str) -> bool:
        """
        Parameters
        ----------
        index: str
            index where document will be updated
        txt: str
            the text (sentence) to be updated 
        txt_index: int
            position of txt in corpus
        corpus: str
            txt corpus
        txt_lang: str
            txt language. Example: EN, RO
        id: str = None, optional
            id of document that will be inserted
        
        Return
        ----------
        True if text was updated, else False
        """
        return self.create(index=index,txt=txt,txt_index=txt_index,txt_lang=txt_lang,corpus=corpus,id=id)