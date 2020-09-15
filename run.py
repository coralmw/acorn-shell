import os
import argparse
import sys
from os import path
import shlex
import code

import acorn.acorn_cle_215 as acorn_cle_215
from acorn.target import BaseSoC
from litex.soc.integration.builder import builder_args, Builder, builder_argdict
from litex.soc.integration.soc_sdram import soc_sdram_args, soc_sdram_argdict
from litepcie.software import generate_litepcie_software

from sh import bash, lspci
import subprocess as sp

import importlib

def hot_reset():
    SQRL="1e24:021f"
    XILINX="10ee:7024"
    for vendor in [SQRL, XILINX]:
        device = lspci("-n", d=vendor).split(" ")[0]
        if device:
            break
    else:
        print("could not find device to reset")
        raise RuntimeError

    device = "0000:"+device
    print("resetting", device)
    sp.run(["sudo", "bash", f"{os.getcwd()}/tools/hot_reset.sh", device])

    old_wd = os.getcwd()
    try:
        os.chdir(path.join(old_wd, "build/acorn_cle_215/driver/kernel"))
        sp.run(["sudo", "rmmod", "litepcie"])
        sp.run(["sudo", "bash", "init.sh"])
        print("device power cycled")
    finally:
        os.chdir(old_wd) # don't mess up the shell

def build_mod():
    sp.run(shlex.split("sed -i '/CSR_CRG_RST_ADDR/d' build/acorn_cle_215/driver/kernel/main.c"))
    sp.run(shlex.split("make -C build/acorn_cle_215/driver/kernel litepcie.ko"))
    sp.run(shlex.split("make -C build/acorn_cle_215/driver/user all"))

    old_wd = os.getcwd()
    try:
        os.chdir(path.join(old_wd, "tools/liblitepcie"))
        sp.run(["make"])
    finally:
        os.chdir(old_wd) # don't mess up the shell
    # built a module: if we want it in the rest of this process, invalidate cache
    # sys.path.append(path.join(old_wd, "tools/liblitepcie"))
    importlib.invalidate_caches()

def test():
    sp.run(shlex.split("build/acorn_cle_215/driver/user/litepcie_util info"))

def main():
    parser = argparse.ArgumentParser(description="LiteX SoC on Acorn CLE 215+")
    parser.add_argument("--build",     action="store_true", help="Build bitstream", default=False)
    parser.add_argument("--with-pcie", action="store_true", help="Enable PCIe support", default=True)
    parser.add_argument("--driver",    action="store_true", help="Generate PCIe driver", default=False)
    parser.add_argument("--load",      action="store_true", help="Load bitstream", default=False)
    parser.add_argument("--flash",     action="store_true", help="Flash bitstream", default=False)
    builder_args(parser)
    soc_sdram_args(parser)
    args = parser.parse_args()
    args.uart_name="crossover"

    # get tools!
    sp.run(shlex.split("source /tools/Xilinx/Vivado/2019.1/settings64.sh"), shell=True)
    gcc_path = "litex-env/riscv64-unknown-elf-gcc-8.3.0-2019.08.0-x86_64-linux-ubuntu14/bin"
    sp.run(shlex.split(f"export PATH=$PATH:{path.join(os.getcwd(), gcc_path)}"), shell=True)

    # Enforce arguments
    args.csr_data_width = 32

    platform = acorn_cle_215.Platform()
    soc      = BaseSoC(platform, with_pcie=args.with_pcie, **soc_sdram_argdict(args))
    builder  = Builder(soc, **builder_argdict(args))
    builder.build(run=args.build)

    if args.driver:
        generate_litepcie_software(soc, os.path.join(builder.output_dir, "driver"))
        build_mod()

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(os.path.join(builder.gateware_dir, soc.build_name + ".bit"))
        hot_reset()

    if args.flash:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(os.path.join(builder.gateware_dir, soc.build_name + ".bin"))
        hot_reset()

    test()
    code.interact(local=dict(globals(), **locals()))

if __name__ == "__main__":
    main()
    # import tools.liblitepcie.liblitepcie as pcie
    # code.interact(local=dict(globals(), **locals()))
