import tkinter as tk
from tkinter import messagebox
import random

P = 2089

def modinv(a, p):
    return pow(a, p - 2, p)

def eval_poly(coeffs, x):
    result = 0
    xi = 1
    for coef in coeffs:
        result = (result + coef * xi) % P
        xi = (xi * x) % P
    return result

def reconstruct(x_vals, y_vals):
    k = len(x_vals)
    secret = 0
    for i in range(k):
        num = 1
        den = 1
        for j in range(k):
            if i != j:
                num = (num * (-x_vals[j] % P)) % P
                den = (den * (x_vals[i] - x_vals[j]) % P) % P
        li = (num * modinv(den, P)) % P
        secret = (secret + y_vals[i] * li) % P
    return secret

class ShamirGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shamir Secret Sharing")

        self.k = 3
        self.n = 5
        self.secret = random.randint(1, P - 1)
        self.coeffs = [self.secret] + [random.randint(1, P - 1) for _ in range(self.k - 1)]
        self.shares = [(i, eval_poly(self.coeffs, i)) for i in range(1, self.n + 1)]

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text=f"▶ 비밀 (Secret): {self.secret}").pack()

        shares_text = "\n".join([f"Share {i}: ({x}, {y})" for i, (x, y) in enumerate(self.shares, 1)])
        tk.Label(self.root, text=f"▶ 생성된 조각들:\n{shares_text}").pack()

        tk.Label(self.root, text=f"▶ 복원할 조각 {self.k}개를 선택하세요 (1~{self.n}):").pack()
        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        tk.Button(self.root, text="비밀 복원", command=self.recover_secret).pack()

    def recover_secret(self):
        try:
            selected = list(map(int, self.entry.get().split()))
            if len(selected) != self.k or any(i < 1 or i > self.n for i in selected):
                raise ValueError

            x_vals = [self.shares[i - 1][0] for i in selected]
            y_vals = [self.shares[i - 1][1] for i in selected]

            recovered = reconstruct(x_vals, y_vals)
            if recovered == self.secret:
                self.result_label.config(text=f"✅ 복원된 비밀: {recovered}\n✅ 성공적으로 복원되었습니다!", fg="green")
            else:
                self.result_label.config(text=f"❌ 복원 실패 (예상: {self.secret}, 결과: {recovered})", fg="red")
        except:
            messagebox.showerror("입력 오류", f"1~{self.n} 사이의 숫자 {self.k}개를 입력하세요.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShamirGUI(root)
    root.mainloop()
