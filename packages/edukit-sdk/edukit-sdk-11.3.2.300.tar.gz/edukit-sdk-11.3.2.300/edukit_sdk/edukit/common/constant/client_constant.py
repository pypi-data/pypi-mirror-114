#  -*- coding: utf-8 -*-
#  Copyright (c) Huawei Technologies Co., Ltd. 2021-2021. All rights reserved.


class ClientConstant:
    FILE_SIZE = 'fileSize'
    FILE_SHA256 = 'fileSha256'
    RESOURCE_TYPE = 'resourseType'
    FILE_NAME = 'fileName'
    FILE = 'file'
    FILE_TYPE = 'fileType'
    PUBLIC_FILE = 'publicFile'
    PART_MAXSIZE = 'PART_MAXSIZE'
    TMP_UPLOAD_URL = 'tmpUploadUrl'
    UPLOAD_HEADERS = 'uploadHeaders'
    UPLOAD_METHOD = 'uploadMethod'
    FILE_ID = 'fileId'
    FILE_PARTS = 'fileParts'
    PART_OBJECT_ID = 'partObjectId'
    MATERIAL_URL = 'materialUrl'
    GOOGLE_GENERATION = 'googleGeneration'
    X_GOOGLE_GENERATION = 'X-Google-Generation'
    MULTI_PART_FLAG = 'multiPartFlag'
    UTF_8 = 'utf-8'
    RB = "rb"
    MAX_PAER_SIZE = 'maxPartSize'
    _HEADERS = '_headers'
    E_TAG = 'ETag'
    SERVER_DOMAIN = 'SERVER_DOMAIN'
    SDK_NAME = 'SDK_NAME'
    SDK_VERSION = 'SDK_VERSION'
    REQUESTING = 'Requesting'
    TUTOR_PORTRAIT = 'TUTOR_PORTRAIT'
    ERROR_MESSAGE = 'error_message'

    STATUS_TEXTS = {
        100: 'Continue',
        101: 'Switching Protocols',
        102: 'Processing',
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non-Authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        206: 'Partial Content',
        207: 'Multi-Status',
        208: 'Already Reported',
        226: 'IM Used',
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        307: 'Temporary Redirect',
        308: 'Permanent Redirect',
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Request Entity Too Large',
        414: 'Request-URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Requested Range Not Satisfiable',
        417: 'Expectation Failed',
        422: 'Unprocessable Entity',
        423: 'Locked',
        424: 'Failed Dependency',
        425: 'Reserved for WebDAV advanced collections expired proposal',
        426: 'Upgrade required',
        428: 'Precondition Required',
        429: 'Too Many Requests',
        431: 'Request Header Fields Too Large',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported',
        506: 'Variant Also Negotiates (Experimental)',
        507: 'Insufficient Storage',
        508: 'Loop Detected',
        510: 'Not Extended',
        511: 'Network Authentication Required'
    }
