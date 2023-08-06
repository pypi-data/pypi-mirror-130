import numpy as np
import six
import zstandard as zstd

if six.PY2:
    _ord = ord
else:
    _ord = lambda a: a

FILE_FORMAT_ID = b'BD'
FORMAT_VERSION = 3

DATA_FMT_UINT8 = 0
DATA_FMT_UINT16 = 1
DATA_FMT_FLOAT32 = 2

DATA_FMTS = ['u1', 'u2', 'f4']
DATA_FMTS_SIZES = [1, 2, 4]

DATA_COMP_RAW = 0
DATA_COMP_HUFFCODE = 1
DATA_COMP_HUFFCODE_CHUNKS = 2
DATA_COMP_ZSTD = 3
DATA_COMP_ZSTD_CHUNKS = 4

DATA_QUANT_NONE = 0
DATA_QUANT_SQRT = 1

header_dtype = [('ID', 'S2'), ('Version', 'u1'), ('DataFormat', 'u1'), ('DataCompression', 'u1'),
                ('DataQuantization', 'u1'), ('DimOrder', 'S1'), ('RESERVED0', 'S1'), ('SequenceID', 'i8'),
                ('FrameNum', 'u4'), ('Width', 'u4'), ('Height', 'u4'), ('Depth', 'u4'),
                ('FrameTimestamp', 'u8'), ('QuantOffset', 'f4'), ('QuantScale', 'f4')]

# v3 increases header size to support arbitrary offsets to img so that img can be aligned.
header_dtype_v3 = [('ID', 'S2'), ('Version', 'u1'), ('DataFormat', 'u1'), ('DataCompression', 'u1'),
                   ('DataQuantization', 'u1'), ('DimOrder', 'S1'), ('RESERVED0', 'S1'), ('SequenceID', 'i8'),
                   ('FrameNum', 'u4'), ('Width', 'u4'), ('Height', 'u4'), ('Depth', 'u4'),
                   ('FrameTimestamp', 'u8'), ('QuantOffset', 'f4'), ('QuantScale', 'f4'), ('DataOffset', 'u4'),
                   ('RESERVED1', 'S12')]

"""
numpy dtype used to define the file header struct.

Most of the entries should be fairly self explanatory, with the following
deserving a bit more explanation:

:ID: a 2-character string that we can test to see if the file type is consistent
:Version: the version of this format the file uses
:DataFormat: what the img type of individual pixels is
:DataCompression: whether the img is compressed, and which algorithm is used
:SequenceID: A unique identifier for the sequence to which this frame belongs.
    The most important property of this number is that it is unique to
    each sequence. A reasonable method of generation would be to use
    a unix-format integer timestamp for the first dword, and a random
    integer for the second. A hash of the first n image pixels could
    also be used.
:FrameNum: The position of this frame within the sequence
:FrameTimestamp: Space to save camera derived frame timestamps, if available
:Depth: As envisaged, the format is expected to contain individual 2D frames, with
    multiple frames being pulled together in a higher level container to
    construct a sequence or stack. Depth is included just because it doesn't
    take a significant ammount of extra space, but gives us flexibility for
    the future.
"""

HEADER_LENGTH = np.zeros(1, header_dtype).nbytes
HEADER_LENGTH_V3 = np.zeros(1, header_dtype_v3).nbytes


def ZstdDecompress(data_s, data_format):
    dctx = zstd.ZstdDecompressor()
    data = dctx.decompress(data_s)
    return np.frombuffer(data, dtype=data_format)


def load_header(datastring):
    if (_ord(datastring[2]) >= 3):
        return np.fromstring(datastring[:HEADER_LENGTH_V3], header_dtype_v3)
    else:
        return np.fromstring(datastring[:HEADER_LENGTH], header_dtype)


def loads(datastring):
    """
    Loads image img from a string in PZF format.

    Parameters
    ----------
    datastring : string / bytes
        The encoded img

    Returns
    -------

    img : ndarray
        The image img as a numpy array

    header : recarray
        The image header, as a numpy record array with the :const:`header_dtype` dtype.

    """
    header = load_header(datastring)

    if not header['ID'] == FILE_FORMAT_ID:
        raise RuntimeError("Invalid format: This doesn't appear to be a PZF file")

    if header['Version'] >= 2:
        dimOrder = header['DimOrder'][0]
    else:
        dimOrder = 'C'

    w, h, d = header['Width'][0], header['Height'][0], header['Depth'][0]

    if header['Version'] < 3:
        data_offset = HEADER_LENGTH
    else:
        data_offset = int(header['DataOffset'])

    data_s = datastring[data_offset:]
    data_format = DATA_FMTS[header['DataFormat'][0]]

    if header['DataCompression'] == DATA_COMP_RAW:
        data = np.fromstring(data_s, 'u1')
    elif header['DataCompression'] == DATA_COMP_ZSTD:
        data = ZstdDecompress(data_s, data_format)
    else:
        raise RuntimeError('Compression type not understood')

    if header['DataQuantization'] == DATA_QUANT_SQRT:
        # img = img.astype('f') * header['QuantScale']
        # img = (img * img + header['QuantOffset'])
        # img = img
        data = data.astype('u2') * data
    data = data.reshape([d, h, w], order=dimOrder).T

    return data, header
