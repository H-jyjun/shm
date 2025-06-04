import tkinter as tk
from tkinter import ttk
import random
from itertools import combinations

P = 2089

def modinv(a, p):
    res = 1
    exp = p - 2
    while exp:
        if exp % 2:
            res = (res * a) % p
        a = (a * a) % p
        exp //= 2
    return res

def poly_mul(A, B):
    res = [0] * 5
    for i in range(len(A)):
        for j in range(len(B)):
            if i + j < 5:
                res[i + j] = (res[i + j] + A[i] * B[j]) % P
    return res[:3]

def poly_scalar_mul(A, c):
    return [(a * c) % P for a in A]

def poly_add(A, B):
    n = max(len(A), len(B))
    res = [0] * n
    for i in range(n):
        a = A[i] if i < len(A) else 0
        b = B[i] if i < len(B) else 0
        res[i] = (a + b) % P
    return res

def eval_poly(coeffs, x):
    res = 0
    xi = 1
    for c in coeffs:
        res = (res + c * xi) % P
        xi = (xi * x) % P
    return res

def lagrange_poly(x, y, k):
    coeffs = [0] * k
    for i in range(k):
        numerator = [1]
        denominator = 1
        for j in range(k):
            if i == j:
                continue
            factor = [(-x[j]) % P, 1]
            numerator = poly_mul(numerator, factor)
            denominator = (denominator * (x[i] - x[j] + P)) % P
        inv_den = modinv(denominator, P)
        term = poly_scalar_mul(numerator, (y[i] * inv_den) % P)
        coeffs = poly_add(coeffs, term)
    return coeffs

class SecretSharingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shamir Secret Sharing (Visualized)")
        self.root.configure(bg="white")
        self.root.geometry("1000x750")

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 14), padding=10)

        self.frame = tk.Frame(self.root, bg="white")
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame, width=980, height=650, bg="white", highlightthickness=0)
        self.canvas.pack(side="top", pady=10)

        self.button = ttk.Button(self.frame, text="🔐 시크릿 공유 실행", command=self.run)
        self.button.pack(side="bottom", pady=10)

    def draw_secret_and_equation(self, secret, coeffs):
        equation = f"f(x) = {coeffs[2]}x² + {coeffs[1]}x + {coeffs[0]}"
        self.canvas.create_text(500, 30, text=f"비밀 값 (a₀): {secret}", font=("Helvetica", 16, "bold"), fill="black")
        self.canvas.create_text(500, 60, text=equation, font=("Helvetica", 14), fill="gray")

    def draw_shares(self, x_values, y_original, y_corrupted):
        self.canvas.create_text(300, 100, text="원래 조각들", font=("Helvetica", 14, "bold"), fill="black")
        self.canvas.create_text(700, 100, text="오염된 조각들", font=("Helvetica", 14, "bold"), fill="black")
        for i in range(len(x_values)):
            self.canvas.create_text(300, 130 + i * 30, text=f"({x_values[i]}, {y_original[i]})", font=("Helvetica", 12), fill="blue")
            color = "red" if y_original[i] != y_corrupted[i] else "black"
            self.canvas.create_text(700, 130 + i * 30, text=f"({x_values[i]}, {y_corrupted[i]})", font=("Helvetica", 12), fill=color)

    def draw_conversion_steps(self, coeffs, x_values, y_corrupted, k):
        self.canvas.create_text(500, 320, text="[과정] 10가지 조합의 복원 시도", font=("Helvetica", 14, "bold"), fill="black")
        combs = list(combinations(range(len(x_values)), k))
        for idx, c in enumerate(combs[:10]):
            xi = [x_values[i] for i in c]
            yi = [y_corrupted[i] for i in c]
            recovered = lagrange_poly(xi, yi, k)
            # 올바른 복원일 경우 초록, 아니면 빨강
            correct = all((a - b) % P == 0 for a, b in zip(recovered, coeffs))
            color = "green" if correct else "red"
            text = f"{idx+1:>2}. ({xi[0]}, {xi[1]}, {xi[2]}) → {recovered[2]}x² + {recovered[1]}x + {recovered[0]}"
            self.canvas.create_text(500, 350 + idx * 20, text=text, font=("Courier", 11), fill=color)

        # 올바른 식과 비밀 값 강조 표시
        self.canvas.create_text(500, 570, text="✔ 올바른 복원식:", font=("Helvetica", 14, "bold"), fill="darkgreen")
        equation = f"f(x) = {coeffs[2]}x² + {coeffs[1]}x + {coeffs[0]}"
        self.canvas.create_text(500, 600, text=equation, font=("Helvetica", 14, "bold"), fill="darkgreen")
        self.canvas.create_text(500, 630, text=f"비밀 값 (a₀): {coeffs[0]}", font=("Helvetica", 14, "bold"), fill="darkgreen")

    def draw_detection(self, x_values, y_original, y_corrupted):
        self.canvas.create_text(500, 660, text="🔍 오염 조각 탐지 결과", font=("Helvetica", 14, "bold"), fill="black")
        for i in range(len(x_values)):
            if y_original[i] != y_corrupted[i]:
                self.canvas.create_text(500, 690, text=f"❗ 오염된 조각: x = {x_values[i]} → 원래 y = {y_original[i]}", font=("Helvetica", 12), fill="red")

    def run(self):
        self.canvas.delete("all")
        secret = random.randint(0, P - 1)
        k, n = 3, 5
        coeffs = [secret] + [random.randint(0, P - 1) for _ in range(k - 1)]

        x_values = random.sample(range(10, 100), n)
        y_original = [eval_poly(coeffs, x) for x in x_values]
        y_corrupted = y_original.copy()

        corrupted_index = random.randint(0, n - 1)
        noise = random.randint(1, P - 1)
        y_corrupted[corrupted_index] = (y_corrupted[corrupted_index] + noise) % P

        self.draw_secret_and_equation(secret, coeffs)
        self.draw_shares(x_values, y_original, y_corrupted)
        self.draw_conversion_steps(coeffs, x_values, y_corrupted, k)
        self.draw_detection(x_values, y_original, y_corrupted)

if __name__ == "__main__":
    root = tk.Tk()
    app = SecretSharingGUI(root)
    root.mainloop()
