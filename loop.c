#include <stdio.h>
#include <omp.h>

#define N 100
float a[N], b[N], result[N];

void parallel_addition() {
    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        result[i] = a[i] + b[i];
    }
}

int main() {
    for (int i = 0; i < N; i++) {
        a[i] = (float)i;
        b[i] = (float)(i * 2);
    }

    parallel_addition();

    printf("Completed parallel addition.\n");
    return 0;
}
