#include <iostream>
#include <vector>
#include <random>
#include <ctime>

using namespace std;

const int MOD = 17;
const int k = 3;
const int n = 5;
const int x_new = 6;

// 모듈러 덧셈
int mod_add(int a, int b) {
    return (a + b) % MOD;
}

// 모듈러 곱셈
int mod_mul(int a, int b) {
    return (a * b) % MOD;
}

// 다항식 평가 (Horner's method 활용 가능하지만, 여기선 간단하게 구현)
int eval_poly(const vector<int>& coef, int x) {
    int result = 0;
    int x_pow = 1;
    for (int c : coef) {
        result = mod_add(result, mod_mul(c, x_pow));
        x_pow = mod_mul(x_pow, x);
    }
    return result;
}

// 난수 생성 (0~MOD-1)
int random_mod(mt19937& gen, int min = 0, int max = MOD - 1) {
    uniform_int_distribution<> dis(min, max);
    return dis(gen);
}

int main() {
    mt19937 gen(static_cast<unsigned int>(time(nullptr)));

    // 비밀 다항식 생성 (k-1 차, 상수항 = secret)
    vector<int> secret_poly(k, 0);
    secret_poly[0] = random_mod(gen); // 비밀 s
    for (int i = 1; i < k; ++i) {
        secret_poly[i] = random_mod(gen);
    }

    cout << "[Secret polynomial coefficients (constant term = secret s)]\n";
    for (int i = 0; i < k; ++i) {
        cout << "a_" << i << " = " << secret_poly[i] << (i == 0 ? " (secret s)" : "") << "\n";
    }
    cout << "\n";

    // 각 참가자 조각 생성 (기본적으로는 secret_poly를 x = i+1 에서 평가)
    vector<pair<int,int>> shares(n); // (x, f(x))
    for (int i = 0; i < n; ++i) {
        int x = i + 1;
        int y = eval_poly(secret_poly, x);
        shares[i] = {x, y};
        cout << "Participant " << x << " share: f(" << x << ") = " << y << "\n";
    }
    cout << "\n";

    // 새로운 참여자 x_new에서 다항식 평가 -> 새로운 조각 생성
    int new_share = eval_poly(secret_poly, x_new);
    cout << "New participant at x = " << x_new << " gets share: f(" << x_new << ") = " << new_share << "\n";

    return 0;
}
