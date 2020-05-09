import re

line = """
-------------------------PerfKitBenchmarker Results Summary-------------------------
COREMARK:
  Coremark Score                     3610.447190                                (iterations="1000000" iterations_per_cpu="1000000" parallelism_method="PTHREAD" run_number="0" size="666" summary="CoreMark 1.0 : 3610.447190 / GCC5.4.0 20160609 -O2 -g -O2 -DMULTITHREAD=1 -DUSE_PTHREAD -DPERFORMANCE_RUN=1 -DPERFORMANCE_RUN=1  -lrt -lpthread / Heap" total_ticks="276974" total_time_sec="276.974")
  lscpu                                 0.000000                                (Architecture="x86_64" BogoMIPS="4600.00" Byte Order="Little Endian" CPU MHz="2300.000" CPU family="6" CPU op-mode(s)="32-bit, 64-bit" CPU(s)="1" Core(s) per socket="1" Flags="fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm invpcid_single pti ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt arat md_clear arch_capabilities" Hypervisor vendor="KVM" L1d cache="32K" L1i cache="32K" L2 cache="256K" L3 cache="46080K" Model="63" Model name="Intel(R) Xeon(R) CPU @ 2.30GHz" NUMA node(s)="1" NUMA node0 CPU(s)="0" On-line CPU(s) list="0" Socket(s)="1" Stepping="0" Thread(s) per core="1" Vendor ID="GenuineIntel" Virtualization type="full" node_name="pkb-17fdf7b7-0")
  proccpu                               0.000000                                (address sizes="46 bits physical, 48 bits virtual" bogomips="4600.00" bugs="cpu_meltdown itlb_multihit l1tf mds spec_store_bypass spectre_v1 spectre_v2 swapgs" cache size="46080 KB" cache_alignment="64" clflush size="64" cpu MHz="2300.000" cpu cores="1" cpu family="6" cpuid level="13" flags="abm aes apic arat arch_capabilities avx avx2 bmi1 bmi2 clflush cmov constant_tsc cpuid cx16 cx8 de erms f16c fma fpu fsgsbase fxsr ht hypervisor ibpb ibrs invpcid invpcid_single lahf_lm lm mca mce md_clear mmx movbe msr mtrr nonstop_tsc nopl nx pae pat pcid pclmulqdq pdpe1gb pge pni popcnt pse pse36 pti rdrand rdtscp rep_good sep smep ss ssbd sse sse2 sse4_1 sse4_2 ssse3 stibp syscall tsc tsc_adjust tsc_known_freq vme x2apic xsave xsaveopt xtopology" fpu="yes" fpu_exception="yes" microcode="0x1" model="63" model name="Intel(R) Xeon(R) CPU @ 2.30GHz" node_name="pkb-17fdf7b7-0" power management="" proccpu="address sizes,bogomips,bugs,cache size,cache_alignment,clflush size,cpu MHz,cpu cores,cpu family,cpuid level,flags,fpu,fpu_exception,microcode,model,model name,power management,siblings,stepping,vendor_id,wp" siblings="1" stepping="0" vendor_id="GenuineIntel" wp="yes")
  proccpu_mapping                       0.000000                                (node_name="pkb-17fdf7b7-0" proc_0="apicid=0;core id=0;initial apicid=0;physical id=0")
  End to End Runtime                  954.729400 seconds                       

-------------------------
For all tests: /dev/sda="10737418240" boot_disk_size="10" boot_disk_type="pd-standard" cloud="GCP" dedicated_host="False" gce_network_tier="premium" gce_shielded_secure_boot="False" image="ubuntu-1604-xenial-v20200429" image_family="ubuntu-1604-lts" image_project="ubuntu-os-cloud" kernel_release="4.15.0-1061-gcp" machine_type="f1-micro" num_cpus="1" numa_node_count="1" os_info="Ubuntu 16.04.6 LTS" os_type="ubuntu1604" perfkitbenchmarker_version="v1.12.0-1867-g0730a7a6" project="perfkitbenchmarks" tcp_congestion_control="cubic" vm_count="1" zone="us-central1-a"

"""

matchObj = re.match(r'((.|\n)*)node_name="pkb-(\w+)(.*?)', line, re.M|re.I)

if matchObj:
   print("matchObj.group(3) : '{}'".format(matchObj.group(3).strip()))
else:
   print("Failed!!")
