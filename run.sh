#!/bin/bash

run_clean(){
rm -f ymlc_exe
}

run_make(){
rm -f ymlc_exe
gcc -O0 ymlc.c -o ymlc_exe
#gcc -O0 ymlc.c -DCOUNT=384 -o ymlc_exe
#gcc -O0 ymlc.c -DCOUNT=4096 -o ymlc_exe
#gcc -O0 ymlc.c -DCOUNT=32768 -o ymlc_exe
#gcc -O0 ymlc.c -DCOUNT=1638400 -o ymlc_exe
#gcc -O0 ymlc.c -DCOUNT=1638400 -DRANDOM -o ymlc_exe
#gcc -O0 ymlc.c -DINTERLEAVE_NUM=8 -o ymlc_exe
}

run_run(){

# - disable hardware prefetch
# - for Xeon
sudo wrmsr -a 0x1a4 0xf
# - for Xeon Phi
#sudo wrmsr -a 0x1a4 07
# - check
sudo rdmsr 0x1a4
:<<COMMENT
COMMENT

#./ymlc_exe
numactl --physcpubind=0 --membind=0 ./ymlc_exe

# - restore hardware prefetch to the original (enabling) setting
sudo wrmsr -a 0x1a4 0
# - check
sudo rdmsr 0x1a4
:<<COMMENT
COMMENT

}


#----------------main--------------------
if [ $# -eq 1 ]; then
	if [ $1 = "make" ]; then
		run_make
	elif [ $1 = "clean" ]; then
		run_clean
	elif [ $1 = "run" ]; then
		run_run
	else
		echo "unknown argument"
	fi
else
	echo "argument num should be 1"
fi


