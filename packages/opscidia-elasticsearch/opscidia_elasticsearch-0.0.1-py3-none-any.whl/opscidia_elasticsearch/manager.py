import json, os
from elasticsearch import RequestsHttpConnection
from elasticsearch.helpers import bulk
from elasticsearch_dsl import connections, Search, Document, UpdateByQuery
import boto3
from requests_aws4auth import AWS4Auth

class Manager(object):
    
    def __init__(self, hosts, region='eu-west-3', service='es', use_ssl=True, verify_certs=True, timeout=60):
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
        
        self.connect = connections.create_connection(
                        hosts=hosts,
                        timeout=timeout,
                        http_auth = awsauth,
                        use_ssl = use_ssl,
                        verify_certs = use_ssl,
                        connection_class = RequestsHttpConnection
                    )
        
        
    def create_index(self, index_name: str, settings: None, erase_if_exists: bool=False):
        
        if settings is None:
             settings = {
                "settings":{
                    "number_of_shards":5,
                    "number_of_replicas":1,
                    "analysis":{
                        "filter":{"backslash":{"pattern":"\\[a-z]","type":"pattern_replace","replacement":""},
                        "english_snowball":{"type":"snowball","language":"English"},
                        "english_stop":{"type":"stop","stopwords":"_english_"}},
                        "analyzer":{
                        "classic_analyzer":{
                            "filter":["lowercase","backslash"],
                            "char_filter":["html_strip"],
                            "type":"custom",
                            "tokenizer":"standard"},
                        "stopword_analyzer":{
                            "filter":["lowercase","backslash","english_stop","english_snowball"],
                            "char_filter":["html_strip"],
                            "type":"custom",
                            "tokenizer":"standard"}
                        }
                    }
                    },
                    "mappings":{
                    "properties":{
                        "DOI":{"type":"keyword"},
                        "prefix_doi": {"type": "keyword"},
                        "URL":{"type":"keyword"},
                        "abstract":{"type":"text","analyzer":"classic_analyzer","search_analyzer":"stopword_analyzer","search_quote_analyzer":"classic_analyzer"},
                        "abstract_clean":{"type":"keyword"},
                        "authors":{"type":"keyword"},
                        "fullText":{"type":"text","analyzer":"classic_analyzer","search_analyzer":"stopword_analyzer","search_quote_analyzer":"classic_analyzer"},
                        "fullText_clean":{"type":"text"},
                        "keywords":{"type":"keyword"},
                        "language":{"type":"keyword"},
                        "openaire_id":{"type":"keyword"},
                        "provider":{"type":"keyword"},
                        "provider_id":{"type":"keyword"},
                        "publication_date":{"type":"date","ignore_malformed":True,"format":"yyyy-mm-dd"},
                        "title":{"type":"text"},
                        "citation": {"type": "text"},
                        # "ISBN": {"type": "keyword"},

                        },
                    }
            }
        
        if self.connect.indices.exists(index_name):
            print(index_name + " index already exists")
            if(erase_if_exists):
                print(index_name + " deleted and recreated")
                self.connect.indices.delete(index=index_name)
        self.connect.indices.create(index=index_name,body=settings,ignore=400)
        
        
    def save_to_index(self, generator):
        print('Bulk starts')
        res = bulk(self.connect, generator, raise_on_error=False, raise_on_exception=False)
        print(res)
        
        

