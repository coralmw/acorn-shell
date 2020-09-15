"""
struct litepcie_ioctl_reg {
    uint32_t addr;
    uint32_t val;
    uint8_t is_write;
};

struct litepcie_ioctl_icap {
    uint8_t addr;
    uint32_t data;
};


"""

import fcntl
from ioctl_opt import IOWR
import ctypes

class litepcie_ioctl_reg(ctypes.Structure):
    _fields_ = [("addr", ctypes.c_uint32),
                ("val", ctypes.c_uint32),
                ("is_write", ctypes.c_uint8)]

LITEPCIE_IOCTL = ord('S')
LITEPCIE_IOCTL_REG = IOWR(LITEPCIE_IOCTL, 0, litepcie_ioctl_reg) # magic numbers...

CSR_BASE = 0x82000000
CSR_IDENTIFIER_MEM_BASE = CSR_BASE + 0x1000

# class litepcie_ioctl_reg():
#
#
#     def __init__(self, addr=None, val=None, is_write=None, data=None):
#         if (addr is not None) and (val is not None) and (is_write is not None):
#             self.addr = addr
#             self.val = val
#             self.is_write = is_write
#             self.data = struct.pack(self.fmt, (addr, val, is_write))
#         else if data is not None:
#             addr, val, data = struct.unpack(fmt, data)
#         else:
#             raise ValueError

def readl(fd, addr):
    msg = litepcie_ioctl_reg(addr, val=0, is_write=False)
    fcntl.ioctl(fd, LITEPCIE_IOCTL_REG, msg)
    return msg.val

def info():
    fd = open("/dev/litepcie0", "rb")
    id = ""
    for i in range(256):
        nxt_chr = chr(readl(fd, CSR_IDENTIFIER_MEM_BASE + 4*i))
        if nxt_chr == '\0':
            break
        id += nxt_chr
    print(id)

info()
