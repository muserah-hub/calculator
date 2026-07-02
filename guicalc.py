import ast
import tkinter as tk
from tkinter import messagebox


ALLOWED_BIN_OPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a**b,
}
ALLOWED_UNARY_OPS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}


def _safe_eval(expr: str) -> float:
    """Safely evaluate a math expression using AST."""
    expr = expr.replace("^", "**")
    node = ast.parse(expr, mode="eval")
    return _eval_node(node.body)


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_BIN_OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError("Division by zero")
        return ALLOWED_BIN_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_UNARY_OPS:
        operand = _eval_node(node.operand)
        return ALLOWED_UNARY_OPS[type(node.op)](operand)
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Tuple):
        raise ValueError("Comma separated values are not supported.")
    raise ValueError("Invalid expression")


def build_ui() -> tk.Tk:
    root = tk.Tk()
    root.title("Calculator")
    root.resizable(False, False)

    expr_var = tk.StringVar()
    display = tk.Entry(root, textvariable=expr_var, font=("Segoe UI", 18), justify="right", bd=8, relief="sunken")
    display.grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky="nsew")

    def append(char: str) -> None:
        expr_var.set(expr_var.get() + char)

    def clear() -> None:
        expr_var.set("")

    def calculate() -> None:
        expression = expr_var.get().strip()
        if not expression:
            return
        try:
            result = _safe_eval(expression)
            expr_var.set(str(result))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    buttons = [
        ("7", lambda: append("7")), ("8", lambda: append("8")), ("9", lambda: append("9")), ("/", lambda: append("/")),
        ("4", lambda: append("4")), ("5", lambda: append("5")), ("6", lambda: append("6")), ("*", lambda: append("*")),
        ("1", lambda: append("1")), ("2", lambda: append("2")), ("3", lambda: append("3")), ("-", lambda: append("-")),
        ("0", lambda: append("0")), (".", lambda: append(".")), ("^", lambda: append("^")), ("+", lambda: append("+")),
    ]

    for idx, (text, cmd) in enumerate(buttons):
        row = 1 + idx // 4
        col = idx % 4
        tk.Button(root, text=text, width=5, height=2, font=("Segoe UI", 14), command=cmd).grid(
            row=row, column=col, padx=4, pady=4, sticky="nsew"
        )

    tk.Button(root, text="C", width=5, height=2, font=("Segoe UI", 14), command=clear).grid(
        row=5, column=0, padx=4, pady=4, sticky="nsew"
    )
    tk.Button(root, text="=", width=5, height=2, font=("Segoe UI", 14), command=calculate).grid(
        row=5, column=1, columnspan=3, padx=4, pady=4, sticky="nsew"
    )

    for i in range(6):
        root.rowconfigure(i, weight=1)
    for i in range(4):
        root.columnconfigure(i, weight=1)

    return root


def main() -> None:
    app = build_ui()
    app.mainloop()


if __name__ == "__main__":
    main()






