"""
MongoDB ORM models for Cryptocurrency transactions
"""
from mongoengine import *

class Transaction(Document):
    """
    Data Model for a Cryptocurrency transaction. The primary key (_id) attribute will be 
    assigned in the model that inherits this model
    """
    hash = StringField(required=True)
    time = IntField(required=True)
    block_num = IntField(required=True)
    tx_fees = IntField()
    tx_val = IntField()

    meta = {
        'allow_inheritance': True,
        'indexes': [
            '#hash',
            'time'
        ]
    }


class Address(Document):
    """
    Data Model for a Cryptocurrency address
    """
    _id = StringField(required=True)
    time = IntField(required=True)
    curr_wealth = IntField(default=0)
    used_as_input = ListField(EmbeddedDocumentField(Transaction))
    used_as_output = ListField(EmbeddedDocumentField(Transaction))

    meta = {'allow_inheritance': True}