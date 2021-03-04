# https://developers.google.com/google-ads/api/reference/rpc/v6/GoogleAdsFieldDataTypeEnum.GoogleAdsFieldDataType?hl=en


def type_to_bq_type(doc_type):

    switcher = {
        "UNSPECIFIED": "STRING",
        "UNKNOWN": "STRING",
        "DATE": "DATE",
        "STRING": "STRING",
        "RESOURCE_NAME": "STRING",
        "MESSAGE": "STRING",
        "ENUM": "STRING",
        "DOUBLE": "FLOAT",
        "FLOAT": "FLOAT",
        "INT32": "INTEGER",
        "INT64": "INTEGER",
        "UINT64": "INTEGER",
        "BOOLEAN": "BOOLEAN",
    }

    return switcher.get(doc_type, "")