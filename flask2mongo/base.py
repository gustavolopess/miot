import pymongo
from flask2mongo import settings
import flask2mongo
import inspect


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

        # The __collection__ attribute determines the mongo collection where the doc referred to this object
        # will be placed.
        # If the attribute collection is passed on kwargs, the value will be the name of child class
        # in lowercase.
        obj.__collection__ = cls.__name__.lower() if 'collection' not in kwargs else kwargs.pop('collection')

        for k, v in doc.items():
            if statically_typed and cls.__dict__.get(k):
                print(k)
                typed_field = cls.__dict__[k]  # get the typed field on child class with same name of doc field
                if isinstance(v, dict) and inspect.isclass(typed_field):
                    instanced_field = typed_field(**v)
                    setattr(obj, k, instanced_field)
                elif inspect.isclass(typed_field) and isinstance(v, typed_field):
                    setattr(obj, k, v)
                else:
                    typed_field.value = v  # instance this field with value equal to the passed on args
                    setattr(obj, k,  typed_field)  # set this attribute to fresh-instanced object
            else:  # non-static docs
                f = flask2mongo.Field()   # set a generic field to receive the value
                f.value = str(v)
                setattr(obj, k, f)

        #  re-check if all fields declared on child class were properly filled (in case of non-static and hybrid docs)
        for k, v in cls.__dict__.items():
            if isinstance(cls.__dict__[k], flask2mongo.Field):
                if not cls.__dict__[k].fillable:
                    setattr(obj, k, v)
                elif k not in doc:
                    print(k, 'not in', doc)
                    raise Exception('Missing field')

        obj.statically_typed = statically_typed
        return obj

    @property
    def collection(self):
        return self.__collection__

    @classmethod
    def jsonify(cls, doc=None):
        doc = cls.__dict__ if not doc else doc
        rdoc = dict({})
        for k, v in doc.items():
            if not str(k).startswith('__') and isinstance(v, flask2mongo.Field):
                rdoc[k] = v.value
        return rdoc

    def save(self, collection=None):
        if not collection:
            collection = self.collection
        if self.identifier_key:
            if not self.unique_keys:
                self.unique_keys.append(self.identifier_key)
            elif self.identifier_key not in self.unique_keys:
                raise Exception('Identifier key must be one of unique_keys')
            _id = ''
            for k in self.unique_keys:
                print(self.__dict__)
                _id += str(self.__dict__[k])
            if _id:
                id_field = flask2mongo.StringField()
                id_field.value = _id
                self.__dict__['_id'] = id_field
        MONGO_DB[collection].insert_one(Document.jsonify(doc=self.__dict__))

    @classmethod
    def all(cls, collection=None):
        collection = cls.__name__.lower() if not collection else collection
        documents = MONGO_DB[collection].find({}, {'_id': 0})
        return list(documents)

    @classmethod
    def query(cls, *query_infs, collection=None):
        collection = cls.__name__.lower() if not collection else collection
        documents = MONGO_DB[collection].find(*query_infs)
        return list(cls.__new__(d) for d in documents)

    @classmethod
    def update(cls, update_doc, query_dict, collection=None):
        if not collection: collection = cls.collection
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

    @property
    def object_collection(self):
        if self.collection:
            return self.collection

    @object_id.setter
    def object_id(self, value):
        self.__dict__['_id'] = value

    @staticmethod
    def get_collection_list():
        return MONGO_DB.collection_names()
