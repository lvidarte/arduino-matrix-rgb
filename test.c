#include <stdio.h>

int main(int argc, char **argv) {
    int n = 180;
    printf("01110001 10110100\n");
    printf("x = %d\n", (n & 7));
    printf("y = %d\n", ((n >> 3) & 7));
    printf("r0 = %d\n", (n >> 6));
    int m = 113;
    printf("r1 = %d\n", (m & 9));
    printf("r = %d\n", (n >> 6) | (m & 9));
    printf("g = %d\n", ((m >> 1) & 7));
    printf("b = %d\n", ((m >> 4) & 7));
    printf("f = %d\n", (m >> 9));
    return 0;
}
