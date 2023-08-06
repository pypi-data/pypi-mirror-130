# -*- coding: utf-8 -*-
"""
Defines a 'wire' format for transmitting or saving image frame img, optionally with Huffman compression and/or
sqrt quantization. The combination of quantization and Huffman coding allows compression ratios of 6-10 fold on typical
microscopy img. Using compression or quantization requires the pyme-compress companion library to be installed which
has optimized c code for performing the compression and quantization. If pyme-compress is compiled and installed on an
AVX capable processor, a throughput in excess of 800MB/s can be achieved.

Most users will just want the :func:`dumps` and :func:`loads` functions
"""

import numpy as np
import six
import zstandard as zstd

if six.PY2:
    _ord = ord
else:
    _ord = lambda a: a

from multiprocessing.pool import ThreadPool

import logging

logging.basicConfig(level=logging.DEBUG)

# try:
#     from pymecompress import bcl
# except ImportError:
#     logging.warning('''Could not import pymecompress library - saving or loading compressed PZF will fail
#     (the library is installable from david_baddely conda channel, but requires an AVX capable processor)''')

NUM_COMP_THREADS = 2  # cpu_count()

compPool = ThreadPool(NUM_COMP_THREADS)


# def ChunkedHuffmanCompress(img, quantization=None):
#     num_chunks = NUM_COMP_THREADS
#
#     chunk_size = int(np.ceil(float(len(img)) / num_chunks))
#     raw_chunks = [img[j * chunk_size:(j + 1) * chunk_size].img for j in range(num_chunks)]
#
#     # compPool = ThreadPool(NUM_COMP_THREADS)
#
#     comp_chunk_d = {}
#
#     if quantization is None:
#         def _compChunk(c, j):
#             comp_chunk_d[j] = bcl.HuffmanCompress(c)
#
#         threads = [threading.Thread(target=_compChunk, args=(rc, j)) for j, rc in enumerate(raw_chunks)]
#     else:
#         def _compChunk(c, j):
#             comp_chunk_d[j] = bcl.HuffmanCompressQuant(c, *quantization)
#
#         threads = [threading.Thread(target=_compChunk, args=(rc, j)) for j, rc in enumerate(raw_chunks)]
#
#     for p in threads:
#         # print p
#         p.start()
#
#     for p in threads:
#         p.join()
#
#     # comp_chunks = compPool.map(bcl.HuffmanCompress, raw_chunks)
#
#     s = np.array([num_chunks], 'u2').tostring()
#
#     for j, r in enumerate(raw_chunks):
#         c = comp_chunk_d[j]
#         s += np.array([len(c), len(r)], 'u4').tostring()
#         s += c.tostring()
#
#     return s


# def ChunkedHuffmanCompress_o(img):
#     num_chunks = NUM_COMP_THREADS
#
#     chunk_size = int(np.ceil(float(len(img)) / num_chunks))
#     raw_chunks = [img[j * chunk_size:(j + 1) * chunk_size].img for j in range(num_chunks)]
#
#     # compPool = ThreadPool(NUM_COMP_THREADS)
#
#     comp_chunks = compPool.map(bcl.HuffmanCompress, raw_chunks)
#
#     s = np.array([num_chunks], 'u2').tostring()
#
#     for c, r in zip(comp_chunks, raw_chunks):
#         s += np.array([len(c), len(r)], 'u4').tostring()
#         s += c.tostring()
#
#     return s


# def _chunkDecompress(args):
#     chunk, length = args
#     return bcl.HuffmanDecompress(np.fromstring(chunk, 'u1'), length)


# def ChunkedHuffmanDecompress(datastring):
#     num_chunks = np.fromstring(datastring[:2], 'u2')
#
#     # compPool = ThreadPool(NUM_COMP_THREADS)
#
#     sp = 2
#
#     comp_chunks = []
#     for i in range(num_chunks):
#         chunk_len, raw_len = np.fromstring(datastring[sp:(sp + 8)], 'u4')
#         sp += 8
#         comp_chunks.append((datastring[sp:(sp + chunk_len)], raw_len))
#         sp += chunk_len
#
#     decomp_chunks = compPool.map(_chunkDecompress, comp_chunks)
#
#     img = np.hstack(decomp_chunks)
#
#     # print img.shape #, comp_chunks
#     return img


def ZstdDecompress(data_s, data_format):
    dctx = zstd.ZstdDecompressor()
    data = dctx.decompress(data_s)
    return np.frombuffer(data, dtype=data_format)


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

