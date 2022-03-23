#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ALLOC_MODE 0 //0:malloc, 1:Local variable, 2:Global variable 3:hbw_malloc

#define POINTER_SIZE 8 //Do not modify!; MEAN: MUST: sizeof(void *) == 8
#define CACHE_LINE_SIZE 64 //Byte; Basically, should not modify; MUST: CACHE_LINE_SIZE%POINTER_SIZE==0
//#define CACHE_LINE_SIZE 8 //for bandwidth
//#define CACHE_LINE_SIZE 256 //for 3D XPoint

#define INTERLEAVE_NUM 1 //2^n would work well. Others are doubtful. This just strides over cache lines. If set 2, Buffer Size is doubled. You must disable both h/w prefetch and RANDOM mode.

#define GOAL 0x11223344

#define RANDOM //Random access mode; If you can disable h/w prefetch, this is not necessary.

#define REP_NUM 10
//#define TIME_LIMIT 1 //second. This overrides REP_NUM

//measure main memory latency
#define COUNT 1638400 //Buffer size: 100MiB (64*1638400=104857600)

//measure cache latency
//for intel i7-7700K processors
//#define COUNT 512 //Buffer size: 32KiB (L1 Data cache / 1 core)
//#define COUNT 4096 //Buffer size: 256KiB (L2 cache / 1 core)
//#define COUNT 131072 //Buffer size: 8MiB (L3 cache)
//safer
//#define COUNT 410 //512*0.8
//#define COUNT 3277 //4096*0.8
//#define COUNT 104858 //131072*0.8

#if ALLOC_MODE == 2
	void *list[COUNT*INTERLEAVE_NUM*CACHE_LINE_SIZE/POINTER_SIZE];
#elif ALLOC_MODE == 3
	#include <hbwmalloc.h>
#endif


