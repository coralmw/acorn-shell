# acorn-shell

This repo holds an effort to provide a dynamic hardware development enviroment for building software acellerated with reconfigurable logic.

The intent is to allow anyone to open a Python shell, write a nMigen module, and access it either in simulation or running inside a physically attached FPGA withuot leaving the shell. Massively inspired by Pynq, but combining the prototpying and build steps to allow for rapid custom gateware.

Currently, this is just a example of launching the excellent work of the LiteX team on a SQRL acorn PCIe attached FPGA, using the xilinx platform cable as a programmer.