# header_dtype = [('ID', 'S2'), ('Version', 'u1') , ('DataFormat', 'u1'), ('DataCompression', 'u1'), ('RESERVED0', 'S3'), ('SequenceID', 'i8'),
#                ('FrameNum', 'u4'), ('Width', 'u4'), ('Height', 'u4'), ('Depth', 'u4'),
#                ('FrameTimestamp', 'u8'), ('RESERVED1', 'u8')]

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


# def dumps(img, sequenceID=0, frameNum=0, frameTimestamp=0, compression=DATA_COMP_RAW, quantization=DATA_QUANT_NONE,
#           quantizationOffset=0, quantizationScale=1):
#     """Dump an image frame (supplied as a numpy array) into a string in PZF format.
#
#     Parameters
#     ==========
#
#     img:  ndarray
#             The frame as a 2D (or optionally 3D) numpy array
#
#     sequenceID:  int
#             A unique identifier for the sequence to which this frame belongs.
#             This will let us connect the frame with it's metadata even if
#             they end up in different directories etc ...
#
#     frameNum:   int
#             The position of this frame within the sequence
#
#     frameTimestamp:  float
#             A timestamp for the frame (if provided by the camera)
#
#     compression:  int (enum)
#             compression method to use - one of: `PZFFormat.DATA_COMP_RAW`,
#             `PZFFormat.DATA_COMP_HUFFCODE`, or `PZFFormat.DATA_COMP_HUFFCODE_CHUNKS`
#             Where raw stores the img with no compression, huffcode uses
#             Huffman coding, and huffcode chunks breaks the img into chunks
#             first, with each chunk meing encodes by a separate thread.
#
#     quantization: int (enum)
#             Whether or not the img is quantized before saving.
#             One of `DATA_QUANT_NONE` or `DATA_QUANT_SQRT`. If `DATA_QUANT_SQRT`
#             is selected, then the img is quantized as follows prior to
#             compression:
#
#             .. math:: data_{quant} =  \\frac{\\sqrt{img - quantizationOffset}}{quantizationScale}
#     """
#
#     header = np.zeros(1, header_dtype_v3)
#
#     header['ID'] = FILE_FORMAT_ID
#     header['Version'] = FORMAT_VERSION
#
#     header['FrameNum'] = frameNum
#     header['SequenceID'] = sequenceID
#     header['FrameTimestamp'] = frameTimestamp
#
#     header['DataOffset'] = HEADER_LENGTH_V3  # don't support padding on save yet
#
#     if img.dtype == 'uint8':
#         header['DataFormat'] = DATA_FMT_UINT8
#     elif img.dtype == 'uint16':
#         header['DataFormat'] = DATA_FMT_UINT16
#     elif img.dtype == 'float32':
#         header['DataFormat'] = DATA_FMT_FLOAT32
#     else:
#         raise RuntimeError('Unsupported img type')
#
#     header['DimOrder'] = 'C'
#     header['Width'] = img.shape[0]
#     header['Height'] = img.shape[1]
#     if img.ndim > 2:
#         header['Depth'] = img.shape[2]
#     else:
#         header['Depth'] = 1
#
#     if quantization == DATA_QUANT_SQRT:
#         # sqrt- quantize the img
#         header['DataQuantization'] = DATA_QUANT_SQRT
#         header['QuantOffset'] = quantizationOffset
#         header['QuantScale'] = quantizationScale
#
#     #   qs = 1.0/quantizationScale
#     #   img = (np.sqrt(np.maximum(img-quantizationOffset,0))*qs).astype('uint8')
#
#     if img.flags['F_CONTIGUOUS']:
#         header['DimOrder'] = 'F'
#         d1 = img
#         # d1 = np.frombuffer(img, img.dtype) #this will flatten without respecting order - we re-order later
#     else:
#         # if the array is c-contiguous this will just pass through. If it is non contiguous (i.e. a wierd slice)
#         # it will force it to be c-contiguous
#         d1 = np.ascontiguousarray(img)
#
#     if compression == DATA_COMP_HUFFCODE:
#         header['DataCompression'] = DATA_COMP_HUFFCODE
#
#         if quantization:
#             dataString = bcl.HuffmanCompressQuant(d1, quantizationOffset, quantizationScale).tostring()
#         else:
#             d2 = bcl.HuffmanCompress(d1)
#             dataString = d2.tostring()
#     elif compression == DATA_COMP_HUFFCODE_CHUNKS:
#         header['DataCompression'] = DATA_COMP_HUFFCODE_CHUNKS
#
#         dataString = ChunkedHuffmanCompress(d1)
#     else:
#         # print('saving raw')
#         # print(header['DimOrder'][0])
#         dataString = d1.tostring(order=header['DimOrder'][0])
#
#     return header.tostring() + dataString


