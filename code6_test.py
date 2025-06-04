import tkinter as tk
from tkinter import messagebox
import random
from PIL import ImageGrab
import os

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

def reconstruct_poly(x_vals, y_vals):
    k = len(x_vals)
    terms = []
    secret = 0
    for i in range(k):
        num = 1
        den = 1
        for j in range(k):
            if i != j:
                num = (num * (-x_vals[j] % P)) % P
                den = (den * (x_vals[i] - x_vals[j]) % P) % P
        li = (num * modinv(den, P)) % P
        term = (y_vals[i] * li) % P
        secret = (secret + term) % P
        terms.append(term)
    return secret, terms

def poly_to_str(coeffs):
    terms = [f"{coef}" if i == 0 else f"{coef}x^{i}" for i, coef in enumerate(coeffs) if coef != 0]
    return " + ".join(terms) if terms else "0"

class ShamirGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shamir Secret Sharing")
        self.root.geometry("600x520")
        self.root.configure(bg='white')

        self.k = 3
        self.n = 5
        self.secret = random.randint(1, P - 1)
        self.coeffs = [self.secret] + [random.randint(1, P - 1) for _ in range(self.k - 1)]
        self.poly_str = poly_to_str(self.coeffs)
        self.shares = [(i, eval_poly(self.coeffs, i)) for i in range(1, self.n + 1)]

        self.create_widgets()

    def create_widgets(self):
        self.output_frame = tk.Frame(self.root, bg='white')
        self.output_frame.pack(pady=10)

        tk.Label(self.output_frame, text=f"▶ 생성된 다항식 (f(x)): {self.poly_str}", font=("Helvetica", 12), bg='white').pack(pady=5)

        shares_text = "\n".join([f"Share {i}: ({x}, {y})" for i, (x, y) in enumerate(self.shares, 1)])
        tk.Label(self.output_frame, text=f"▶ 생성된 조각들:\n{shares_text}", font=("Helvetica", 11), bg='white', justify='left').pack(pady=5)

        tk.Label(self.output_frame, text=f"▶ 복원할 조각 {self.k}개를 직접 입력하세요 (형식: x1,y1 x2,y2 x3,y3):", font=("Helvetica", 11), bg='white').pack()
        self.entry = tk.Entry(self.output_frame, width=50)
        self.entry.pack(pady=5)

        self.result_label = tk.Label(self.output_frame, text="", font=("Helvetica", 12), bg='white')
        self.result_label.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg='white')
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="비밀 및 방정식 복원", command=self.recover_secret, font=("Helvetica", 11), bg='#336699', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="이미지 저장 (PNG)", command=self.save_as_image, font=("Helvetica", 11), bg='#228B22', fg='white').pack(side='left', padx=5)

    def recover_secret(self):
        try:
            raw_input = self.entry.get().strip().split()
            selected = [tuple(map(int, pair.split(","))) for pair in raw_input]
            if len(selected) != self.k:
                raise ValueError

            x_vals = [pair[0] for pair in selected]
            y_vals = [pair[1] for pair in selected]

            recovered, terms = reconstruct_poly(x_vals, y_vals)
            recovered_str = poly_to_str(terms)

            result_text = f"✅ 복원된 비밀: {recovered}\n✅ 복원된 다항식 (f(x)): {recovered_str}"
            color = "green" if recovered == self.secret else "red"
            self.result_label.config(text=result_text, fg=color)
        except:
            messagebox.showerror("입력 오류", "입력 형식: x1,y1 x2,y2 x3,y3  (예: 1,123 2,456 4,789)")

    def save_as_image(self):
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        filepath = os.path.join(os.getcwd(), "shamir_output.png")
        ImageGrab.grab().crop((x, y, x + w, y + h)).save(filepath)
        messagebox.showinfo("저장 완료", f"이미지가 저장되었습니다:\n{filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShamirGUI(root)
    root.mainloop()
