from m5.objects import *


class VectorFU(FUDesc):
    opList = [OpDesc(OpClass='SimdMult', opLat=8)]  # Example OpDesc
    count = 4


class VectorCPU(DerivO3CPU):
    fuPool = DefaultX86FUPool()


# System Configuration
system = System(
    clk_domain=SrcClockDomain(clock='4GHz', voltage_domain=VoltageDomain()),
    mem_mode='timing',  # Use timing mode for realistic memory simulation
    mem_ranges=[AddrRange('512MB')],  # Define memory size
    cpu=VectorCPU(
        numThreads=1,  # Example: 4 CPU threads
        #        fuPool = [
        #          *DefaultFUPool(), # Include standard functional units
        #           *VectorFU(),     # Add your vector functional units
        #     ]
    )
)


# Connect the cache to the CPU and memory
system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
# system.membus = SystemXBar()

system.cpu.createInterruptController()


# For X86 only we make sure the interrupts care connect to memory.
# Note: these are directly connected to the memory bus and are not cached.
# For other ISA you should remove the following three lines.
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports
# system.cache.mem_side = system.membus.mem_side_ports
system.mem_ctrl = MemCtrl(dram=DDR3_1600_8x8())
system.mem_ctrl.port = system.membus.mem_side_ports

# Set up the process and workload
thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(
    thispath,
    "../../../",
    "loop",
)

system.workload = SEWorkload.init_compatible(binary)
process = Process()
process.cmd = [binary]  # Example workload
system.cpu.workload = [process]
system.cpu.createThreads()

# Create a Root object and start the simulation
root = Root(full_system=False, system=system)
m5.instantiate()
print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
