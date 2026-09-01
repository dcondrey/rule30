/* equiv_check.c -- verify that the longest repeated factor L of a prefix equals
 * the longest local period-agreement run:
 *     L == max over q>=1 of  (longest run of consecutive k with w[k] == w[k+q])
 * A repeated factor w[i..i+L-1] == w[j..j+L-1] with q = j-i IS a period-q
 * agreement running L positions, and conversely. If this holds, the subword
 * route and the direct periodicity scan are literally the same statement, and
 * the prefix is consistent with eventual period (r,q) iff r+q >= N-L.
 * Brute force O(N^2); run on small prefixes only.
 * Build: cc -O3 -o equiv_check equiv_check.c ; Usage: ./equiv_check f.bin N */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int c, char **v){
    FILE*f=fopen(v[1],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); fseek(f,0,SEEK_SET);
    unsigned char*d=malloc(sz); if(fread(d,1,sz,f)!=(size_t)sz)return 1; fclose(f);
    uint64_t N=strtoull(v[2],NULL,10);
    #define B(i) ((d[(i)>>3]>>((i)&7))&1)
    uint64_t best=0, bestq=0;
    for(uint64_t q=1;q<N;q++){
        uint64_t run=0;
        for(uint64_t k=0;k+q<N;k++){
            if(B(k)==B(k+q)){ if(++run>best){best=run;bestq=q;} } else run=0;
        }
    }
    printf("N=%llu  longest period-agreement run = %llu (at offset q=%llu)\n",
           (unsigned long long)N,(unsigned long long)best,(unsigned long long)bestq);
    return 0;
}