int main(int argc, char *argv[]){

	if(sizeof(void *) != POINTER_SIZE){
		printf("MUST: sizeof(void *) == POINTER_SIZE\n");
		return 0;
	} else if(CACHE_LINE_SIZE < POINTER_SIZE){
		printf("MUST: CACHE_LINE_SIZE >= POINTER_SIZE\n");
		return 0;
	} else if(CACHE_LINE_SIZE % POINTER_SIZE != 0){
		printf("MUST: CACHE_LINE_SIZE % POINTER_SIZE == 0\n");
		return 0;
	}

#if ALLOC_MODE == 0
	void **list = (void **)malloc((long long int)COUNT*INTERLEAVE_NUM*CACHE_LINE_SIZE);
#elif ALLOC_MODE == 1
	void *list[COUNT*INTERLEAVE_NUM*CACHE_LINE_SIZE/POINTER_SIZE];
#elif ALLOC_MODE == 3
	void **list = (void **)hbw_malloc((long long int)COUNT*INTERLEAVE_NUM*CACHE_LINE_SIZE);
#endif

	printf("Total buffer size: %lldByte\n", (long long int)COUNT*INTERLEAVE_NUM*CACHE_LINE_SIZE);

	//The line below doesn't work when COUNT is set over 2095000-ish (stack var limit)
	//int shuffle[COUNT];
	//so need to use malloc
	int *shuffle = (int *)malloc(sizeof(int)*COUNT);
	int i;
	for(i=0; i<COUNT; i++){
		shuffle[i] = i;
	}

#ifdef RANDOM
	printf("Random access mode\n");

	time_t seed=time(NULL);
	srand(seed);
	//printf("seed: %lld\n", seed);

	//Fisher-Yates shuffle algorithm
	int r, temp;
	for(i=COUNT; i>1; i--){
		r = rand()%i;
		if(r == i-1) continue;
		temp = shuffle[r];
		shuffle[r] = shuffle[i-1];
		shuffle[i-1] = temp;
	}
#else
	printf("Sequential access mode\n");
#endif

#if 0
	printf("shuffle[] dump end\n");
	for(i=0; i<COUNT; i++){
		printf("%d\n", shuffle[i]);
	}
	printf("shuffle[] dump end\n");
#endif

	//Loop of interleaving 
	int il=0;
	for(il=0; il<INTERLEAVE_NUM; il++){
		printf("Interleaving num: %d\n", il);

		//make linked list
		for(i=0; i<COUNT-1; i++){
			*(list + CACHE_LINE_SIZE/POINTER_SIZE*(shuffle[i]*INTERLEAVE_NUM+il)) = (list + CACHE_LINE_SIZE/POINTER_SIZE*(shuffle[i+1]*INTERLEAVE_NUM+il));
			if(*(list + CACHE_LINE_SIZE/POINTER_SIZE*(shuffle[i]*INTERLEAVE_NUM+il)) == (void *)GOAL){
				printf("Unfortunate fail. Try again.\n");
				return 0;
			}
		}
		*(list + CACHE_LINE_SIZE/POINTER_SIZE*(shuffle[COUNT-1]*INTERLEAVE_NUM+il)) = (void *)GOAL;

		void **pointer;
		pointer = (list + CACHE_LINE_SIZE/POINTER_SIZE*(shuffle[0]*INTERLEAVE_NUM+il)); //start point

#if 0
		printf("list:         %x\n", list);
		printf("list+8:       %x\n", list+8);
		printf("list+COUNT-1: %x\n", list+COUNT-1);
		printf("*list:        %x\n", *list);
		printf("list[0]:      %x\n", list[0]);
		printf("*(list+8):    %x\n", *(list+8));
		printf("pointer:      %x\n", pointer);
		printf("*pointer:     %x\n", *pointer);
#endif

		struct timespec ts1, ts2;
		double et_sec, lt_nsec, bw_gps;

#if 0
		struct timespect res;
		clock_getres(CLOCK_REALTIME, &res);
		//printf("clock_getres time resolution: %10ld.%09ld\n", res.tv_sec, res.tv_nsec);
		printf("clock_getres time resolution: %lldns\n", res.tv_nsec);
		clock_gettime(CLOCK_REALTIME, &ts1);
		clock_gettime(CLOCK_REALTIME, &ts2);
		//printf("clock_gettime (real) time resolution: %10ld.%09ld\n", ts2.tv_sec-ts1.tv_sec, ts2.tv_nsec-ts1.tv_nsec);
		printf("clock_gettime (real) time resolution: %lldns\n", ts2.tv_nsec-ts1.tv_nsec);
#endif

		//--------------------------------------------------
		//calc repetition num

		int rep = 1;
#ifdef REP_NUM
		rep = REP_NUM;
#endif
#ifdef TIME_LIMIT
		//test once
		clock_gettime(CLOCK_REALTIME, &ts1);
		while(*pointer != (void *)GOAL){
			pointer = (void **)(*pointer);
		}
		clock_gettime(CLOCK_REALTIME, &ts2);

		et_sec = (double)(ts2.tv_sec - ts1.tv_sec) + ((double)(ts2.tv_nsec - ts1.tv_nsec))*1.e-9;
		printf("First test: Elapsed time (s): %f\n", et_sec);

		lt_nsec = et_sec*1.e+9/(COUNT-1);
		printf("First test: Latency (ns): %f\n", lt_nsec);

		//bw_gps = ((double)((long long int)COUNT*CACHE_LINE_SIZE))/1.e+9/et_sec;
		//printf("First test: Bandwidth (GB/s): %f\n", bw_gps);

		rep =  (int)(TIME_LIMIT/et_sec); //round off
#endif
		if(rep<1) rep=1;
		printf("Repetition number: %d\n", rep);

		//--------------------------------------------------
		//measurement

		clock_gettime(CLOCK_REALTIME, &ts1);
		for(i=0; i<rep; i++){
			pointer = (list + CACHE_LINE_SIZE/POINTER_SIZE*(shuffle[0]*INTERLEAVE_NUM+il)); //start point
			while(*pointer != (void *)GOAL){
				pointer = (void **)(*pointer);
			}
		}
		clock_gettime(CLOCK_REALTIME, &ts2);

		et_sec = (double)(ts2.tv_sec - ts1.tv_sec) + ((double)(ts2.tv_nsec - ts1.tv_nsec))*1.e-9;
		printf("Repeated test: Total Elapsed time (s): %f\n", et_sec);

		lt_nsec = et_sec*1.e+9/(COUNT-1)/rep;
		printf("Repeated test: Latency (ns): %f\n", lt_nsec);

		//bw_gps = ((double)((long long int)COUNT*CACHE_LINE_SIZE))/1.e+9/et_sec*rep;
		//printf("Repeated test: Bandwidth (GB/s): %f\n", bw_gps);

	}

	return 0;

}



