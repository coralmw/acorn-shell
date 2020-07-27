execute `python run.py`. builds, flashes, tests a design for the SQRL.

# getting started with NiteFury on Ubuntu 19.04

0) Use 18.04. XDMA drivers installed but did not work on 19.04
1) get Vivado 2018.3 Webpack
2) get a JTAG programming adaptor - I got the ebay WvaeShare clone cable
3) set up the cable driver. Method 1 from https://github.com/timvideos/litex-buildenv/wiki/Xilinx-Platform-Cable-USB-under-Linux worked for me. You NEED ISE 14.7 bins - the files of the same name from vivado do not work for me.
4) set up PCIe drivers for the Xilinx ref PCIe design for XDMA

https://www.xilinx.com/support/answers/65444.html

Drivers here: https://github.com/Xilinx/dma_ip_drivers
for 19.04, needed to patch slightly. Content of a relevent Xilinx post:

```
Re: PCIe DMA driver compilation issues in Linux Ubuntu 19.04
Answering my own question..

There are two problems with compiling the driver with kernel 5.0.0-29:

1) The interface of linux/swait.h changed from the previous versions of the kernel..

Inside libxdma.c replace

- swait_event_interruptible_timeout
+ swait_event_interruptible_timeout_exclusive
and

- swake_up
+ swake_up_one
The correct approach should be find the version where this changes and add another #if LINUX_VERSION_CODE >= KERNEL_VERSION(x,x,x)..

2) The 5.0 kernel dropped the type argument to access_ok()

- access_ok(type, addr, size)
+ access_ok(addr, size)
Inside cdev_ctrl.c replace

- result = !access_ok(VERIFY_WRITE, (void __user *)arg,
+ result = !access_ok((void __user *)arg,
and

- result =  !access_ok(VERIFY_READ, (void __user *)arg,
+ result =  !access_ok( (void __user *)arg,
This will allow the compilation of the driver..
```

then run from within xdma
```
make -j
sudo make install
sudo depmod
```

before modprobe to get it to pick up the module. If working, tests/load_driver.sh should report loaded correctly and devices recognised.


when programmed with sample_0, lspci -vv output looks like this:

```
tparks@gpunode:/media/bulk/Projects/nitefury/NiteFury/Sample-Projects/Project-0/Host/Driver/Xilinx_Answer_65444_Linux_Files_rel20180420$ sudo lspci -s 04:00.0 -vv
04:00.0 Serial controller: Xilinx Corporation Device 7024 (prog-if 01 [16450])
	Subsystem: Xilinx Corporation Device 0007
	Control: I/O- Mem- BusMaster- SpecCycle- MemWINV- VGASnoop- ParErr- Stepping- SERR- FastB2B- DisINTx-
	Status: Cap+ 66MHz- UDF- FastB2B- ParErr- DEVSEL=fast >TAbort- <TAbort- <MAbort- >SERR- <PERR- INTx-
	Interrupt: pin A routed to IRQ 16
	NUMA node: 0
	Region 0: [virtual] Memory at dfb00000 (32-bit, non-prefetchable) [size=1M]
	Region 1: [virtual] Memory at dfc00000 (32-bit, non-prefetchable) [size=64K]
	Capabilities: [40] Power Management version 3
		Flags: PMEClk- DSI- D1- D2- AuxCurrent=0mA PME(D0+,D1+,D2+,D3hot+,D3cold-)
		Status: D0 NoSoftRst+ PME-Enable- DSel=0 DScale=0 PME-
	Capabilities: [48] MSI: Enable- Count=1/1 Maskable- 64bit+
		Address: 0000000000000000  Data: 0000
	Capabilities: [60] Express (v2) Endpoint, MSI 00
		DevCap:	MaxPayload 512 bytes, PhantFunc 0, Latency L0s <64ns, L1 unlimited
			ExtTag+ AttnBtn- AttnInd- PwrInd- RBE+ FLReset- SlotPowerLimit 75.000W
		DevCtl:	Report errors: Correctable- Non-Fatal- Fatal- Unsupported-
			RlxdOrd+ ExtTag- PhantFunc- AuxPwr- NoSnoop+
			MaxPayload 128 bytes, MaxReadReq 512 bytes
		DevSta:	CorrErr- UncorrErr- FatalErr- UnsuppReq- AuxPwr- TransPend-
		LnkCap:	Port #0, Speed 5GT/s, Width x4, ASPM L0s, Exit Latency L0s unlimited, L1 unlimited
			ClockPM- Surprise- LLActRep- BwNot- ASPMOptComp-
		LnkCtl:	ASPM Disabled; RCB 64 bytes Disabled- CommClk-
			ExtSynch- ClockPM- AutWidDis- BWInt- AutBWInt-
		LnkSta:	Speed 5GT/s, Width x4, TrErr- Train- SlotClk+ DLActive- BWMgmt- ABWMgmt-
		DevCap2: Completion Timeout: Range B, TimeoutDis-, LTR-, OBFF Not Supported
		DevCtl2: Completion Timeout: 50us to 50ms, TimeoutDis-, LTR-, OBFF Disabled
		LnkCtl2: Target Link Speed: 5GT/s, EnterCompliance- SpeedDis-
			 Transmit Margin: Normal Operating Range, EnterModifiedCompliance- ComplianceSOS-
			 Compliance De-emphasis: -6dB
		LnkSta2: Current De-emphasis Level: -6dB, EqualizationComplete-, EqualizationPhase1-
			 EqualizationPhase2-, EqualizationPhase3-, LinkEqualizationRequest-
	Capabilities: [100 v1] Device Serial Number 00-00-00-00-00-00-00-00
```
