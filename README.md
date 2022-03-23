# ymlc

Y Memory Latency Checker

## Usage

```
gcc -O0 ymlc.c -o ymlc_exe
numactl --physcpubind=0 --membind=0 ./ymlc_exe
```
or
```
run.sh make
run.sh run
```

See [ymlc.c](/ymlc.c) and [run.sh](/run.sh) for details.
You may need to modify arguments of numactl commands for your NUMA environment at least.

## Other Tools

- [makefig](/makefig/): Scripts for batch experiment and make good pics from the results.
- batch.sh: Scripts for batch experiment on many-core multi memory numa node environment. Outputs JSON file as a result.
- [core_puzzle](https://github.com/yuki1024/core_puzzle): https://yuki1024.github.io/core_puzzle/  Visualizes the result of batch.sh

## References

[HPC Asia 2020 Poster: Toward Latency-Aware Data Arrangement on Many-Core Processors](http://sighpc.ipsj.or.jp/HPCAsia2020/program.html)

## Acknowledgement

This work is partly supported by a project commissioned by the New Energy and Industrial Technology Development Organization (NEDO)

## Contact

yuki.t.ab@m.titech.ac.jp

Copyright (C) 2019, Tomoya Yuki. All Rights Reserved.
