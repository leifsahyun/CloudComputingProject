import re

line = """COREMARK:
  Coremark Score                     3610.447190                                (iterations="1000000" iterations_per_cpu="1000000" parallelism_method="PTHREAD" run_number="0" size="666" summary="CoreMark 1.0 : 3610.447190 / GCC5.4.0 20160609 -O2 -g -O2 -DMULTITHREAD=1 -DUSE_PTHREAD -DPERFORMANCE_RUN=1 -DPERFORMANCE_RUN=1  -lrt -lpthread / Heap" total_ticks="276974" total_time_sec="276.974")
  lscpu                                 0.000000                                (Architecture="x86_64" BogoMIPS="4600.00" Byte Order="Little Endian" CPU MHz="2300.000" CPU family="6" CPU op-mode(s)="32-bit, 64-bit" CPU(s)="1" Core(s) per socket="1" Flags="fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities" Hypervisor vendor="KVM" L1d cache="32K" L1i cache="32K" L2 cache="256K" L3 cache="46080K" Model="63" Model name="Intel(R) Xeon(R) CPU @ 2.30GHz" NUMA node(s)="1" NUMA node0 CPU(s)="0" On-line CPU(s) list="0" Socket(s)="1" Stepping="0" Thread(s) per core="1" Vendor ID="GenuineIntel" Virtualization type="full" node_name="pkb-17fdf7b7-0")
  """

matchObj = re.match(r'((.|\n)*)node_name="pkb-(\w+)(.*?)', line, re.M|re.I)

if matchObj:
   print("matchObj.group(5) : '{}'".format(matchObj.group(3).strip()))
else:
   print("Failed!!")
