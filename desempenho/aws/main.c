#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>

uint64_t micros_since_epoch(){
    struct timeval tv;
    uint64_t micros = 0;
    gettimeofday(&tv, NULL);  
    micros =  ((uint64_t)tv.tv_sec) * 1000000 + tv.tv_usec;
    return micros;
}

int main(int argc, char* argv[]){
    FILE *fp;
    
    if (argc < 2) {
        printf("Falta nome do arquivo.\n");
        return 1;
    }
    
    
    fp = fopen(argv[1], "rb");
    if (fp == NULL) {
        printf("Erro abrindo arquivo");
        return 1;
    }
    fseek(fp, 0L, SEEK_END);    
    size_t file_size = ftell(fp);
    rewind(fp);
    
    int i;
    int block_size = 1024*1024;
    char *buf = (char*) malloc(sizeof(char)*block_size);
    int steps = (file_size/block_size);
    uint64_t start_time = micros_since_epoch();
    for(i=0; i<steps; ++i){
       fread(buf, block_size, 1, fp);
    }
    uint64_t end_time = micros_since_epoch();
    
    free(buf);
    fclose(fp);
    printf("%d, %4.6lf, %4.6lf\n", file_size, 
                                    (end_time-start_time)/1000., 
                                    (file_size/(1024*1024))/((end_time-start_time)/(1000.*1000.)));  

    return 0;
}