def load_header(datastring):
    if (_ord(datastring[2]) >= 3):
        return np.fromstring(datastring[:HEADER_LENGTH_V3], header_dtype_v3)
    else:
        return np.fromstring(datastring[:HEADER_LENGTH], header_dtype)


def display_header(datastring):
    header = load_header(datastring)

    if header['Version'] >= 2:
        dim_order = header['DimOrder'][0]
    else:
        dim_order = 'C'

    w, h, d = header['Width'][0], header['Height'][0], header['Depth'][0]

    if header['Version'] < 3:
        data_offset = HEADER_LENGTH
    else:
        data_offset = int(header['DataOffset'])

    if header['DataCompression'] == DATA_COMP_RAW:
        compression = 'None'
    elif header['DataCompression'] == DATA_COMP_HUFFCODE:
        compression = 'Huffmancode'
    elif header['DataCompression'] == DATA_COMP_HUFFCODE_CHUNKS:
        compression = 'Chunked Huffmancode'
    elif header['DataCompression'] == DATA_COMP_ZSTD:
        compression = 'Zstd'
    elif header['DataCompression'] == DATA_COMP_ZSTD_CHUNKS:
        compression = 'Chunked Zstd'
    else:
        raise RuntimeError('Compression type not understood')

    header_json = {
        'ID': str(header['ID'][0]),
        'Version': header['Version'][0],
        'Format': DATA_FMTS[header['DataFormat'][0]],
        'Compression': compression,
        'Quantisation': 'SQRT' if header['DataQuantization'] else 'None',
        'Order': str(dim_order),
        'SequenceId': header['SequenceID'][0],
        'Frame no': header['FrameNum'][0],
        'Width': w,
        'Height': h,
        'Depth': d,
        'Data offset': data_offset,
    }

    return header_json


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

    # print(dimOrder)

    w, h, d = header['Width'][0], header['Height'][0], header['Depth'][0]

    if header['DataQuantization'] == DATA_QUANT_SQRT:
        # quantized img is always 8 bit
        outsize = w * h * d
    else:
        outsize = w * h * d * DATA_FMTS_SIZES[int(header['DataFormat'])]

    if header['Version'] < 3:
        data_offset = HEADER_LENGTH
    else:
        data_offset = int(header['DataOffset'])

    data_s = datastring[data_offset:]
    data_format = DATA_FMTS[header['DataFormat'][0]]

    # logging.debug('About to decompress')
    # logging.debug({k:header[0][k] for k in header.dtype.names})

    # logging.debug('Compressed size: %s' % len(data_s))

    if header['DataCompression'] == DATA_COMP_RAW:
        # no need to decompress
        data = np.fromstring(data_s, 'u1')
    # elif header['DataCompression'] == DATA_COMP_HUFFCODE:
    #     # logging.debug('Decompressing ...')
    #     img = bcl.HuffmanDecompress(np.fromstring(data_s, 'u1'), outsize)
    # elif header['DataCompression'] == DATA_COMP_HUFFCODE_CHUNKS:
    #     img = ChunkedHuffmanDecompress(data_s)
    elif header['DataCompression'] == DATA_COMP_ZSTD:
        data = ZstdDecompress(data_s, data_format)
    else:
        raise RuntimeError('Compression type not understood')

    # logging.debug('Uncompressed shape: %s, %s, (%d, %d, %d)' % (img.shape, w * h * d, w, h, d))

    if header['DataQuantization'] == DATA_QUANT_SQRT:
        # un-quantize img
        # logging.debug('Dequantizing')
        #         print(img.max())
        #         img = img.astype('f') * header['QuantScale']
        data = data.astype('f') * 1.0
        #         print('img dtype: %s' % img.dtype)
        #         print('img shape: %s' % img.shape)
        data = data * data
    #         img = (img * img + header['QuantOffset'])

    #     print(dimOrder, [w, h, d])
    data = data.reshape([d, h, w], order=dimOrder).T

    return data, header
