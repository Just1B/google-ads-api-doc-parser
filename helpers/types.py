def type_to_bq_type(doc_type):

    switcher = {
        "STRING": "STRING",
        "RESOURCE_NAME": "STRING",
        "MESSAGE": "STRING",
        "ENUM": "STRING",
        "DOUBLE": "FLOAT",
        "INT64": "INTEGER",
    }

    return switcher.get(doc_type, "")