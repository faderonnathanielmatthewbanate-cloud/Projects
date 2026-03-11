"""
╔══════════════════════════════════════════════════════╗
║           JOLLI-BAE RESTAURANT SYSTEM               ║
║        Beautiful Tkinter GUI Applet Edition         ║
║  Run with: python3 jolli_bae_gui.py                 ║
╚══════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import hashlib
import sys

# ══════════════════════════════════════════════════
#  THEME / PALETTE
# ══════════════════════════════════════════════════
C = {
    "red":        "#D62B2B",
    "red_dark":   "#A81E1E",
    "red_light":  "#FF5555",
    "yellow":     "#FFD000",
    "yellow_dk":  "#E6B800",
    "cream":      "#FFF8E7",
    "brown":      "#5C2D0E",
    "white":      "#FFFFFF",
    "gray":       "#F0EBE0",
    "gray_dark":  "#D8D0C0",
    "dark":       "#1A0A00",
    "green":      "#27AE60",
    "green_bg":   "#E8F8F0",
    "orange":     "#E67E22",
    "orange_bg":  "#FEF9E7",
    "danger":     "#E74C3C",
    "danger_bg":  "#FDEDEC",
    "sidebar_bg": "#2D1506",
    "sidebar_fg": "#FFD000",
    "header_bg":  "#D62B2B",
    "header_fg":  "#FFD000",
}

FONT_TITLE  = ("Georgia", 22, "bold")
FONT_HEADER = ("Georgia", 16, "bold")
FONT_SUB    = ("Georgia", 13, "bold")
FONT_BODY   = ("Helvetica", 11)
FONT_BOLD   = ("Helvetica", 11, "bold")
FONT_SMALL  = ("Helvetica", 9)
FONT_PRICE  = ("Georgia", 14, "bold")
FONT_BIG    = ("Georgia", 28, "bold")

# ══════════════════════════════════════════════════
#  DATA MODELS
# ══════════════════════════════════════════════════
class MenuItem:
    def __init__(self, name, price, stock, restock_price, restock_qty):
        self.name          = name
        self.price         = price
        self.stock         = stock
        self.restock_price = restock_price
        self.restock_qty   = restock_qty
        self.sold          = 0

    def is_available(self): return self.stock > 0
    def deduct(self, qty):  self.stock = max(0, self.stock - qty); self.sold += qty
    def restock(self, qty): self.stock += qty
    def restock_cost(self, qty=None): return (qty or self.restock_qty) * self.restock_price

    def status_text(self):
        if self.stock == 0:    return "OUT OF STOCK", C["danger"],    C["danger_bg"]
        if self.stock <= 5:    return f"Low ({self.stock})",  C["orange"],   C["orange_bg"]
        return f"In Stock ({self.stock})", C["green"], C["green_bg"]


class CartItem:
    def __init__(self, menu_item, quantity):
        self.menu_item = menu_item
        self.quantity  = quantity

    def subtotal(self): return self.menu_item.price * self.quantity


class Cart:
    def __init__(self): self.items = []

    def add(self, menu_item, quantity):
        for ci in self.items:
            if ci.menu_item.name == menu_item.name:
                ci.quantity += quantity; return
        self.items.append(CartItem(menu_item, quantity))

    def remove(self, idx):   self.items.pop(idx)
    def total(self):         return sum(ci.subtotal() for ci in self.items)
    def is_empty(self):      return len(self.items) == 0
    def clear(self):         self.items.clear()
    def qty_in_cart(self, name):
        for ci in self.items:
            if ci.menu_item.name == name: return ci.quantity
        return 0


class SalesTracker:
    def __init__(self): self.total_revenue = 0; self.total_cogs = 0

    def record_sale(self, cart):
        self.total_revenue += cart.total()
        for ci in cart.items:
            self.total_cogs += ci.menu_item.restock_price * ci.quantity

    def gross_profit(self):  return self.total_revenue - self.total_cogs
    def profit_margin(self): return 0 if self.total_revenue == 0 else (self.gross_profit() / self.total_revenue) * 100

    def health(self):
        m = self.profit_margin()
        if self.total_revenue == 0: return "NEUTRAL",       "No sales yet. Start selling!",                   C["gray_dark"], C["gray"]
        if m >= 30:                 return "✅ HEALTHY",    "Strong profit margin — keep it up!",              C["green"],     C["green_bg"]
        if m >= 10:                 return "🟡 STABLE",     "Stable — consider reducing costs.",               C["orange"],    C["orange_bg"]
        if m > 0:                   return "🟠 AT RISK",    "Thin margins — act soon!",                        "#E67E22",      "#FEF0E0"
        return "🔴 BANKRUPT RISK",  "DANGER: Losing money — immediate action needed!",  C["danger"],    C["danger_bg"]


def build_menu():
    return {
        1: ("Regular Meals", "🍗", [
            MenuItem("1pc Chickenjoy w/ Rice",   95,  20, 50,  20),
            MenuItem("2pc Chickenjoy w/ Rice",  180,  15, 95,  15),
            MenuItem("1pc Spicy Chickenjoy",    100,  15, 55,  15),
            MenuItem("1pc Burger Steak",         60,  20, 30,  20),
            MenuItem("2pc Burger Steak",        115,  15, 60,  15),
            MenuItem("Jolly Spaghetti Solo",     60,  25, 25,  25),
            MenuItem("Palabok Fiesta Solo",     120,  20, 60,  20),
            MenuItem("Yumburger Solo",           40,  30, 15,  30),
            MenuItem("Cheesy Yumburger",         65,  20, 30,  20),
            MenuItem("Tuna Pie (2pcs)",          90,  20, 40,  20),
        ]),
        2: ("Combo Meals", "🥤", [
            MenuItem("C1: Chickenjoy + Drink",           115, 15, 60,  15),
            MenuItem("C2: 2pc Chickenjoy + Drink",        200, 10, 100, 10),
            MenuItem("C3: Chickenjoy + Spag + Drink",     160, 10, 80,  10),
            MenuItem("C4: Chickenjoy + Palabok + Drink",  210, 10, 110, 10),
            MenuItem("J1: Burger Steak + Spag + Drink",   130, 12, 65,  12),
            MenuItem("S1: Spag + Yumburger + Drink",      110, 15, 55,  15),
            MenuItem("S2: Spag + Fries + Drink",          105, 15, 50,  15),
            MenuItem("B1: Yumburger + Fries + Drink",      95, 15, 45,  15),
            MenuItem("B2: Cheesy Yum + Fries + Drink",    120, 12, 60,  12),
            MenuItem("B3: Aloha Yum + Fries + Drink",     185, 10, 95,  10),
        ]),
        3: ("Family Meals", "👨‍👩‍👧", [
            MenuItem("6pc Chickenjoy Bucket",      450, 10, 240, 10),
            MenuItem("8pc Chickenjoy Bucket",      590,  8, 310,  8),
            MenuItem("6pc Spicy Bucket",           480,  8, 255,  8),
            MenuItem("Family Pan Spaghetti",       250, 10, 120, 10),
            MenuItem("Family Pan Palabok",         400,  8, 200,  8),
            MenuItem("Chicken + Spag Family Meal", 550,  8, 280,  8),
            MenuItem("Burger Steak Family Pan",    320,  8, 160,  8),
            MenuItem("Bucket of Fries",            150, 15,  70, 15),
            MenuItem("Peach Mango Pie 3-Pack",     130, 15,  60, 15),
            MenuItem("Tuna Pie 3-Pack",            135, 15,  60, 15),
        ]),
        4: ("Party Meals", "🎉", [
            MenuItem("Party Bundle A (12pc+2 Spag)",   1200, 5,  650, 5),
            MenuItem("Party Bundle B (18pc+20 Yum)",   2500, 3, 1300, 3),
            MenuItem("12pc Chickenjoy Bucket",          850, 5,  450, 5),
            MenuItem("15pc Chickenjoy Bucket",         1050, 5,  560, 5),
            MenuItem("Jolly Spaghetti Party Size",      650, 5,  320, 5),
            MenuItem("Palabok Fiesta Party Size",       850, 5,  440, 5),
            MenuItem("Burger Steak Party Tray (20pc)",  950, 5,  500, 5),
            MenuItem("Pie Party Pack (12pcs)",          500, 5,  240, 5),
            MenuItem("Sundae Party Set (10 cups)",      450, 5,  200, 5),
            MenuItem("Mixed Bucket (6 Reg/6 Spicy)",    880, 5,  460, 5),
        ]),
        5: ("Jolli-Saver Meals", "💰", [
            MenuItem("Budget Yumburger",            35, 30, 12, 30),
            MenuItem("Jr. Burger Steak",            55, 25, 25, 25),
            MenuItem("Jr. Jolly Spaghetti",         50, 25, 20, 25),
            MenuItem("Fries & Coke Float",          75, 20, 35, 20),
            MenuItem("Yumburger & Pineapple Juice", 70, 20, 30, 20),
            MenuItem("Jolli-Hotdog",                60, 20, 25, 20),
            MenuItem("Tuna Pie & Coffee",           80, 20, 35, 20),
            MenuItem("Steak & Peach Mango Pie",     99, 15, 45, 15),
            MenuItem("Rice & Extra Gravy Bowl",     30, 30, 10, 30),
            MenuItem("Iced Barako & Yumburger",     85, 15, 38, 15),
        ]),
    }


# ══════════════════════════════════════════════════
#  UI HELPERS
# ══════════════════════════════════════════════════
def clear_frame(frame):
    for w in frame.winfo_children():
        w.destroy()


def rounded_btn(parent, text, command, bg=C["red"], fg=C["white"],
                font=FONT_BOLD, padx=18, pady=8, relief="flat", cursor="hand2", **kw):
    btn = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                    font=font, padx=padx, pady=pady, relief=relief,
                    cursor=cursor, activebackground=C["red_dark"],
                    activeforeground=C["white"], bd=0, **kw)
    btn.bind("<Enter>", lambda e: btn.config(bg=C["red_dark"] if bg == C["red"] else bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def label_badge(parent, text, fg, bg, font=FONT_SMALL):
    f = tk.Frame(parent, bg=bg, pady=2, padx=6)
    tk.Label(f, text=text, fg=fg, bg=bg, font=font).pack()
    return f


def separator(parent, color=C["gray_dark"], height=1, pady=4):
    f = tk.Frame(parent, bg=color, height=height)
    f.pack(fill="x", pady=pady)


# ══════════════════════════════════════════════════
#  SCROLLABLE FRAME
# ══════════════════════════════════════════════════
class ScrollFrame(tk.Frame):
    def __init__(self, parent, bg=C["cream"], **kw):
        super().__init__(parent, bg=bg, **kw)
        canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.inner = tk.Frame(canvas, bg=bg)
        self.inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))


# ══════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════
class JolliBaeApp:
    def __init__(self, root):
        self.root    = root
        self.menu    = build_menu()
        self.tracker = SalesTracker()
        self.cart    = Cart()
        self.auth    = hashlib.sha256(b"admin1234").hexdigest()

        self._setup_root()
        self._build_skeleton()
        self.show_welcome()

    # ─── Root window ───────────────────────────────
    def _setup_root(self):
        self.root.title("🍗 Jolli-Bae Restaurant System")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=C["cream"])
        self.root.resizable(True, True)
        try:
            self.root.state("zoomed")
        except:
            pass

    # ─── Skeleton: topbar + body ────────────────────
    def _build_skeleton(self):
        # ── Top Bar ──
        self.topbar = tk.Frame(self.root, bg=C["header_bg"], height=60)
        self.topbar.pack(fill="x", side="top")
        self.topbar.pack_propagate(False)

        tk.Label(self.topbar, text="🍗  JOLLI-BAE", font=("Georgia", 20, "bold"),
                 bg=C["header_bg"], fg=C["yellow"]).pack(side="left", padx=20)
        tk.Label(self.topbar, text='"Your EX might be salty, but our chicken is always crispy!"',
                 font=("Helvetica", 9, "italic"), bg=C["header_bg"],
                 fg="white").pack(side="left", padx=4)

        self.topbar_right = tk.Frame(self.topbar, bg=C["header_bg"])
        self.topbar_right.pack(side="right", padx=16)

        # ── Body ──
        self.body = tk.Frame(self.root, bg=C["cream"])
        self.body.pack(fill="both", expand=True)

    def _clear_topbar_right(self):
        for w in self.topbar_right.winfo_children():
            w.destroy()

    def _clear_body(self):
        for w in self.body.winfo_children():
            w.destroy()

    # ═══════════════════════════════════════════════
    #  WELCOME SCREEN
    # ═══════════════════════════════════════════════
    def show_welcome(self):
        self._clear_topbar_right()
        self._clear_body()
        self.cart.clear()

        f = tk.Frame(self.body, bg=C["cream"])
        f.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(f, text="🍗", font=("Helvetica", 72), bg=C["cream"]).pack()
        tk.Label(f, text="JOLLI-BAE", font=("Georgia", 52, "bold"),
                 bg=C["cream"], fg=C["red"]).pack()
        tk.Label(f, text="The Tastiest Deal in Town", font=("Helvetica", 13, "italic"),
                 bg=C["cream"], fg=C["brown"]).pack(pady=(0, 40))

        btns = tk.Frame(f, bg=C["cream"])
        btns.pack()

        for text, cmd, bg, fg in [
            ("🧑  Customer",    self.show_customer,   C["red"],    C["white"]),
            ("🔐  Admin Staff", self.show_admin_auth, C["brown"],  C["yellow"]),
            ("👋  Exit",        self.root.destroy,    C["gray"],   C["dark"]),
        ]:
            b = tk.Button(btns, text=text, command=cmd, bg=bg, fg=fg,
                          font=("Georgia", 13, "bold"), padx=30, pady=14,
                          relief="flat", cursor="hand2", bd=0, width=16)
            b.pack(side="left", padx=10)

    # ═══════════════════════════════════════════════
    #  CUSTOMER SCREEN
    # ═══════════════════════════════════════════════
    def show_customer(self):
        self._clear_body()
        self._clear_topbar_right()

        # Cart button in topbar
        self.cart_label_var = tk.StringVar(value="🛒  Cart  (0)  ₱0")
        cart_btn = tk.Button(self.topbar_right, textvariable=self.cart_label_var,
                             bg=C["yellow"], fg=C["brown"], font=FONT_BOLD,
                             padx=14, pady=6, relief="flat", cursor="hand2", bd=0,
                             command=self.show_cart)
        cart_btn.pack(side="left", padx=(0, 8))

        back_btn = tk.Button(self.topbar_right, text="← Exit",
                             bg="white", fg=C["dark"], font=FONT_SMALL,
                             padx=10, pady=6, relief="flat", cursor="hand2", bd=0,
                             command=self.show_welcome)
        back_btn.pack(side="left")

        # Layout: sidebar + main
        sidebar = tk.Frame(self.body, bg=C["sidebar_bg"], width=200)
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="MENU", font=("Georgia", 11, "bold"),
                 bg=C["sidebar_bg"], fg=C["yellow"]).pack(pady=(20, 6))

        tk.Frame(sidebar, bg=C["yellow"], height=2).pack(fill="x", padx=16, pady=(0, 10))

        self.main_area = tk.Frame(self.body, bg=C["cream"])
        self.main_area.pack(fill="both", expand=True, side="left")

        # Category buttons
        for cat_id, (cat_name, icon, _) in self.menu.items():
            btn = tk.Button(sidebar, text=f"  {icon}  {cat_name}",
                            font=("Helvetica", 10, "bold"), bg=C["sidebar_bg"],
                            fg="white", anchor="w", relief="flat", cursor="hand2",
                            padx=12, pady=10, bd=0,
                            command=lambda cid=cat_id: self._load_category(cid))
            btn.pack(fill="x", pady=1)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#5C1E08", fg=C["yellow"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=C["sidebar_bg"], fg="white"))

        self._load_category(1)

    def _load_category(self, cat_id):
        clear_frame(self.main_area)
        cat_name, icon, items = self.menu[cat_id]

        # Header
        hdr = tk.Frame(self.main_area, bg=C["red"], pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"{icon}  {cat_name}", font=FONT_TITLE,
                 bg=C["red"], fg="white").pack(padx=24, side="left")

        # Scrollable grid
        sf = ScrollFrame(self.main_area, bg=C["cream"])
        sf.pack(fill="both", expand=True, padx=16, pady=16)

        COLS = 3
        for idx, item in enumerate(items):
            row, col = divmod(idx, COLS)
            sf.inner.columnconfigure(col, weight=1, minsize=260)
            self._menu_card(sf.inner, item).grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def _menu_card(self, parent, item):
        card = tk.Frame(parent, bg=C["white"], relief="flat", bd=0,
                        highlightthickness=2, highlightbackground=C["gray_dark"])
        oos = not item.is_available()

        # Colour bar on top
        tk.Frame(card, bg=C["red"] if not oos else C["gray_dark"], height=5).pack(fill="x")

        body = tk.Frame(card, bg=C["white"], padx=16, pady=14)
        body.pack(fill="both", expand=True)

        tk.Label(body, text=item.name, font=FONT_BOLD,
                 bg=C["white"], fg=C["dark"], wraplength=210,
                 justify="left", anchor="w").pack(anchor="w")

        tk.Label(body, text=f"₱{item.price}", font=("Georgia", 18, "bold"),
                 bg=C["white"], fg=C["red"]).pack(anchor="w", pady=(4, 8))

        # Stock badge
        txt, fg, bg = item.status_text()
        badge = tk.Frame(body, bg=bg, padx=8, pady=3)
        badge.pack(anchor="w", pady=(0, 10))
        tk.Label(badge, text=txt, font=("Helvetica", 9, "bold"), bg=bg, fg=fg).pack()

        if not oos:
            btn = tk.Button(body, text="+ Add to Cart", command=lambda i=item: self._add_to_cart_dialog(i),
                            bg=C["red"], fg="white", font=FONT_BOLD, relief="flat",
                            cursor="hand2", pady=7, bd=0)
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e: btn.config(bg=C["red_dark"]))
            btn.bind("<Leave>", lambda e: btn.config(bg=C["red"]))
        else:
            tk.Label(body, text="Unavailable", font=FONT_SMALL,
                     bg=C["white"], fg="#bbb").pack()

        # hover highlight
        def on_enter(e):
            if not oos:
                card.config(highlightbackground=C["red"])
        def on_leave(e):
            card.config(highlightbackground=C["gray_dark"])
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        return card

    def _add_to_cart_dialog(self, item):
        max_add = item.stock - self.cart.qty_in_cart(item.name)
        if max_add <= 0:
            messagebox.showinfo("Cart Full", f"You already have the maximum stock of\n'{item.name}' in your cart.")
            return

        dlg = tk.Toplevel(self.root)
        dlg.title("Add to Cart")
        dlg.resizable(False, False)
        dlg.configure(bg=C["white"])
        dlg.grab_set()
        w, h = 380, 300
        dlg.geometry(f"{w}x{h}+{(self.root.winfo_width()-w)//2+self.root.winfo_x()}+"
                     f"{(self.root.winfo_height()-h)//2+self.root.winfo_y()}")

        tk.Frame(dlg, bg=C["red"], height=8).pack(fill="x")
        inner = tk.Frame(dlg, bg=C["white"], padx=28, pady=20)
        inner.pack(fill="both", expand=True)

        tk.Label(inner, text="🍗  Add to Cart", font=FONT_HEADER,
                 bg=C["white"], fg=C["red"]).pack(anchor="w")
        tk.Label(inner, text=item.name, font=FONT_SUB, bg=C["white"],
                 fg=C["dark"], wraplength=310, justify="left").pack(anchor="w", pady=(4, 2))
        tk.Label(inner, text=f"₱{item.price} each  •  up to {max_add} available",
                 font=FONT_SMALL, bg=C["white"], fg="#888").pack(anchor="w", pady=(0, 16))

        qty_var = tk.IntVar(value=1)
        subtotal_var = tk.StringVar(value=f"Subtotal: ₱{item.price}")

        def update_sub(*_):
            subtotal_var.set(f"Subtotal: ₱{item.price * qty_var.get()}")

        qty_var.trace_add("write", update_sub)

        ctrl = tk.Frame(inner, bg=C["white"])
        ctrl.pack()

        def dec():
            if qty_var.get() > 1: qty_var.set(qty_var.get() - 1)
        def inc():
            if qty_var.get() < max_add: qty_var.set(qty_var.get() + 1)

        tk.Button(ctrl, text="−", command=dec, bg=C["red"], fg="white",
                  font=("Helvetica", 16, "bold"), width=3, relief="flat",
                  cursor="hand2", bd=0).pack(side="left", padx=6)
        tk.Label(ctrl, textvariable=qty_var, font=("Georgia", 22, "bold"),
                 bg=C["white"], width=4, fg=C["dark"]).pack(side="left")
        tk.Button(ctrl, text="+", command=inc, bg=C["red"], fg="white",
                  font=("Helvetica", 16, "bold"), width=3, relief="flat",
                  cursor="hand2", bd=0).pack(side="left", padx=6)

        tk.Label(inner, textvariable=subtotal_var, font=FONT_BOLD,
                 bg=C["white"], fg=C["brown"]).pack(pady=12)

        btn_row = tk.Frame(inner, bg=C["white"])
        btn_row.pack(fill="x")

        def confirm():
            self.cart.add(item, qty_var.get())
            self._refresh_cart_label()
            dlg.destroy()

        tk.Button(btn_row, text="Cancel", command=dlg.destroy,
                  bg=C["gray"], fg=C["dark"], font=FONT_BOLD, relief="flat",
                  cursor="hand2", padx=16, pady=8, bd=0).pack(side="left", expand=True, fill="x", padx=(0, 6))
        tk.Button(btn_row, text="Add to Cart ✓", command=confirm,
                  bg=C["red"], fg="white", font=FONT_BOLD, relief="flat",
                  cursor="hand2", padx=16, pady=8, bd=0).pack(side="left", expand=True, fill="x")

    def _refresh_cart_label(self):
        count = sum(ci.quantity for ci in self.cart.items)
        total = self.cart.total()
        self.cart_label_var.set(f"🛒  Cart  ({count})  ₱{total:,}")

    # ═══════════════════════════════════════════════
    #  CART WINDOW
    # ═══════════════════════════════════════════════
    def show_cart(self):
        win = tk.Toplevel(self.root)
        win.title("Shopping Cart")
        win.configure(bg=C["white"])
        win.grab_set()
        w, h = 520, 560
        win.geometry(f"{w}x{h}+{(self.root.winfo_width()-w)//2+self.root.winfo_x()}+"
                     f"{(self.root.winfo_height()-h)//2+self.root.winfo_y()}")
        win.resizable(False, False)

        # Header
        hdr = tk.Frame(win, bg=C["red"], pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🛒  Shopping Cart", font=FONT_HEADER,
                 bg=C["red"], fg=C["yellow"]).pack(padx=20, side="left")

        if self.cart.is_empty():
            tk.Label(win, text="🛒\n\nYour cart is empty!", font=FONT_HEADER,
                     bg=C["white"], fg="#bbb").pack(expand=True)
            tk.Button(win, text="Continue Shopping", command=win.destroy,
                      bg=C["red"], fg="white", font=FONT_BOLD, relief="flat",
                      cursor="hand2", pady=10, bd=0).pack(padx=40, pady=20, fill="x")
            return

        # Items list
        sf = ScrollFrame(win, bg=C["white"])
        sf.pack(fill="both", expand=True, padx=0, pady=0)

        def refresh_cart_ui():
            clear_frame(sf.inner)
            for idx, ci in enumerate(self.cart.items):
                row = tk.Frame(sf.inner, bg=C["white"], padx=16, pady=10)
                row.pack(fill="x")

                tk.Label(row, text=ci.menu_item.name, font=FONT_BOLD,
                         bg=C["white"], fg=C["dark"], anchor="w",
                         wraplength=240).grid(row=0, column=0, sticky="w")
                tk.Label(row, text=f"₱{ci.menu_item.price} × {ci.quantity} = ₱{ci.subtotal():,}",
                         font=FONT_SMALL, bg=C["white"], fg="#888").grid(row=1, column=0, sticky="w")

                ctrl = tk.Frame(row, bg=C["white"])
                ctrl.grid(row=0, column=1, rowspan=2, padx=(10, 0), sticky="e")
                row.columnconfigure(0, weight=1)

                def make_dec(i=idx):
                    def dec():
                        if self.cart.items[i].quantity > 1:
                            self.cart.items[i].quantity -= 1
                        refresh_cart_ui()
                        self._refresh_cart_label()
                    return dec

                def make_inc(i=idx):
                    def inc():
                        ci_ = self.cart.items[i]
                        if ci_.quantity < ci_.menu_item.stock:
                            ci_.quantity += 1
                        refresh_cart_ui()
                        self._refresh_cart_label()
                    return inc

                def make_remove(i=idx):
                    def rem():
                        self.cart.remove(i)
                        self._refresh_cart_label()
                        if self.cart.is_empty():
                            win.destroy()
                        else:
                            refresh_cart_ui()
                            update_total()
                    return rem

                tk.Button(ctrl, text="−", command=make_dec(), bg=C["gray"],
                          font=FONT_BOLD, relief="flat", cursor="hand2", bd=0,
                          width=3).pack(side="left")
                tk.Label(ctrl, text=str(ci.quantity), font=FONT_BOLD,
                         bg=C["white"], width=3).pack(side="left")
                tk.Button(ctrl, text="+", command=make_inc(), bg=C["gray"],
                          font=FONT_BOLD, relief="flat", cursor="hand2", bd=0,
                          width=3).pack(side="left")
                tk.Button(ctrl, text="🗑", command=make_remove(), bg=C["white"],
                          fg=C["danger"], font=FONT_BOLD, relief="flat",
                          cursor="hand2", bd=0).pack(side="left", padx=(6, 0))

                tk.Frame(sf.inner, bg=C["gray"], height=1).pack(fill="x", padx=16)
            update_total()

        total_var = tk.StringVar()

        def update_total():
            total_var.set(f"Total: ₱{self.cart.total():,}")

        # Footer
        footer = tk.Frame(win, bg=C["white"], pady=14, padx=20)
        footer.pack(fill="x", side="bottom")
        tk.Frame(footer, bg=C["gray_dark"], height=2).pack(fill="x", pady=(0, 12))
        tk.Label(footer, textvariable=total_var, font=("Georgia", 16, "bold"),
                 bg=C["white"], fg=C["dark"]).pack(side="left")

        def do_checkout():
            if messagebox.askyesno("Confirm Checkout",
                                   f"Confirm order?\nTotal: ₱{self.cart.total():,}"):
                items_snap = [(ci.menu_item.name, ci.menu_item.price, ci.quantity)
                              for ci in self.cart.items]
                total_snap = self.cart.total()
                self.tracker.record_sale(self.cart)
                for ci in self.cart.items:
                    ci.menu_item.deduct(ci.quantity)
                self.cart.clear()
                self._refresh_cart_label()
                win.destroy()
                self._show_receipt(items_snap, total_snap)

        tk.Button(footer, text="CHECKOUT  →", command=do_checkout,
                  bg=C["red"], fg="white", font=("Georgia", 13, "bold"),
                  relief="flat", cursor="hand2", pady=10, padx=20, bd=0).pack(side="right")

        refresh_cart_ui()

    def _show_receipt(self, items, total):
        win = tk.Toplevel(self.root)
        win.title("Receipt")
        win.configure(bg=C["white"])
        win.grab_set()
        w, h = 460, 580
        win.geometry(f"{w}x{h}+{(self.root.winfo_width()-w)//2+self.root.winfo_x()}+"
                     f"{(self.root.winfo_height()-h)//2+self.root.winfo_y()}")
        win.resizable(False, True)

        # Red accent bar at top
        tk.Frame(win, bg=C["red"], height=8).pack(fill="x")

        # Header (fixed, never scrolls)
        header = tk.Frame(win, bg=C["white"], padx=36, pady=16)
        header.pack(fill="x")

        tk.Label(header, text="🍗  JOLLI-BAE", font=("Georgia", 22, "bold"),
                 bg=C["white"], fg=C["red"]).pack()
        tk.Label(header, text="(02) 8123-4567  •  jolli-bae@email.com",
                 font=FONT_SMALL, bg=C["white"], fg="#aaa").pack()

        tk.Frame(header, bg=C["gray_dark"], height=1).pack(fill="x", pady=(10, 0))
        tk.Label(header, text="ORDER RECEIPT", font=("Helvetica", 10, "bold"),
                 bg=C["white"], fg="#888").pack(pady=4)
        tk.Frame(header, bg=C["gray_dark"], height=1).pack(fill="x", pady=(0, 4))

        # Scrollable items area (expands to fill available space)
        sf = ScrollFrame(win, bg=C["white"])
        sf.pack(fill="both", expand=True, padx=36)

        for name, price, qty in items:
            row = tk.Frame(sf.inner, bg=C["white"])
            row.pack(fill="x", pady=3)
            tk.Label(row, text=name, font=FONT_BOLD, bg=C["white"],
                     fg=C["dark"], anchor="w", wraplength=240,
                     justify="left").pack(side="left")
            tk.Label(row, text=f"×{qty}  ₱{price*qty:,}", font=FONT_BOLD,
                     bg=C["white"], fg=C["red"]).pack(side="right")

        # Footer (fixed at bottom — always visible)
        footer = tk.Frame(win, bg=C["white"], padx=36, pady=16)
        footer.pack(fill="x", side="bottom")

        tk.Frame(footer, bg=C["dark"], height=2).pack(fill="x", pady=(0, 10))
        total_row = tk.Frame(footer, bg=C["white"])
        total_row.pack(fill="x")
        tk.Label(total_row, text="TOTAL DUE", font=("Georgia", 13, "bold"),
                 bg=C["white"]).pack(side="left")
        tk.Label(total_row, text=f"₱{total:,}", font=("Georgia", 20, "bold"),
                 bg=C["white"], fg=C["red"]).pack(side="right")

        tk.Frame(footer, bg=C["gray_dark"], height=1).pack(fill="x", pady=10)
        tk.Label(footer, text="🎉  Thank you! Enjoy your meal!", font=FONT_BOLD,
                 bg=C["white"], fg=C["brown"]).pack(pady=(0, 10))

        btn_row = tk.Frame(footer, bg=C["white"])
        btn_row.pack(fill="x")

        tk.Button(btn_row, text="Order More", command=win.destroy,
                  bg=C["gray"], fg=C["dark"], font=FONT_BOLD, relief="flat",
                  cursor="hand2", pady=10, bd=0).pack(side="left", expand=True, fill="x", padx=(0, 8))
        tk.Button(btn_row, text="Home  🏠", command=lambda: [win.destroy(), self.show_welcome()],
                  bg=C["brown"], fg=C["yellow"], font=FONT_BOLD, relief="flat",
                  cursor="hand2", pady=10, bd=0).pack(side="left", expand=True, fill="x")

    # ═══════════════════════════════════════════════
    #  ADMIN AUTH
    # ═══════════════════════════════════════════════
    def show_admin_auth(self):
        self._clear_body()
        self._clear_topbar_right()

        f = tk.Frame(self.body, bg=C["cream"])
        f.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(f, text="🔒", font=("Helvetica", 52), bg=C["cream"]).pack()
        tk.Label(f, text="ADMIN ACCESS", font=("Georgia", 24, "bold"),
                 bg=C["cream"], fg=C["brown"]).pack(pady=(0, 4))
        tk.Label(f, text="Enter your passcode to continue",
                 font=FONT_BODY, bg=C["cream"], fg="#888").pack(pady=(0, 24))

        self.auth_attempts = 0
        self.auth_error_var = tk.StringVar()

        tk.Label(f, textvariable=self.auth_error_var, font=FONT_SMALL,
                 bg=C["cream"], fg=C["danger"]).pack()

        pw_var = tk.StringVar()
        entry = tk.Entry(f, textvariable=pw_var, show="●", font=("Georgia", 14),
                         relief="solid", bd=1, width=20, justify="center")
        entry.pack(ipady=8, pady=8)
        entry.focus_set()

        def attempt(e=None):
            pw = pw_var.get()
            hsh = hashlib.sha256(pw.encode()).hexdigest()
            if hsh == self.auth:
                self.show_admin()
            else:
                self.auth_attempts += 1
                pw_var.set("")
                rem = 3 - self.auth_attempts
                if rem > 0:
                    self.auth_error_var.set(f"Incorrect passcode. {rem} attempt(s) remaining.")
                else:
                    self.auth_error_var.set("Too many failed attempts.")
                    self.root.after(1500, self.show_welcome)

        entry.bind("<Return>", attempt)
        tk.Button(f, text="UNLOCK  →", command=attempt,
                  bg=C["brown"], fg=C["yellow"], font=("Georgia", 13, "bold"),
                  relief="flat", cursor="hand2", pady=10, padx=28, bd=0).pack(pady=(4, 16))
        tk.Button(f, text="← Back to Role Selection", command=self.show_welcome,
                  bg=C["cream"], fg="#aaa", font=FONT_SMALL, relief="flat",
                  cursor="hand2", bd=0).pack()

    # ═══════════════════════════════════════════════
    #  ADMIN PANEL
    # ═══════════════════════════════════════════════
    def show_admin(self):
        self._clear_body()
        self._clear_topbar_right()

        tk.Button(self.topbar_right, text="← Exit Admin", command=self.show_welcome,
                  bg="white", fg=C["dark"], font=FONT_SMALL,
                  padx=10, pady=6, relief="flat", cursor="hand2", bd=0).pack()

        # Tabs row
        top = tk.Frame(self.body, bg=C["white"], pady=0)
        top.pack(fill="x")

        tk.Label(top, text="⚙  Admin Panel", font=("Georgia", 18, "bold"),
                 bg=C["white"], fg=C["brown"], padx=24, pady=16).pack(side="left")

        tab_bar = tk.Frame(top, bg=C["white"])
        tab_bar.pack(side="right", padx=16, pady=10)

        content = tk.Frame(self.body, bg=C["cream"])
        content.pack(fill="both", expand=True)

        self._active_tab = tk.StringVar(value="stock")

        tabs = [
            ("📦  Stock",     "stock"),
            ("📈  Analytics", "analytics"),
            ("🔑  Passcode",  "passcode"),
        ]
        tab_btns = {}

        def switch(key):
            self._active_tab.set(key)
            for k, b in tab_btns.items():
                if k == key:
                    b.config(bg=C["red"], fg="white")
                else:
                    b.config(bg=C["gray"], fg=C["dark"])
            clear_frame(content)
            if key == "stock":     self._admin_stock(content)
            elif key == "analytics": self._admin_analytics(content)
            elif key == "passcode":  self._admin_passcode(content)

        for label, key in tabs:
            b = tk.Button(tab_bar, text=label, command=lambda k=key: switch(k),
                          bg=C["gray"], fg=C["dark"], font=FONT_BOLD,
                          relief="flat", cursor="hand2", padx=16, pady=8, bd=0)
            b.pack(side="left", padx=4)
            tab_btns[key] = b

        switch("stock")

    # ── Admin: Stock ────────────────────────────────
    def _admin_stock(self, parent):
        sf = ScrollFrame(parent, bg=C["cream"])
        sf.pack(fill="both", expand=True, padx=20, pady=16)

        # (header text, grid column weight, min pixel width)
        col_defs = [
            ("#",        0, 30),
            ("Item",     3, 150),
            ("Category", 2, 110),
            ("Price",    1, 55),
            ("Stock",    1, 45),
            ("Status",   2, 100),
            ("Action",   1, 80),
        ]

        # Configure sf.inner columns so it stretches to fill width
        for col_i, (_, weight, min_w) in enumerate(col_defs):
            sf.inner.columnconfigure(col_i, weight=weight, minsize=min_w)

        # Header row
        for col_i, (col_name, _, _) in enumerate(col_defs):
            tk.Label(sf.inner, text=col_name, font=("Helvetica", 10, "bold"),
                     bg=C["brown"], fg="white", pady=8, padx=6,
                     anchor="w").grid(row=0, column=col_i, sticky="ew", pady=(0, 2))

        num = 1
        for cat_id, (cat_name, icon, items) in self.menu.items():
            for item in items:
                grid_row = num  # row 0 is header
                row_bg = C["white"] if num % 2 == 0 else C["cream"]
                txt, fg, bg = item.status_text()

                tk.Label(sf.inner, text=str(num), font=FONT_SMALL, bg=row_bg,
                         fg=C["dark"], anchor="w", padx=6, pady=6).grid(
                             row=grid_row, column=0, sticky="ew")
                tk.Label(sf.inner, text=item.name, font=FONT_SMALL, bg=row_bg,
                         fg=C["dark"], anchor="w", padx=6, pady=6,
                         wraplength=180).grid(row=grid_row, column=1, sticky="ew")
                tk.Label(sf.inner, text=f"{icon} {cat_name}", font=FONT_SMALL, bg=row_bg,
                         fg=C["dark"], anchor="w", padx=6, pady=6).grid(
                             row=grid_row, column=2, sticky="ew")
                tk.Label(sf.inner, text=f"₱{item.price}", font=FONT_SMALL, bg=row_bg,
                         fg=C["dark"], anchor="w", padx=6, pady=6).grid(
                             row=grid_row, column=3, sticky="ew")
                tk.Label(sf.inner, text=str(item.stock), font=FONT_SMALL, bg=row_bg,
                         fg=C["dark"], anchor="w", padx=6, pady=6).grid(
                             row=grid_row, column=4, sticky="ew")

                badge_cell = tk.Frame(sf.inner, bg=row_bg, padx=4, pady=4)
                badge_cell.grid(row=grid_row, column=5, sticky="ew")
                badge = tk.Frame(badge_cell, bg=bg, padx=6, pady=2)
                badge.pack(anchor="w")
                tk.Label(badge, text=txt, font=("Helvetica", 9, "bold"),
                         bg=bg, fg=fg).pack()

                tk.Button(sf.inner, text="Restock", font=("Helvetica", 9, "bold"),
                          bg=C["yellow"], fg=C["brown"], relief="flat", cursor="hand2",
                          bd=0, padx=8, pady=4,
                          command=lambda i=item: self._restock_dialog(i, parent)).grid(
                              row=grid_row, column=6, sticky="ew", padx=8, pady=2)
                num += 1

    def _restock_dialog(self, item, content_frame):
        dlg = tk.Toplevel(self.root)
        dlg.title("Restock Item")
        dlg.resizable(False, False)
        dlg.configure(bg=C["white"])
        dlg.grab_set()
        w, h = 400, 420
        dlg.geometry(f"{w}x{h}+{(self.root.winfo_width()-w)//2+self.root.winfo_x()}+"
                     f"{(self.root.winfo_height()-h)//2+self.root.winfo_y()}")
        dlg.resizable(False, True)

        tk.Frame(dlg, bg=C["yellow"], height=8).pack(fill="x")
        body = tk.Frame(dlg, bg=C["white"], padx=28, pady=20)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="📦  Restock", font=FONT_HEADER,
                 bg=C["white"], fg=C["brown"]).pack(anchor="w")
        tk.Label(body, text=item.name, font=FONT_BOLD, bg=C["white"],
                 wraplength=310, justify="left").pack(anchor="w", pady=(4, 12))

        info = tk.Frame(body, bg=C["gray"], padx=12, pady=10)
        info.pack(fill="x", pady=(0, 14))
        for lbl, val in [("Current Stock", item.stock),
                          ("Default Qty",   item.restock_qty),
                          ("Cost/Unit",     f"₱{item.restock_price}")]:
            r = tk.Frame(info, bg=C["gray"])
            r.pack(fill="x", pady=2)
            tk.Label(r, text=lbl, font=FONT_SMALL, bg=C["gray"], fg="#888").pack(side="left")
            tk.Label(r, text=str(val), font=FONT_BOLD, bg=C["gray"], fg=C["dark"]).pack(side="right")

        qty_var = tk.IntVar(value=item.restock_qty)
        cost_var = tk.StringVar(value=f"Total cost: ₱{item.restock_cost()}")

        def update_cost(*_):
            try: cost_var.set(f"Total cost: ₱{qty_var.get() * item.restock_price:,}")
            except: pass

        qty_var.trace_add("write", update_cost)

        tk.Label(body, text="Quantity to restock:", font=FONT_SMALL,
                 bg=C["white"], fg="#888").pack(anchor="w")
        tk.Entry(body, textvariable=qty_var, font=("Georgia", 14),
                 relief="solid", bd=1, justify="center",
                 width=12).pack(pady=6, ipady=6)
        tk.Label(body, textvariable=cost_var, font=FONT_BOLD,
                 bg=C["white"], fg=C["red"]).pack()

        def confirm():
            try:
                qty = int(qty_var.get())
                if qty <= 0: raise ValueError
            except:
                messagebox.showerror("Invalid", "Enter a positive quantity."); return
            item.restock(qty)
            dlg.destroy()
            # Refresh stock view by clearing the content frame and rebuilding
            clear_frame(content_frame)
            self._admin_stock(content_frame)

        btn_row = tk.Frame(body, bg=C["white"])
        btn_row.pack(fill="x", pady=(14, 0))
        tk.Button(btn_row, text="Cancel", command=dlg.destroy,
                  bg=C["gray"], fg=C["dark"], font=FONT_BOLD, relief="flat",
                  cursor="hand2", pady=8, bd=0).pack(side="left", expand=True, fill="x", padx=(0, 6))
        tk.Button(btn_row, text="Confirm Restock ✓", command=confirm,
                  bg=C["brown"], fg=C["yellow"], font=FONT_BOLD, relief="flat",
                  cursor="hand2", pady=8, bd=0).pack(side="left", expand=True, fill="x")

    # ── Admin: Analytics ────────────────────────────
    def _admin_analytics(self, parent):
        sf = ScrollFrame(parent, bg=C["cream"])
        sf.pack(fill="both", expand=True, padx=20, pady=16)
        inner = sf.inner

        # Health banner
        hl, hm, hfg, hbg = self.tracker.health()
        banner = tk.Frame(inner, bg=hbg, padx=20, pady=14,
                          highlightthickness=2, highlightbackground=hfg)
        banner.pack(fill="x", pady=(0, 16))
        tk.Label(banner, text=hl, font=("Georgia", 15, "bold"),
                 bg=hbg, fg=hfg).pack(side="left")
        tk.Label(banner, text=f"  {hm}", font=FONT_BODY,
                 bg=hbg, fg=hfg).pack(side="left")

        # Stat cards
        stats_row = tk.Frame(inner, bg=C["cream"])
        stats_row.pack(fill="x", pady=(0, 16))

        r = self.tracker.total_revenue
        cogs = self.tracker.total_cogs
        gp = self.tracker.gross_profit()
        pm = self.tracker.profit_margin()

        for label, value, accent in [
            ("Total Revenue",  f"₱{r:,.2f}",   C["red"]),
            ("Est. COGS",      f"₱{cogs:,.2f}", C["orange"]),
            ("Gross Profit",   f"₱{gp:,.2f}",   C["green"]),
            ("Profit Margin",  f"{pm:.1f}%",     C["brown"]),
        ]:
            card = tk.Frame(stats_row, bg=C["white"], padx=18, pady=16,
                            highlightthickness=3, highlightbackground=accent)
            card.pack(side="left", expand=True, fill="both", padx=6)
            tk.Label(card, text=label, font=("Helvetica", 9, "bold"),
                     bg=C["white"], fg="#888").pack(anchor="w")
            tk.Label(card, text=value, font=("Georgia", 18, "bold"),
                     bg=C["white"], fg=C["dark"]).pack(anchor="w")

        # Sales rankings
        all_items = [i for _, (_, _, items) in self.menu.items() for i in items]
        ranked = sorted(all_items, key=lambda x: x.sold, reverse=True)
        top_sold = ranked[0].sold if ranked else 1

        tk.Label(inner, text="🏆  Sales Rankings", font=FONT_HEADER,
                 bg=C["cream"], fg=C["brown"]).pack(anchor="w", pady=(8, 8))

        rank_card = tk.Frame(inner, bg=C["white"])
        rank_card.pack(fill="x")

        for i, item in enumerate(ranked):
            row = tk.Frame(rank_card, bg=C["white"], padx=14, pady=8)
            row.pack(fill="x")
            tk.Label(row, text=f"#{i+1}", font=("Georgia", 14, "bold"),
                     bg=C["white"], fg=C["red"], width=4).pack(side="left")
            tk.Label(row, text=item.name, font=FONT_BOLD,
                     bg=C["white"], fg=C["dark"]).pack(side="left")

            bar_pct = int((item.sold / max(top_sold, 1)) * 150)
            bar_frame = tk.Frame(row, bg=C["gray"], height=8, width=150)
            bar_frame.pack(side="right", padx=(0, 12))
            bar_frame.pack_propagate(False)
            tk.Frame(bar_frame, bg=C["red"], height=8, width=bar_pct).pack(side="left")

            tk.Label(row, text=f"{item.sold} sold", font=FONT_SMALL,
                     bg=C["white"], fg="#888", width=8).pack(side="right")

            if i < len(ranked) - 1:
                tk.Frame(rank_card, bg=C["gray"], height=1).pack(fill="x", padx=14)

    # ── Admin: Passcode ─────────────────────────────
    def _admin_passcode(self, parent):
        f = tk.Frame(parent, bg=C["cream"])
        f.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(f, bg=C["white"], padx=40, pady=36,
                        highlightthickness=2, highlightbackground=C["gray_dark"])
        card.pack()

        tk.Label(card, text="🔑  Change Passcode", font=("Georgia", 18, "bold"),
                 bg=C["white"], fg=C["brown"]).pack(pady=(0, 20))

        err_var = tk.StringVar()
        tk.Label(card, textvariable=err_var, font=FONT_SMALL,
                 bg=C["white"], fg=C["danger"]).pack()

        fields = {}
        for label, key in [("Current Passcode", "cur"), ("New Passcode", "new"), ("Confirm New", "con")]:
            tk.Label(card, text=label, font=FONT_SMALL, bg=C["white"], fg="#888",
                     anchor="w").pack(fill="x")
            e = tk.Entry(card, show="●", font=("Helvetica", 12),
                         relief="solid", bd=1, justify="center")
            e.pack(fill="x", ipady=7, pady=(2, 10))
            fields[key] = e

        def save():
            cur = fields["cur"].get()
            new = fields["new"].get()
            con = fields["con"].get()
            err_var.set("")
            if hashlib.sha256(cur.encode()).hexdigest() != self.auth:
                err_var.set("Current passcode is incorrect."); return
            if len(new) < 4:
                err_var.set("New passcode must be at least 4 characters."); return
            if new != con:
                err_var.set("Passcodes do not match."); return
            self.auth = hashlib.sha256(new.encode()).hexdigest()
            for e in fields.values(): e.delete(0, "end")
            messagebox.showinfo("Success", "Passcode changed successfully!")

        tk.Button(card, text="Save Passcode  ✓", command=save,
                  bg=C["brown"], fg=C["yellow"], font=("Georgia", 13, "bold"),
                  relief="flat", cursor="hand2", pady=10, bd=0).pack(fill="x", pady=(8, 0))


# ══════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app  = JolliBaeApp(root)
    root.mainloop()
