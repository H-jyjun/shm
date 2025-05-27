#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <utility>
#include <vector>

using namespace std;

double quadFunction(double x, double a, double b, double c) {
    return a * x * x + b * x + c;
}

// 라그랑주 보간으로 y = ax^2 + bx + c 계수 계산
void lagrangeGeneralForm(vector<pair<double, double>> pts) {
    double x0 = pts[0].first, y0 = pts[0].second;
    double x1 = pts[1].first, y1 = pts[1].second;
    double x2 = pts[2].first, y2 = pts[2].second;

    // 기본 라그랑주 다항식 L0, L1, L2에 대해 전개한 결과의 계수를 수작업 계산
    // L0(x) = [(x - x1)(x - x2)] / [(x0 - x1)(x0 - x2)]
    // L1(x) = [(x - x0)(x - x2)] / [(x1 - x0)(x1 - x2)]
    // L2(x) = [(x - x0)(x - x1)] / [(x2 - x0)(x2 - x1)]

    double denom0 = (x0 - x1) * (x0 - x2);
    double denom1 = (x1 - x0) * (x1 - x2);
    double denom2 = (x2 - x0) * (x2 - x1);

    // 각각의 다항식을 전개: L(x) = A*x^2 + B*x + C
    double a0 = y0 / denom0;
    double a1 = y1 / denom1;
    double a2 = y2 / denom2;

    // 각 항의 x^2, x, 상수항 계수 계산
    double A = a0 + a1 + a2;

    double B = -a0 * (x1 + x2) - a1 * (x0 + x2) - a2 * (x0 + x1);

    double C = a0 * x1 * x2 + a1 * x0 * x2 + a2 * x0 * x1;

    printf("\n일반화된 이차 함수: y = %.4fx^2 + %.4fx + %.4f\n", A, B, C);
}

int main() {
    srand((unsigned int)time(NULL));

    int a = rand() % 5 + 1;           // 1~5
    int b = rand() % 11 - 5;          // -5~5
    int c = rand() % 21 - 10;         // -10~10

    printf("랜덤 생성된 2차 함수: f(x) = %dx^2 + %dx + %d\n", a, b, c);

    vector<pair<double, double>> points;
    printf("\n생성된 순서쌍 (x, y):\n");
    for (int i = 0; i < 10; ++i) {
        double x = i;
        double y = quadFunction(x, a, b, c);
        points.push_back({x, y});
        printf("(%.0f, %.2f)\n", x, y);
    }

    vector<pair<double, double>> inputPoints;
    printf("\n(x, y) 순서쌍 3개를 입력하세요:\n");
    for (int i = 0; i < 3; ++i) {
        double x, y;
        printf("%d번째 x y: ", i + 1);
        scanf("%lf %lf", &x, &y);
        inputPoints.push_back({x, y});
    }

    lagrangeGeneralForm(inputPoints);

    return 0;
}
