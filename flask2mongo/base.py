import pymongo
from flask2mongo import settings
import flask2mongo
import inspect
import datetime


MONGO_CONN = pymongo.MongoClient(settings.mongo['MONGO_HOST'], settings.mongo['MONGO_PORT'])
MONGO_DB = MONGO_CONN[settings.mongo['MONGO_DATABASE']]


class Document(object):
    """Abstraction of a Python class to a Mongo Document

    Capable of inspect itself and parse its attributes to and values to JSON-like
    pairs of keys and values

    """

    unique_keys = []  # unique_keys are vars which will compose the _id field on django
    identifier_key = None  # a key to identify this instance (must be one of key(s) into unique_keys)

    #: there are 3 types of documents provided by flask2mongo:
    #:
    #: 1. static documents: the attributes are pointed on
    #:    class definition and only those fields will be turn into mongo docs
    #:
    #: 2. non-static documents: the attributes aren't defined and whenever entity the object takes it'll be turned
    #:    into mongo docs
    #:
    #: 3. hybrid documents: You can define some obligatory fields that the doc must have, but if extra fields are
    #:   given they'll go to the mongo doc as well
    hybrid = False

    def __new__(cls, *args, **kwargs):
        """Redefine the creation of a new instance
        This method inspect the attributes of the class to instance them if they're fields.
        """

        # fields which starts with __ or are instance of Field and are not fillable must be ignored for now
        significant_fields = []
        print(cls)
        for k in cls.__dict__:
            if str(k).startswith('__'): continue
            if isinstance(cls.__dict__[k], flask2mongo.Field) and not cls.__dict__[k].fillable: continue
            significant_fields.append(k)

        # Is this instance statically typed?
        statically_typed = len(significant_fields) > 0 and not cls.hybrid

        # check if a dictionary was passed as arg
        if args:
            doc = args[0]  # a dictionary was passed as arg to instance object attributes
        else:
            doc = kwargs   # the object attributes were passed by kwargs on key=value style

        obj = super(Document, cls).__new__(cls)  # create a pre-instance of this class

        for k, v in doc.items():
            if statically_typed and cls.__dict__.get(k):
                typed_v = cls.__dict__[k]
                typed_v.value = v
                setattr(obj, k,  typed_v)
            else:
                f = flask2mongo.Field()
                f.value = v
                setattr(obj, k, f)

        field_date = flask2mongo.Field()
        field_date.value = datetime.datetime.utcnow()
        setattr(obj, 'created_at', field_date)

        #  re-check if all fields declared on child class were properly filled (in case of non-static and hybrid docs)
        for k, v in inspect.getmembers(cls):
            attr = getattr(cls, k)
            if isinstance(attr, flask2mongo.Field) and not cls.__dict__.get(k):
                if not attr.fillable:
                    val = attr.__class__()
                    setattr(obj, k, val)
                elif k not in doc:
                    raise Exception('Missing field {}'.format(k))

        obj.statically_typed = statically_typed
        return obj


    def jsonify(self):
        doc_iter = self.__dict__
        rdoc = dict({})
        for k, v in doc_iter.items():
            if not str(k).startswith('__') and isinstance(v, flask2mongo.Field) and v:
                rdoc[k] = v.value
        return rdoc

    def save(self, collection=None):
        _id = ''
        collection = self.__class__.__name__.lower() if not collection else collection
        if self.identifier_key:
            if not self.unique_keys:
                self.unique_keys.append(self.identifier_key)
            if self.identifier_key not in self.unique_keys:
                raise Exception('Identifier key must be one of unique_keys')
            for k in self.unique_keys:
                _id += '{}'.format(self.__dict__[k])
            if _id:
                self.__dict__['_id'] = _id
        mongo_doc = self.jsonify()
        if _id:
            mongo_doc['_id'] = _id
        MONGO_DB[collection].insert_one(mongo_doc)

    @classmethod
    def all(cls, collection=None):
        collection = cls.__name__.lower() if not collection else collection
        documents = MONGO_DB[collection].find({}, {'_id': 0})
        return list(documents)

    @classmethod
    def query(cls, *query_infs, collection=None, jsoned=False):
        collection = cls.__name__.lower() if not collection else collection
        documents = MONGO_DB[collection].find(*query_infs)
        if jsoned: return list(documents)
        return list(cls(d) for d in documents)

    @classmethod
    def update(cls, update_doc, query_dict, collection=None):
        if not collection: collection = cls.__name__.lower()
        for k, v in update_doc.items():
            MONGO_DB[collection].update(
                query_dict,
                {'$set': {k: v}},
                upsert=True
            )

    @property
    def object_id(self):
        if '_id' in self.__dict__:
            return self.__dict__['_id'].__str__()


    @object_id.setter
    def object_id(self, value):
        self.__dict__['_id'] = value

    @staticmethod
    def get_collection_list():
        return MONGO_DB.collection_names()
