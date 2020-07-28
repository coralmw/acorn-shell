%module liblitepcie

%{
#include "../../build/acorn_cle_215/driver/user/liblitepcie.h"
%}

extern uint32_t litepcie_readl(int fd, uint32_t addr);
extern void litepcie_writel(int fd, uint32_t addr, uint32_t val);
extern void litepcie_reload(int fd);
