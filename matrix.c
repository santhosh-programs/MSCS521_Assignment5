#include <stdio.h>
#include <stdlib.h>

#define N 128  

void matrix_vector_multiply(float matrix[N][N], float vector[N], float result[N]) {
    for (int i = 0; i < N; i++) {
        result[i] = 0;
        for (int j = 0; j < N; j++) {
            result[i] += matrix[i][j] * vector[j];
        }
    }
}

int main() {
    float matrix[N][N];
    float vector[N];
    float result[N];

    for (int i = 0; i < N; i++) {
        vector[i] = 1.0;
        for (int j = 0; j < N; j++) {
            matrix[i][j] = (float)(i + j);
        }
    }

    matrix_vector_multiply(matrix, vector, result);

    printf("Completed matrix-vector multiplication.\n");
    return 0;
}
