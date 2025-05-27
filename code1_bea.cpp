#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define P 2089  // 작은 소수 (mod 연산용)

// 모듈로 역수 (페르마의 소정리 사용: a^(p-2) mod p)
int modinv(int a, int p) {
    int res = 1;
    int exp = p - 2;
    while (exp) {
        if (exp % 2) res = (res * a) % p;
        a = (a * a) % p;
        exp /= 2;
    }
    return res;
}

// 다항식 계산: f(x) = a0 + a1*x + a2*x^2 + ...
int eval(int *coeffs, int k, int x) {
    int res = 0, xi = 1;
    for (int i = 0; i < k; i++) {
        res = (res + coeffs[i] * xi) % P;
        xi = (xi * x) % P;
    }
    return res;
}

// Lagrange 보간법으로 x=0에서의 y값(비밀) 복원
int reconstruct(int *x, int *y, int k) {
    int secret = 0;
    for (int i = 0; i < k; i++) {
        int num = 1, den = 1;
        for (int j = 0; j < k; j++) {
            if (i != j) {
                num = (num * (-x[j] + P)) % P;
                den = (den * (x[i] - x[j] + P)) % P;
            }
        }
        int li = (num * modinv(den, P)) % P;
        secret = (secret + y[i] * li) % P;
    }
    return secret;
}

int main() {
    srand(time(0));

    int secret = rand()%P;   // 비밀
    int n = 5;            // 생성할 조각 수
    int k = 3;            // 복원에 필요한 최소 조각 수

    int coeffs[k];
    coeffs[0] = secret;
    for (int i = 1; i < k; i++) {
        coeffs[i] = rand() % P;
    }

    // 조각 생성
    int x[5], y[5];
    printf("생성된 조각들 (x, y):\n");
    for (int i = 0; i < n; i++) {
        x[i] = i + 1;
        y[i] = eval(coeffs, k, x[i]);
        printf("(%d, %d)\n", x[i], y[i]);
    }

    // 일부 조각으로 복원
    printf("\n복원할 조각 3개 선택 (예: 1 2 4): ");
    int xi[3], yi[3];
    for (int i = 0; i < k; i++) {
        int idx;
        scanf("%d", &idx);
        xi[i] = x[idx - 1];
        yi[i] = y[idx - 1];
    }

    int recovered = reconstruct(xi, yi, k);
    printf("복원된 비밀: %d\n", recovered);

    return 0;
}

