from functools import partial
import struct

class Record:
    """
    Representation of a single Record in the SIO file.

    Data can be optionally `None` if it was not loaded.
    """
    def __init__(self, name, compressed, size_uncompressed, data=None):
        self.name             =name
        self.compressed       =compressed
        self.size_uncompressed=size_uncompressed

        self.data             =data

def read_sio(path, skip_data=True):
    """
    Iterate over different records inside a SIO file.

    If `skip_data=False`, then all blocks are loaded uncompressed.

    Parameters:
     path (str): Path to SIO file.
     skip_data (bool): Do not load blocks
    """

    fh=open(path, mode='rb')

    # Iterate over all data.
    # End is determined when we can no longer read another header length
    for header_len in iter(partial(fh.read, 4), b''):
        header_len = struct.unpack('>I',header_len)[0]

        header_data= fh.read(header_len-4)

        # Parse the header
        frame_magic, options, record_len_comp, record_len_real, recname_len = \
            struct.unpack('>IIIII',header_data[:5*4])
        header_data=header_data[5*4:] # unparsed header data

        # Parse header options
        if frame_magic!=0xABADCAFE:
            raise RuntimeError(f'Bad header magic: 0x{frame_magic:08X}')

        compressed     = (options>>0)&0x1==1
        recname        = header_data[:recname_len].decode()
        header_data=header_data[recname_len:] # unparsed header_data

        if record_len_comp%4!=0: # account for padding
            record_len_comp+=4-(record_len_comp%4)
        
        # Read/skip the data
        data=None
        if skip_data:
            fh.seek(record_len_comp,1)
        else:
            data=fh.read(record_len_comp)

        # Create and return object
        yield Record(recname, compressed, record_len_real, data)
