#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <windows.h>
#define P 2089


using namespace std;
// 모듈로 역수: a^(p-2) mod p
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
// 다항식 곱셈 (최대 2차 다항식)
vector<int> poly_mul(const vector<int>& A, const vector<int>& B) {
	vector<int> res(5, 0);
	for (size_t i = 0; i < A.size(); i++) {
		for (size_t j = 0; j < B.size(); j++) {
			if (i + j < 5) {
				res[i + j] = (res[i + j] + A[i] * B[j]) % P;
			}
		}
	}
	res.resize(3);
	return res;
}
// 다항식 스칼라 곱
vector<int> poly_scalar_mul(const vector<int>& A, int c) {
	vector<int> res(A.size());
	for (size_t i = 0; i < A.size(); i++) {
		res[i] = (A[i] * c) % P;
	}
	return res;
}
// 다항식 덧셈
vector<int> poly_add(const vector<int>& A, const vector<int>& B) {
	size_t n = max(A.size(), B.size());
	vector<int> res(n, 0);
	for (size_t i = 0; i < n; i++) {
		int a = (i < A.size()) ? A[i] : 0;
		int b = (i < B.size()) ? B[i] : 0;
		res[i] = (a + b) % P;
	}
	return res;
}
// 다항식 계산: f(x) = a0 + a1*x + a2*x^2 + ...
int eval(const vector<int>& coeffs, int k, int x) {
	int res = 0, xi = 1;
	for (int i = 0; i < k; i++) {
		res = (res + coeffs[i] * xi) % P;
		xi = (xi * x) % P;
	}
	return res;
}
// Lagrange 보간법으로 다항식 계수 복원
vector<int> lagrange_poly(int* x, int* y, int k) {
	vector<int> coeffs(k, 0);
	for (int i = 0; i < k; i++) {
		vector<int> numerator;
		numerator.push_back(1);
		int denominator = 1;
		for (int j = 0; j < k; j++) {
			if (i == j) continue;
			vector<int> factor;
			factor.push_back((P - x[j]) % P);
			factor.push_back(1);
			numerator = poly_mul(numerator, factor);
			denominator = (denominator * ((x[i] - x[j] + P) % P)) % P;
		}
		int inv_den = modinv(denominator, P);
		vector<int> term = poly_scalar_mul(numerator, (y[i] * inv_den) % P);
		coeffs = poly_add(coeffs, term);
	}
	return coeffs;
}
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    SetConsoleOutputCP(65001); 
    std::setlocale(LC_ALL, "");

	srand(time(0));
	int secret = rand() % P;
	int n = 5;
	int k = 3;
	vector<int> coeffs(k);
	coeffs[0] = secret;
	for (int i = 1; i < k; i++) {
		coeffs[i] = rand() % P;
	}
	int x[5], y[5];
	for (int i = 0; i < n; i++) {
		x[i] = i + 1;
		y[i] = eval(coeffs, k, x[i]);
	}
	// 오염 먼저 수행
	int corrupted_index = rand() % n;
	int noise = rand() % P;
	y[corrupted_index] = (y[corrupted_index] + noise) % P;
	cout << "생성된 조각들 (x, y):\n";
	for (int i = 0; i < n; i++) {
		cout << "(" << x[i] << ", " << y[i] << ")\n";
	}
	vector<vector<int> > comb;
	comb.push_back(vector<int>(3));
	comb[0][0] = 0; comb[0][1] = 1; comb[0][2] = 2;
	comb.push_back(vector<int>(3));
	comb[1][0] = 0; comb[1][1] = 1; comb[1][2] = 3;
	comb.push_back(vector<int>(3));
	comb[2][0] = 0; comb[2][1] = 1; comb[2][2] = 4;
	comb.push_back(vector<int>(3));
	comb[3][0] = 0; comb[3][1] = 2; comb[3][2] = 3;
	comb.push_back(vector<int>(3));
	comb[4][0] = 0; comb[4][1] = 2; comb[4][2] = 4;
	comb.push_back(vector<int>(3));
	comb[5][0] = 0; comb[5][1] = 3; comb[5][2] = 4;
	comb.push_back(vector<int>(3));
	comb[6][0] = 1; comb[6][1] = 2; comb[6][2] = 3;
	comb.push_back(vector<int>(3));
	comb[7][0] = 1; comb[7][1] = 2; comb[7][2] = 4;
	comb.push_back(vector<int>(3));
	comb[8][0] = 1; comb[8][1] = 3; comb[8][2] = 4;
	comb.push_back(vector<int>(3));
	comb[9][0] = 2; comb[9][1] = 3; comb[9][2] = 4;
	cout << "\n3조각 조합별 복원 다항식 (a2 x^2 + a1 x + a0):\n";
	for (size_t ci = 0; ci < comb.size(); ci++) {
		int xi[3], yi[3];
		for (int j = 0; j < k; j++) {
			xi[j] = x[comb[ci][j]];
			yi[j] = y[comb[ci][j]];
		}
		vector<int> poly = lagrange_poly(xi, yi, k);
		cout << "(" << xi[0] << "," << xi[1] << "," << xi[2] << "): ";
		cout << poly[2] << "x^2 + " << poly[1] << "x + " << poly[0] << "\n";
	}
	cout << "\n오염된 조각 탐지 및 복원 결과:\n";
	for (int i = 0; i < n; i++) {
		int correct_y = eval(coeffs, k, x[i]);
		if (y[i] != correct_y) {
			cout << "오염된 조각 : " << x[i] << "\n";
			cout << "조각 복원 결과 : (" << x[i] << ", " << correct_y << ")\n";
		}
	}
	return 0;
}