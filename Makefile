# ENV SETUP
# export PYTHONPATH=$PYTHONPATH:`pwd`/litex
# source /tools/Xilinx/Vivado/2019.1/settings64.sh
# export PATH=$PATH:`pwd`/litex-env/riscv64-unknown-elf-gcc-8.3.0-2019.08.0-x86_64-linux-ubuntu14/bin

build/acorn_cle_215/gateware/acorn_cle_215.bit: acorn/target.py
	python3 acorn/target.py --uart-name=crossover --with-pcie --build --driver

load: acorn/target.py build/acorn_cle_215/gateware/acorn_cle_215.bit
	python3 acorn/target.py --uart-name=crossover --with-pcie --load

module:
	sed -i '/CSR_CRG_RST_ADDR/d' build/acorn_cle_215/driver/kernel/main.c
	make -C build/acorn_cle_215/driver/kernel litepcie.ko

.PHONY: reset
reset: module
	sudo ./hot_reset.sh `lspci -d 10ee:7024 -n | cut -d " " -f1`
	cd build/acorn_cle_215/driver/kernel && sudo rmmod litepcie || echo
	cd build/acorn_cle_215/driver/kernel && sudo bash init.sh || echo

util: build/acorn_cle_215/driver/user/liblitepcie.c build/acorn_cle_215/driver/kernel/csr.h
	make -C build/acorn_cle_215/driver/user all

run_test:
	make load
	make reset
	make util
	sudo build/acorn_cle_215/driver/user/litepcie_util info

# GOAL: one-command launch a shell with access to the CSRs in the device.
