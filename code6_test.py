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
    coeffs = [0] * k
    secret = 0
    for i in range(k):
        num = 1
        den = 1
        for j in range(k):
            if i != j:
                num = (num * (-x_vals[j] % P)) % P
                den = (den * (x_vals[i] - x_vals[j]) % P) % P
        li = (num * modinv(den, P)) % P
        for j in range(k):
            power = 1
            for m in range(j):
                power = (power * x_vals[i]) % P
            coeffs[j] = (coeffs[j] + y_vals[i] * li * power) % P
        secret = (secret + y_vals[i] * li) % P
    return secret, coeffs

def poly_to_str(coeffs):
    terms = [f"{coef}" if i == 0 else f"{coef}x^{i}" for i, coef in enumerate(coeffs) if coef != 0]
    return " + ".join(terms) if terms else "0"

class ShamirGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shamir Secret Sharing")
        self.root.geometry("700x600")
        self.root.configure(bg='white')

        self.k = 3
        self.n = 5
        self.secret = random.randint(1, P - 1)
        self.coeffs = [self.secret] + [random.randint(1, P - 1) for _ in range(self.k - 1)]
        self.poly_str = poly_to_str(self.coeffs)

        x_values = random.sample(range(1, P), self.n)
        self.shares = [(x, eval_poly(self.coeffs, x)) for x in x_values]

        self.create_widgets()

    def create_widgets(self):
        self.output_frame = tk.Frame(self.root, bg='white')
        self.output_frame.pack(pady=10)

        tk.Label(self.output_frame, text=f"▶ 생성된 다항식 (f(x)): {self.poly_str}", font=("Helvetica", 12), bg='white').pack(pady=5)

        shares_text = "\n".join([f"Share {i}: ({x}, {y})" for i, (x, y) in enumerate(self.shares, 1)])
        tk.Label(self.output_frame, text=f"▶ 생성된 조각들:\n{shares_text}", font=("Helvetica", 11), bg='white', justify='left').pack(pady=5)

        tk.Label(self.output_frame, text=f"▶ 복원할 조각 3개를 입력하세요:", font=("Helvetica", 11), bg='white').pack(pady=5)

        self.entries = []
        entry_frame = tk.Frame(self.output_frame, bg='white')
        entry_frame.pack()

        labels = ["x₁", "y₁", "x₂", "y₂", "x₃", "y₃"]
        for i in range(3):
            for j in range(2):
                label = tk.Label(entry_frame, text=labels[i * 2 + j], bg='white', font=("Helvetica", 10))
                label.grid(row=i, column=j * 2, padx=5, pady=2)
                entry = tk.Entry(entry_frame, width=7)
                entry.grid(row=i, column=j * 2 + 1, padx=5, pady=2)
                self.entries.append(entry)

        self.result_label = tk.Label(self.output_frame, text="", font=("Helvetica", 12), bg='white')
        self.result_label.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg='white')
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="비밀 및 방정식 복원", command=self.recover_secret, font=("Helvetica", 11), bg='#336699', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="이미지 저장 (PNG)", command=self.save_as_image, font=("Helvetica", 11), bg='#228B22', fg='white').pack(side='left', padx=5)

    def recover_secret(self):
        try:
            x_vals, y_vals = [], []
            for i in range(3):
                x = int(self.entries[i * 2].get())
                y = int(self.entries[i * 2 + 1].get())
                x_vals.append(x)
                y_vals.append(y)

            recovered, coeffs = reconstruct_poly(x_vals, y_vals)
            recovered_str = poly_to_str(coeffs)

            result_text = f"✅ 복원된 비밀: {recovered}\n✅ 복원된 다항식 (f(x)): {recovered_str}"
            color = "green" if recovered == self.secret else "red"
            self.result_label.config(text=result_text, fg=color)
        except:
            messagebox.showerror("입력 오류", "각 x, y 값을 정수로 정확히 입력하세요.")

    def save_as_image(self):
        self.root.update()
        x = self.output_frame.winfo_rootx()
        y = self.output_frame.winfo_rooty()
        w = self.output_frame.winfo_width()
        h = self.output_frame.winfo_height()
        filepath = os.path.join(os.getcwd(), "shamir_output.png")
        ImageGrab.grab().crop((x, y, x + w, y + h)).save(filepath)
        messagebox.showinfo("저장 완료", f"이미지가 저장되었습니다:\n{filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShamirGUI(root)
    root.mainloop()
