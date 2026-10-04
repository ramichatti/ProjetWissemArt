"""
WissemArt Achat - Application Professionnelle de Gestion d'Achats
UI/UX Design Premium - Interface Responsive - Performance Optimale
"""

import os, csv, tkinter as tk
from tkinter import ttk, messagebox, Toplevel, font as tkfont
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import sys, math, time, webbrowser

# ── Fichiers de donnees ──
BASE_DIR = r"C:\Users\ramic\Desktop\WissemProject\Data"
ENTETE_FILE = os.path.join(BASE_DIR, "EnteteAchat.csv")
LIGNE_FILE = os.path.join(BASE_DIR, "LigneAchat.csv")

ENTETE_HEADERS = ["num_facture", "date_achat", "nom_fournisseur",
                  "matricule_fiscal", "adresse_fournisseur", "mode_paiement", "total_achat"]
LIGNE_HEADERS = ["num_facture", "nom_produit", "reference", "categorie", "design",
                 "quantite", "prix_unitaire", "montant_ligne"]
MODES_PAIEMENT = ["Especes", "Cheque", "Virement", "Carte Bancaire"]

# ── Palette de couleurs professionnelle ──
C = {
    'primary':       '#1565C0',
    'primary_dark':  '#0D47A1',
    'primary_light': '#1E88E5',
    'primary_bg':    '#E3F2FD',
    'primary_grad':  '#0D47A1',
    'white':         '#FFFFFF',
    'bg':            '#F0F2F5',
    'card':          '#FFFFFF',
    'text':          '#1A1A2E',
    'text_sec':      '#546E7A',
    'text_hint':     '#90A4AE',
    'border':        '#E0E0E0',
    'divider':       '#ECEFF1',
    'success':       '#2E7D32',
    'success_bg':    '#E8F5E9',
    'error':         '#C62828',
    'error_bg':      '#FFEBEE',
    'warning':       '#F57F17',
    'warning_bg':    '#FFF8E1',

    'shadow':        '#00000020',
    'overlay':       '#0D1B3ECC',
}

# ── Utilitaires ──
def init_csv(path, headers):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            csv.writer(f, delimiter=';').writerow(headers)

def read_csv(path):
    if not os.path.exists(path): return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=';'))

def append_csv(path, headers, row):
    with open(path, "a", newline="", encoding="utf-8-sig") as f:
        csv.DictWriter(f, fieldnames=headers, delimiter=';').writerow(row)

def write_csv(path, headers, rows):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=headers, delimiter=';')
        w.writeheader(); w.writerows(rows)

def dec(v):
    try: return Decimal(str(v).strip().replace(",", "."))
    except: raise ValueError(f"Valeur invalide: {v}")

def fmt_money(v):
    return f"{Decimal(v) if not isinstance(v, Decimal) else v:.3f}"

def fmt_date_iso(d):
    try: return datetime.strptime(d.strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
    except: return d.strip()

def fmt_date_display(d):
    try: return datetime.strptime(d.strip(), '%Y-%m-%d').strftime('%d/%m/%Y')
    except: return d.strip()

def today():
    return date.today().strftime('%d/%m/%Y')

def next_facture():
    entetes = read_csv(ENTETE_FILE)
    if not entetes: return "FAC1"
    m = 0
    for e in entetes:
        n = str(e.get('num_facture','')).strip()
        if n.startswith('FAC'):
            try: m = max(m, int(n.replace('FAC','')))
            except: pass
        else:
            try: m = max(m, int(n))
            except: pass
    return f"FAC{m+1}"

def next_ref():
    lignes = read_csv(LIGNE_FILE)
    if not lignes: return "REF1"
    m = 0
    for l in lignes:
        r = l.get('reference','').strip()
        if r.startswith('REF'):
            try: m = max(m, int(r.replace('REF','')))
            except: pass
    return f"REF{m+1}"

def next_mat():
    entetes = read_csv(ENTETE_FILE)
    if not entetes: return "MF1"
    m = 0
    for e in entetes:
        n = str(e.get('matricule_fiscal','')).strip()
        if n.startswith('MF'):
            try: m = max(m, int(n.replace('MF','')))
            except: pass
    return f"MF{m+1}"

def get_products():
    lignes = read_csv(LIGNE_FILE)
    prods = {}
    for l in lignes:
        n, r, c = l.get('nom_produit','').strip(), l.get('reference','').strip(), l.get('categorie','').strip()
        if n and f"{n}|{r}" not in prods:
            prods[f"{n}|{r}"] = {'nom': n, 'ref': r, 'cat': c}
    return list(prods.values())

def get_product_names():
    return sorted(set(p['nom'] for p in get_products()))

def get_fournisseurs():
    entetes = read_csv(ENTETE_FILE)
    f = {}
    for e in entetes:
        n, m, a = e.get('nom_fournisseur','').strip(), e.get('matricule_fiscal','').strip(), e.get('adresse_fournisseur','').strip()
        if n and f"{n}|{m}" not in f:
            f[f"{n}|{m}"] = {'nom': n, 'mat': m, 'adresse': a}
    return list(f.values())

def get_fournisseur_names():
    return sorted(set(f['nom'] for f in get_fournisseurs()))


class AutocompleteEntry(tk.Frame):
    """Entry avec dropdown de suggestions en temps reel (style Google)."""
    def __init__(self, parent, items, textvariable=None, on_select=None, **kw):
        bg = kw.get('bg', C['white'])
        font = kw.get('font', ('Segoe UI', 10))
        super().__init__(parent, bg=bg)
        self._items = list(items)
        self._on_select = on_select
        self._var = textvariable or tk.StringVar()

        self.entry = tk.Entry(self, textvariable=self._var, font=font,
                             relief=tk.SOLID, bd=1, bg=bg, fg=C['text'])
        self.entry.pack(fill='x', expand=True, ipady=3)
        self.entry.bind('<KeyRelease>', self._on_key)

        # Dropdown fenetre popup (comme une vraie combobox)
        self._dw = tk.Toplevel(self)
        self._dw.withdraw()
        self._dw.overrideredirect(True)
        self._dw.attributes('-topmost', True)
        self._lb = tk.Listbox(self._dw, height=5, font=font, bd=1, relief=tk.SOLID,
                             highlightthickness=0, selectbackground=C['primary'],
                             selectforeground=C['white'], activestyle='dotbox')
        self._lb.pack(fill='both', expand=True)
        self._lb.bind('<ButtonRelease-1>', self._pick)
        self._lb.bind('<Return>', self._pick)
        self._lb.bind('<Motion>', lambda e: (
            self._lb.selection_clear(0, 'end'),
            self._lb.selection_set(max(0, self._lb.nearest(e.y)))
        ) if 0 <= self._lb.nearest(e.y) < self._lb.size() else None)

        self.entry.bind('<FocusOut>', lambda e: self.after(200, self._hide))
        self._dw.bind('<FocusOut>', lambda e: self.after(200, self._hide))
        self._lb.bind('<FocusOut>', lambda e: self.after(200, self._hide))

    def _on_key(self, e):
        k = e.keysym
        if k in ('Return','Tab','Up','Down','Escape','Left','Right','Home','End','Prior','Next'):
            if k == 'Escape': self._hide()
            elif k == 'Down':
                if not self._lb_vis:
                    self._filter(force=True)
                if self._lb_vis:
                    self._lb.focus_set()
                    self._lb.selection_clear(0, 'end')
                    self._lb.selection_set(0)
                    self._lb.activate(0)
            elif k == 'Return':
                self._pick()
                self.entry.focus_set()
            return
        self._filter()

    def _filter(self, force=False):
        typed = self.entry.get()
        if not typed and not force:
            self._hide(); return
        if not typed and force:
            matches = list(self._items)
        else:
            matches = [i for i in self._items if not typed or typed.lower() in i.lower()]
        if matches:
            self._lb.delete(0, 'end')
            for m in matches: self._lb.insert('end', m)
            self._show()
        else:
            self._hide()

    def _show(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.entry.winfo_height()
        w = max(self.entry.winfo_width(), 50)
        self._dw.geometry(f"{w}x{self._lb.winfo_reqheight()}+{x}+{y}")
        self._dw.deiconify()
        self._dw.lift()
        self._lb_vis = True

    def _hide(self):
        self._dw.withdraw(); self._lb_vis = False

    def _pick(self, e=None):
        sel = self._lb.curselection()
        if not sel: return
        val = self._lb.get(sel[0])
        self._var.set(val)
        self.entry.icursor(len(val))
        self._hide()
        self.entry.focus_set()
        if self._on_select: self._on_select(val)

    def get(self): return self._var.get()
    def set(self, v): self._var.set(v)


# ═══════════════════════════════════════════════════
# COMPOSANTS UI PREMIUM
# ═══════════════════════════════════════════════════

class RoundedButton:
    """Bouton professionnel avec effet hover"""
    def __init__(self, parent, text, command=None, bg=C['primary'], fg=C['white'],
                 font=('Segoe UI', 11, 'bold'), px=28, py=12, icon=None):
        self._bg = bg
        self._hbg = self._lighten(bg)
        self._widget = tk.Button(parent, text=text, font=font, bg=bg, fg=fg,
                                 relief=tk.FLAT, bd=0, cursor='hand2',
                                 padx=px, pady=py, activebackground=self._hbg,
                                 activeforeground=fg, command=command)
        self._widget.bind('<Enter>', self._enter)
        self._widget.bind('<Leave>', self._leave)

    def _lighten(self, c):
        c = c.lstrip('#')
        r, g, b = int(c[0:2],16), int(c[2:4],16), int(c[4:6],16)
        return f'#{min(255,r+35):02x}{min(255,g+35):02x}{min(255,b+35):02x}'

    def _enter(self, e):
        self._widget.config(bg=self._hbg, activebackground=self._hbg)

    def _leave(self, e):
        self._widget.config(bg=self._bg, activebackground=self._hbg)

    def pack(self, **kw):
        self._widget.pack(**kw)

    @property
    def _btn(self):
        return self._widget

    @property
    def _label(self):
        return self._widget


class Tooltip:
    def __init__(self, widget, text):
        self._w = widget
        self._t = text
        self._tw = self._id = None
        widget.bind('<Enter>', self._schedule, add='+')
        widget.bind('<Leave>', self._hide, add='+')
        widget.bind('<ButtonPress>', self._hide, add='+')

    def _schedule(self, e=None):
        self._id = self._w.after(350, self._show)

    def _show(self):
        if self._tw: return
        x = self._w.winfo_rootx() + 18
        y = self._w.winfo_rooty() + self._w.winfo_height() + 6
        self._tw = tw = tk.Toplevel(self._w)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes('-topmost', True)
        f = tk.Frame(tw, bg='#263238', relief=tk.FLAT, bd=0)
        f.pack()
        tk.Label(f, text=self._t, justify=tk.LEFT,
                background='#263238', foreground='white',
                font=("Segoe UI",9), padx=10, pady=6).pack()

    def _hide(self, e=None):
        if self._id: self._w.after_cancel(self._id); self._id = None
        if self._tw: self._tw.destroy(); self._tw = None


# ═══════════════════════════════════════════════════
# SPLASH SCREEN
# ═══════════════════════════════════════════════════

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = 620, 420
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.configure(bg='#0a1628')
        self.overrideredirect(True)
        self.attributes('-alpha', 0)
        self._alpha = 0.0
        self._prog = 0
        self._wave = 0

        self._cw = tk.Canvas(self, width=w, height=h, bg='#0a1628', highlightthickness=0)
        self._cw.pack(fill='both', expand=True)

        # Cercles
        self._circles = []
        for i in range(4):
            c = self._cw.create_oval(0,0,0,0, outline=C['primary_light'], width=1.5)
            self._circles.append(c)

        # Logo
        self._logo = self._cw.create_oval(0,0,0,0, fill=C['white'], outline='')
        self._logot = self._cw.create_text(0,0, text="WA",
                                           font=('Segoe UI', 40, 'bold'), fill=C['primary'])

        self._rings = []
        for i in range(3):
            r = self._cw.create_oval(0,0,0,0, outline=C['primary_light'], width=1.2)
            self._rings.append(r)

        self._title = self._cw.create_text(w//2, 270, text="WissemArt Achat",
                                           font=('Segoe UI', 26, 'bold'), fill=C['white'])
        self._sub = self._cw.create_text(w//2, 300, text="Gestion Professionnelle des Achats",
                                         font=('Segoe UI', 12), fill=C['primary_bg'])

        # Barre progression
        self._pbg = self._cw.create_rectangle(100, 350, 520, 358, fill='#1a3060', outline='')
        self._pbar = self._cw.create_rectangle(100, 350, 100, 358, fill=C['primary_light'], outline='')
        self._ptxt = self._cw.create_text(w//2, 375, text="0%",
                                          font=('Segoe UI', 11, 'bold'), fill=C['white'])
        self._ltxt = self._cw.create_text(w//2, 395, text="Initialisation...",
                                          font=('Segoe UI', 10), fill=C['primary_bg'])
        self._fade_in()
        self._anim()

    def _fade_in(self):
        if self._alpha < 1:
            self._alpha = min(1, self._alpha + 0.06)
            self.attributes('-alpha', self._alpha)
            self.after(16, self._fade_in)

    def _anim(self):
        self._wave += 0.05
        t = time.time()
        w = self.winfo_width()
        for i, c in enumerate(self._circles):
            r = 40 + i * 30 + math.sin(self._wave + i) * 8
            self._cw.coords(c, w//2-r, 140-r, w//2+r, 140+r)

        pulse = math.sin(t * 2) * 3
        self._cw.coords(self._logo, w//2-50-pulse, 140-50-pulse, w//2+50+pulse, 140+50+pulse)
        self._cw.coords(self._logot, w//2, 140)

        angle = self._wave * 25
        for i, r in enumerate(self._rings):
            radius = 68 + i * 18
            ox = math.sin(angle + i) * 6
            oy = math.cos(angle + i) * 6
            self._cw.coords(r, w//2-radius+ox, 140-radius+oy, w//2+radius+ox, 140+radius+oy)

        msgs = [
            (0, "Initialisation..."),
            (25, "Chargement des donnees..."),
            (50, "Preparation de l'interface..."),
            (75, "Finalisation..."),
            (95, "Pret!")
        ]
        if self._prog < 100:
            self._prog += 0.9
            x = 100 + (self._prog / 100) * 420
            self._cw.coords(self._pbar, 100, 350, x, 358)
            self._cw.itemconfig(self._ptxt, text=f"{int(self._prog)}%")
            for p, m in msgs:
                if self._prog >= p:
                    self._cw.itemconfig(self._ltxt, text=m)
            self.after(25, self._anim)
        else:
            self._cw.itemconfig(self._ptxt, text="100%")
            self.after(400, self._fade_out)

    def _fade_out(self):
        if self._alpha > 0:
            self._alpha = max(0, self._alpha - 0.1)
            self.attributes('-alpha', self._alpha)
            self.after(16, self._fade_out)
        else:
            self.destroy()


# ═══════════════════════════════════════════════════
# LIGNE D'ACHAT
# ═══════════════════════════════════════════════════

class Ligne:
    def __init__(self, parent, on_change, on_delete, idx):
        self.pr = parent
        self.cb = on_change
        self.del_cb = on_delete
        self.idx = idx
        self.nom = tk.StringVar()
        self.ref = tk.StringVar()
        self.cat = tk.StringVar()
        self.dsg = tk.StringVar()
        self.qte = tk.StringVar()
        self.px = tk.StringVar()
        self.mt = tk.StringVar()
        self.prods = get_products()
        self.qte.trace_add('write', lambda *_: self._calc())
        self.px.trace_add('write', lambda *_: self._calc())
        self._build()

    def _build(self):
        f = tk.Frame(self.pr, bg=C['white'], highlightthickness=1,
                    highlightbackground=C['divider'], relief=tk.FLAT)
        f.pack(fill='x', padx=6, pady=2)
        self.fr = f
        i = tk.Frame(f, bg=C['white'], padx=8, pady=5)
        i.pack(fill='x')
        for col, w in enumerate([0,3,1,1,1,1,1,1,0]):
            if w > 0: i.columnconfigure(col, weight=w)

        tk.Label(i, text=f"#{self.idx}", font=('Segoe UI', 9, 'bold'),
                bg=C['white'], fg=C['primary'], width=3).grid(row=0,column=0, padx=(0,6), sticky='w')

        names = get_product_names()
        self.nc = AutocompleteEntry(i, names, textvariable=self.nom, on_select=lambda v: self._on_nom(), font=('Segoe UI',9))
        self.nc.grid(row=0,column=1, sticky='ew', padx=2, pady=3)
        Tooltip(self.nc.entry, "Rechercher un produit")

        self.ref.set(next_ref())
        tk.Entry(i, textvariable=self.ref, font=('Segoe UI',9),
                fg=C['text_sec'], bg=C['bg'], relief=tk.FLAT,
                state='readonly', width=8).grid(row=0,column=2, sticky='ew', padx=2, pady=3, ipady=3)

        tk.Entry(i, textvariable=self.cat, font=('Segoe UI',9),
                fg=C['text'], bg=C['white'], width=8,
                relief=tk.SOLID, bd=1).grid(row=0,column=3, sticky='ew', padx=2, pady=3, ipady=3)
        tk.Entry(i, textvariable=self.dsg, font=('Segoe UI',9),
                fg=C['text'], bg=C['white'], width=8,
                relief=tk.SOLID, bd=1).grid(row=0,column=4, sticky='ew', padx=2, pady=3, ipady=3)

        qe = tk.Entry(i, textvariable=self.qte, font=('Segoe UI',9,'bold'),
                     justify='center', width=6, fg=C['text'],
                     bg=C['white'], relief=tk.SOLID, bd=1)
        qe.grid(row=0,column=5, sticky='ew', padx=2, pady=3, ipady=3)
        Tooltip(qe, "Quantite")

        pe = tk.Entry(i, textvariable=self.px, font=('Segoe UI',9,'bold'),
                     justify='right', width=8, fg=C['text'],
                     bg=C['white'], relief=tk.SOLID, bd=1)
        pe.grid(row=0,column=6, sticky='ew', padx=2, pady=3, ipady=3)
        Tooltip(pe, "Prix unitaire TND")

        me = tk.Entry(i, textvariable=self.mt, font=('Segoe UI',10,'bold'),
                     state='readonly', justify='right', width=10,
                     bg=C['primary_bg'], fg=C['primary'], relief=tk.FLAT)
        me.grid(row=0,column=7, sticky='ew', padx=2, pady=3, ipady=3)
        Tooltip(me, "Montant automatique")

        n = len(self.pr.winfo_children())
        db = tk.Button(i, text='\u00d7', font=('Segoe UI',14,'bold'),
                      bg=C['white'], fg=C['error'] if n>1 else C['text_hint'],
                      relief=tk.FLAT, cursor='hand2' if n>1 else 'arrow',
                      width=2, bd=0,
                      command=lambda: self.del_cb(self) if n>1 else None)
        db.grid(row=0,column=8, padx=(6,0))
        db.bind('<Enter>', lambda e: e.widget.config(bg=C['error_bg']))
        db.bind('<Leave>', lambda e: e.widget.config(bg=C['white']))
        Tooltip(db, "Supprimer" if n>1 else "Minimum 1 ligne")

    def _on_nom(self):
        n = self.nom.get().strip()
        for p in self.prods:
            if p['nom'] == n:
                self.ref.set(p['ref']); self.cat.set(p['cat']); break

    def _calc(self):
        try:
            self.mt.set(fmt_money(dec(self.qte.get()) * dec(self.px.get())))
        except:
            self.mt.set('')
        self.cb()

    def get(self):
        return {'nom_produit':self.nom.get().strip(),'reference':self.ref.get().strip(),
                'categorie':self.cat.get().strip(),'design':self.dsg.get().strip(),
                'quantite':self.qte.get().strip(),
                'prix_unitaire':self.px.get().strip(),'montant_ligne':self.mt.get().strip()}

    def valid(self):
        d = self.get()
        if not d['nom_produit']: raise ValueError(f"Ligne {self.idx}: Nom requis")
        if not d['quantite']: raise ValueError(f"Ligne {self.idx}: Quantite requise")
        if not d['prix_unitaire']: raise ValueError(f"Ligne {self.idx}: Prix requis")
        q, p = dec(d['quantite']), dec(d['prix_unitaire'])
        if q <= 0: raise ValueError(f"Ligne {self.idx}: Quantite > 0")
        if p <= 0: raise ValueError(f"Ligne {self.idx}: Prix > 0")
        return True

    def destroy(self):
        self.fr.destroy()


# ═══════════════════════════════════════════════════
# GESTIONNAIRES (Produits, Fournisseurs)
# ═══════════════════════════════════════════════════

class BaseListWindow(Toplevel):
    def __init__(self, parent, title, w, h, cols, data, headings):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{w}x{h}")
        self.configure(bg=C['bg'])
        self.resizable(True, True)
        self.transient(parent)

        # Header
        hdr = tk.Frame(self, bg=C['primary'], height=52)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Label(hdr, text=title.upper(), font=('Segoe UI',13,'bold'),
                bg=C['primary'], fg=C['white']).pack(side='left', padx=20, pady=14)

        # Contenu
        f = tk.Frame(self, bg=C['white'])
        f.pack(fill='both', expand=True, padx=15, pady=15)

        self.tree = ttk.Treeview(f, columns=cols, show='headings', height=16)
        for c, t, anc, wd in headings:
            self.tree.heading(c, text=t, anchor=anc)
            self.tree.column(c, width=wd, minwidth=wd-30)

        sb = ttk.Scrollbar(f, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')

        # Bouton fermer
        bf = tk.Frame(self, bg=C['bg'])
        bf.pack(fill='x', padx=15, pady=(0,15))
        RoundedButton(bf, "Fermer", command=self.destroy,
                     bg=C['primary'], fg=C['white'],
                     font=('Segoe UI',10,'bold'), px=22, py=8).pack(side='right')

        self._load(data)

    def _load(self, data):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in data:
            self.tree.insert('', 'end', values=row)


class ProductManager(BaseListWindow):
    def __init__(self, parent):
        cols = ('nom', 'ref')
        headings = [('nom', 'Nom du Produit', 'w', 350), ('ref', 'Reference', 'center', 200)]
        data = [(p['nom'], p['ref']) for p in get_products()]
        super().__init__(parent, "Gestion des Produits", 650, 480, cols, data, headings)


class FournisseurManager(BaseListWindow):
    def __init__(self, parent):
        cols = ('nom', 'mat')
        headings = [('nom', 'Nom Fournisseur', 'w', 350), ('mat', 'Matricule Fiscal', 'center', 200)]
        data = [(f['nom'], f['mat']) for f in get_fournisseurs()]
        super().__init__(parent, "Gestion des Fournisseurs", 650, 480, cols, data, headings)


class EditWindow(tk.Toplevel):
    """Fenetre d'edition de facture avec suppression de lignes"""
    def __init__(self, parent, nf, entete, lignes):
        super().__init__(parent)
        self.title(f"Edition Facture N\u00b0 {nf}")
        w, h = 900, 700; sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.configure(bg=C['bg']); self.transient(parent)
        self.parent = parent; self.num_facture = nf
        self.lines = []; self.cnt = 1

        self.num_fac = tk.StringVar(value=nf)
        self.date = tk.StringVar(value=fmt_date_display(entete.get('date_achat','')))
        self.nom_four = tk.StringVar(value=entete.get('nom_fournisseur',''))
        self.mat = tk.StringVar(value=entete.get('matricule_fiscal',''))
        self.adresse = tk.StringVar(value=entete.get('adresse_fournisseur',''))
        self.mode = tk.StringVar(value=entete.get('mode_paiement',''))
        self.total = tk.StringVar(value=entete.get('total_achat',''))

        self._build()
        for i, l in enumerate(lignes, 1):
            nl = Ligne(self._lc, self._calc, self._del_line, i)
            nl.nom.set(l.get('nom_produit','')); nl.ref.set(l.get('reference',''))
            nl.cat.set(l.get('categorie','')); nl.dsg.set(l.get('design',''))
            nl.qte.set(l.get('quantite','')); nl.px.set(l.get('prix_unitaire',''))
            self.lines.append(nl); self.cnt = i+1
        self._calc()

    def _build(self):
        c = tk.Canvas(self, bg=C['bg'], highlightthickness=0)
        sb = ttk.Scrollbar(self, orient='vertical', command=c.yview)
        sf = tk.Frame(c, bg=C['bg'])
        sf.bind('<Configure>', lambda e: c.configure(scrollregion=c.bbox('all')))
        c.create_window((0,0), window=sf, anchor='nw')
        c.configure(yscrollcommand=sb.set)
        c.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')

        # Entete facture
        ic = tk.Frame(sf, bg=C['white'], highlightthickness=1, highlightbackground=C['border'])
        ic.pack(fill='x', padx=10, pady=(10,6))
        ih = tk.Frame(ic, bg=C['primary'], height=40)
        ih.pack(fill='x'); ih.pack_propagate(False)
        tk.Label(ih, text=f"EDITION FACTURE N\u00b0 {self.num_facture}", font=('Segoe UI',11,'bold'),
                bg=C['primary'], fg=C['white']).pack(side='left', padx=15, pady=9)

        iw = tk.Frame(ic, bg=C['white'])
        iw.pack(fill='x', padx=20, pady=12)
        iw.columnconfigure(1, weight=1); iw.columnconfigure(3, weight=1)
        fn = get_fournisseur_names()

        tk.Label(iw, text="N\u00b0 Facture", font=('Segoe UI',9,'bold'),
                bg=C['white'], fg=C['text_sec']).grid(row=0,column=0, sticky='w')
        tk.Entry(iw, textvariable=self.num_fac, font=('Segoe UI',10,'bold'),
                fg=C['primary'], bg=C['bg'], relief=tk.FLAT, state='readonly'
                ).grid(row=0,column=1, sticky='ew', padx=(0,18), pady=4, ipady=3)
        tk.Label(iw, text="Date *", font=('Segoe UI',9,'bold'),
                bg=C['white'], fg=C['text_sec']).grid(row=0,column=2, sticky='w')
        tk.Entry(iw, textvariable=self.date, font=('Segoe UI',10),
                fg=C['text'], bg=C['white'], relief=tk.SOLID, bd=1
                ).grid(row=0,column=3, sticky='ew', pady=4, ipady=3)

        tk.Label(iw, text="Fournisseur *", font=('Segoe UI',9,'bold'),
                bg=C['white'], fg=C['text_sec']).grid(row=1,column=0, sticky='w')
        fc = AutocompleteEntry(iw, fn, textvariable=self.nom_four, font=('Segoe UI',10))
        fc.grid(row=1,column=1, sticky='ew', padx=(0,18), pady=4)
        tk.Label(iw, text="Adresse", font=('Segoe UI',9,'bold'),
                bg=C['white'], fg=C['text_sec']).grid(row=1,column=2, sticky='w')
        tk.Entry(iw, textvariable=self.adresse, font=('Segoe UI',10),
                fg=C['text'], bg=C['white'], relief=tk.SOLID, bd=1
                ).grid(row=1,column=3, sticky='ew', pady=4, ipady=3)

        tk.Label(iw, text="Matricule", font=('Segoe UI',9,'bold'),
                bg=C['white'], fg=C['text_sec']).grid(row=2,column=0, sticky='w')
        tk.Entry(iw, textvariable=self.mat, font=('Segoe UI',10),
                fg=C['text'], bg=C['white'], relief=tk.SOLID, bd=1
                ).grid(row=2,column=1, sticky='ew', padx=(0,18), pady=4, ipady=3)
        tk.Label(iw, text="Paiement", font=('Segoe UI',9,'bold'),
                bg=C['white'], fg=C['text_sec']).grid(row=2,column=2, sticky='w')
        ttk.Combobox(iw, textvariable=self.mode, values=MODES_PAIEMENT,
                    state='readonly', font=('Segoe UI',10)
                    ).grid(row=2,column=3, sticky='ew', pady=4)

        # Lignes
        lc = tk.Frame(sf, bg=C['white'], highlightthickness=1, highlightbackground=C['border'])
        lc.pack(fill='both', expand=True, padx=10, pady=6)
        lh = tk.Frame(lc, bg=C['primary'], height=40)
        lh.pack(fill='x'); lh.pack_propagate(False)
        tk.Label(lh, text="LIGNES DE PRODUITS", font=('Segoe UI',11,'bold'),
                bg=C['primary'], fg=C['white']).pack(side='left', padx=15, pady=9)

        ch = tk.Frame(lc, bg=C['bg'])
        ch.pack(fill='x', padx=10, pady=(10,4))
        cols_data = [("", 3), ("Produit *", 3), ("Ref", 1), ("Cat.", 1),
                     ("Design", 1), ("Qte *", 1), ("Prix U. *", 1), ("Montant", 1), ("", 0)]
        for i, (t, w) in enumerate(cols_data):
            if w > 0: ch.columnconfigure(i, weight=w)
            tk.Label(ch, text=t, font=('Segoe UI',9,'bold'),
                    bg=C['bg'], fg=C['text']).grid(row=0,column=i, padx=2, sticky='ew' if i>0 else 'w')

        self._lc = tk.Frame(lc, bg=C['bg'])
        self._lc.pack(fill='both', expand=True, padx=6, pady=(0,10))

        af = tk.Frame(lc, bg=C['white'])
        af.pack(pady=8)
        tk.Button(af, text="+ AJOUTER LIGNE", font=('Segoe UI',10,'bold'),
                 bg=C['primary'], fg=C['white'], relief=tk.FLAT,
                 cursor='hand2', padx=28, pady=8, bd=0, command=self._add
                 ).pack()

        # Total + Boutons
        tc = tk.Frame(sf, bg=C['primary'])
        tc.pack(fill='x', padx=10, pady=(6,0))
        ti = tk.Frame(tc, bg=C['primary'])
        ti.pack(fill='x', padx=28, pady=12)
        tk.Label(ti, text="TOTAL:", font=('Segoe UI',14,'bold'),
                bg=C['primary'], fg=C['white']).pack(side='left')
        tk.Entry(ti, textvariable=self.total, font=('Segoe UI',20,'bold'),
                state='readonly', bg=C['primary'], fg=C['white'],
                relief=tk.FLAT, justify='right', width=12, bd=0).pack(side='right')
        tk.Label(ti, text="TND", font=('Segoe UI',12,'bold'),
                bg=C['primary'], fg=C['white']).pack(side='right', padx=(4,0))

        bf = tk.Frame(sf, bg=C['bg'])
        bf.pack(pady=12)
        for txt, bgc, cmd in [("ENREGISTRER", C['primary'], self.save), ("ANNULER", C['white'], self.destroy)]:
            b = tk.Button(bf, text=txt, font=('Segoe UI',11,'bold' if txt=='ENREGISTRER' else 'normal'),
                         bg=bgc, fg=C['white'] if txt=='ENREGISTRER' else C['primary'],
                         relief=tk.FLAT if txt=='ENREGISTRER' else tk.SOLID,
                         cursor='hand2', padx=30, pady=10, bd=2 if txt!='ENREGISTRER' else 0, command=cmd)
            b.pack(side='left', padx=6)

    def _add(self):
        l = Ligne(self._lc, self._calc, self._del_line, self.cnt)
        self.lines.append(l); self.cnt += 1

    def _del_line(self, line):
        if len(self.lines) <= 1: return
        line.destroy(); self.lines.remove(line)
        for i, l in enumerate(self.lines, 1): l.idx = i
        self._calc()

    def _calc(self):
        t = Decimal('0')
        for l in self.lines:
            try:
                if l.mt.get(): t += dec(l.mt.get())
            except: pass
        self.total.set(fmt_money(t))

    def save(self):
        try:
            if not self.date.get().strip(): raise ValueError("Date requise")
            if not self.nom_four.get().strip(): raise ValueError("Fournisseur requis")
            try: datetime.strptime(self.date.get().strip(),'%d/%m/%Y')
            except: raise ValueError("Format date invalide (JJ/MM/AAAA)")
            if not self.lines: raise ValueError("Au moins 1 ligne requise")
            for l in self.lines: l.valid()

            nf = self.num_facture
            write_csv(ENTETE_FILE, ENTETE_HEADERS,
                     [e for e in read_csv(ENTETE_FILE) if str(e['num_facture']).strip()!=nf])
            write_csv(LIGNE_FILE, LIGNE_HEADERS,
                     [l for l in read_csv(LIGNE_FILE) if str(l['num_facture']).strip()!=nf])

            append_csv(ENTETE_FILE, ENTETE_HEADERS, {
                'num_facture': nf, 'date_achat': fmt_date_iso(self.date.get().strip()),
                'nom_fournisseur': self.nom_four.get().strip(),
                'matricule_fiscal': self.mat.get().strip(),
                'adresse_fournisseur': self.adresse.get().strip(),
                'mode_paiement': self.mode.get().strip(),
                'total_achat': self.total.get()
            })
            for l in self.lines:
                d = l.get(); d['num_facture'] = nf
                append_csv(LIGNE_FILE, LIGNE_HEADERS, d)

            self.parent.refresh()
            messagebox.showinfo("Succes", f"Facture N\u00b0 {nf} mise a jour !", parent=self)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e), parent=self)


class ViewInvoice(tk.Toplevel):
    """Affichage formatte d'une facture (comme un vrai document)"""
    def __init__(self, parent, entete, lignes):
        super().__init__(parent)
        nf = entete.get('num_facture','')
        self.title(f"Facture N\u00b0 {nf}")
        w, h = 700, 750; sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.configure(bg=C['white']); self.transient(parent)

        c = tk.Frame(self, bg=C['white'], padx=40, pady=30)
        c.pack(fill='both', expand=True)

        # En-tete document
        tk.Label(c, text="WISSEMART ACHAT", font=('Segoe UI',18,'bold'),
                fg=C['primary'], bg=C['white']).pack(anchor='center')
        tk.Label(c, text="Systeme de Gestion Professionnel", font=('Segoe UI',9),
                fg=C['text_sec'], bg=C['white']).pack()
        tk.Frame(c, bg=C['primary'], height=2).pack(fill='x', pady=(12,20))

        # Infos facture
        info = tk.Frame(c, bg=C['white'])
        info.pack(fill='x')
        tk.Label(info, text=f"FACTURE N\u00b0 {nf}", font=('Segoe UI',14,'bold'),
                fg=C['text'], bg=C['white']).pack(anchor='w')
        tk.Label(info, text=f"Date: {fmt_date_display(entete.get('date_achat',''))}",
                font=('Segoe UI',10), fg=C['text_sec'], bg=C['white']).pack(anchor='w')
        tk.Frame(c, bg=C['divider'], height=1).pack(fill='x', pady=12)

        # Fournisseur
        sup = tk.Frame(c, bg=C['bg'], padx=15, pady=10, relief=tk.SOLID, bd=1)
        sup.pack(fill='x')
        tk.Label(sup, text="FOURNISSEUR", font=('Segoe UI',9,'bold'),
                fg=C['primary'], bg=C['bg']).pack(anchor='w')
        tk.Label(sup, text=entete.get('nom_fournisseur',''), font=('Segoe UI',11,'bold'),
                fg=C['text'], bg=C['bg']).pack(anchor='w')
        m = entete.get('matricule_fiscal','')
        if m: tk.Label(sup, text=f"Matricule: {m}", font=('Segoe UI',10),
                      fg=C['text_sec'], bg=C['bg']).pack(anchor='w')
        a = entete.get('adresse_fournisseur','')
        if a: tk.Label(sup, text=a, font=('Segoe UI',10),
                      fg=C['text_sec'], bg=C['bg']).pack(anchor='w')
        tk.Frame(c, bg=C['divider'], height=1).pack(fill='x', pady=12)

        # Tableau des lignes
        th = tk.Frame(c, bg=C['primary'])
        th.pack(fill='x')
        cols = [("Produit", 3), ("Ref", 1), ("Qte", 1), ("Prix U.", 1), ("Montant", 1)]
        for i, (t, w) in enumerate(cols):
            th.columnconfigure(i, weight=w)
            tk.Label(th, text=t, font=('Segoe UI',9,'bold'), bg=C['primary'], fg=C['white'],
                    padx=6, pady=6).grid(row=0, column=i, sticky='ew')

        total = Decimal('0')
        for l in lignes:
            rw = tk.Frame(c, bg=C['white'])
            rw.pack(fill='x')
            for i in range(5): rw.columnconfigure(i, weight=cols[i][1])
            tk.Label(rw, text=l.get('nom_produit',''), font=('Segoe UI',10),
                    bg=C['white'], fg=C['text'], padx=6, pady=4).grid(row=0,column=0, sticky='w')
            tk.Label(rw, text=l.get('reference',''), font=('Segoe UI',10),
                    bg=C['white'], fg=C['text_sec'], padx=6).grid(row=0,column=1)
            tk.Label(rw, text=l.get('quantite',''), font=('Segoe UI',10),
                    bg=C['white'], fg=C['text'], padx=6).grid(row=0,column=2)
            tk.Label(rw, text=l.get('prix_unitaire',''), font=('Segoe UI',10),
                    bg=C['white'], fg=C['text'], padx=6).grid(row=0,column=3)
            tk.Label(rw, text=l.get('montant_ligne',''), font=('Segoe UI',10,'bold'),
                    bg=C['white'], fg=C['text'], padx=6).grid(row=0,column=4)
            try: total += dec(l.get('montant_ligne',''))
            except: pass
            tk.Frame(c, bg=C['divider'], height=1).pack(fill='x')

        # Total
        tk.Frame(c, bg=C['primary'], height=1).pack(fill='x', pady=(10,4))
        tt = tk.Frame(c, bg=C['white'])
        tt.pack(fill='x')
        tt.columnconfigure(0, weight=3); tt.columnconfigure(1, weight=1)
        tk.Label(tt, text="TOTAL TND", font=('Segoe UI',12,'bold'),
                fg=C['text'], bg=C['white']).grid(row=0,column=0, sticky='e', padx=6)
        tk.Label(tt, text=fmt_money(total), font=('Segoe UI',14,'bold'),
                fg=C['primary'], bg=C['white']).grid(row=0,column=1, sticky='e', padx=6)
        tk.Label(tt, text=f"Mode: {entete.get('mode_paiement','')}", font=('Segoe UI',9),
                fg=C['text_sec'], bg=C['white']).grid(row=1,column=0, columnspan=2, sticky='e', padx=6, pady=(4,0))

        tk.Frame(c, bg=C['divider'], height=1).pack(fill='x', pady=(10,20))
        tk.Button(c, text="FERMER", font=('Segoe UI',11,'bold'),
                 bg=C['primary'], fg=C['white'], relief=tk.FLAT,
                 cursor='hand2', padx=30, pady=10, bd=0, command=self.destroy
                 ).pack()


# ═══════════════════════════════════════════════════
# APPLICATION PRINCIPALE
# ═══════════════════════════════════════════════════

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()

        # Splash
        splash = SplashScreen(self); self.update(); self.wait_window(splash)

        self.deiconify()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{sw}x{sh}+0+0")
        self.minsize(1200, 700)
        self.configure(bg=C['bg'])

        try:
            ip = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LogoWissem.ico")
            if os.path.exists(ip): self.iconbitmap(ip)
        except: pass

        init_csv(ENTETE_FILE, ENTETE_HEADERS)
        init_csv(LIGNE_FILE, LIGNE_HEADERS)

        self.lines = []
        self.cnt = 1
        self.all_entetes = []

        self._style()
        self._build()
        self.num_fac.set(str(next_facture()))
        self.mat.set(str(next_mat()))

    # ── Styles ──
    def _style(self):
        s = ttk.Style(); s.theme_use('clam')
        s.configure('Treeview', background=C['white'], foreground=C['text'],
                   rowheight=36, font=('Segoe UI',10), borderwidth=0,
                   fieldbackground=C['white'])
        s.configure('Treeview.Heading', background=C['primary'], foreground=C['white'],
                   font=('Segoe UI',10,'bold'), borderwidth=0, relief='flat')
        s.map('Treeview', background=[('selected','#1565C0')],
              foreground=[('selected',C['white'])])
        s.configure('TCombobox', fieldbackground=C['white'], background=C['white'],
                   foreground=C['text'], font=('Segoe UI',10), padding=5)
        s.configure('Vertical.TScrollbar', background=C['primary_bg'], troughcolor=C['white'],
                   bordercolor=C['border'], arrowsize=12)
        s.configure('Horizontal.TScrollbar', background=C['primary_bg'], troughcolor=C['white'],
                   bordercolor=C['border'], arrowsize=12)

    # ── Interface principale ──
    def _build(self):
        # ── CONTENU PRINCIPAL ──
        main = tk.Frame(self, bg=C['bg'])
        main.pack(side='left', fill='both', expand=True)

        # Header bar
        hdr = tk.Frame(main, bg=C['white'], height=60)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['primary'], height=2).pack(fill='x', side='bottom')

        # Titre page
        self._page_title = tk.Label(hdr, text="Nouvelle Facture",
                                    font=('Segoe UI',16,'bold'),
                                    bg=C['white'], fg=C['text'])
        self._page_title.pack(side='left', padx=25, pady=16)

        # ── CONTENU SCROLLABLE ──
        body = tk.Frame(main, bg=C['bg'])
        body.pack(fill='both', expand=True)

        # Paned principal
        self._pw = tk.PanedWindow(body, orient=tk.HORIZONTAL,
                                  sashwidth=6, bg=C['border'],
                                  sashrelief=tk.FLAT, bd=0)
        self._pw.pack(fill='both', expand=True, padx=12, pady=12)

        left = tk.Frame(self._pw, bg=C['bg'])
        right = tk.Frame(self._pw, bg=C['bg'])
        self._pw.add(left, minsize=650)
        self._pw.add(right, minsize=500)

        self._form(left)
        self._history(right)

    # ── FORMULAIRE FACTURE ──
    def _form(self, parent):
        c = tk.Canvas(parent, bg=C['bg'], highlightthickness=0)
        sb = ttk.Scrollbar(parent, orient='vertical', command=c.yview)
        sf = tk.Frame(c, bg=C['bg'])
        sf.bind('<Configure>', lambda e: c.configure(scrollregion=c.bbox('all')))
        c.create_window((0,0), window=sf, anchor='nw')
        c.configure(yscrollcommand=sb.set)
        c.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')

        # ── Carte infos facture ──
        ic = tk.Frame(sf, bg=C['white'], relief=tk.FLAT, bd=0,
                     highlightthickness=1, highlightbackground=C['border'])
        ic.pack(fill='x', padx=10, pady=(10,6))

        ih = tk.Frame(ic, bg=C['primary'], height=40)
        ih.pack(fill='x')
        ih.pack_propagate(False)
        tk.Label(ih, text="INFORMATIONS FACTURE", font=('Segoe UI',11,'bold'),
                bg=C['primary'], fg=C['white']).pack(side='left', padx=15, pady=9)

        iw = tk.Frame(ic, bg=C['white'])
        iw.pack(fill='x', padx=20, pady=16)
        iw.columnconfigure(1, weight=1); iw.columnconfigure(3, weight=1)

        self.num_fac = tk.StringVar()
        self.date = tk.StringVar(value=today())
        self.nom_four = tk.StringVar()
        self.mat = tk.StringVar()
        self.adresse = tk.StringVar()
        self.mode = tk.StringVar(value="Especes")
        self.total = tk.StringVar(value="0.000")

        fn = get_fournisseur_names()

        # Date
        tk.Label(iw, text="Date (JJ/MM/AAAA) *", font=('Segoe UI',9,'bold'),
                bg=C['white'], fg=C['text_sec']).grid(row=0,column=0, sticky='w', pady=(0,4))
        de = tk.Entry(iw, textvariable=self.date, font=('Segoe UI',10),
                     fg=C['text'], bg=C['white'], relief=tk.SOLID, bd=1)
        de.grid(row=0,column=1, sticky='ew', padx=(0,18), pady=(0,12), ipady=5)
        Tooltip(de, "Format JJ/MM/AAAA")

        # Fournisseur + Adresse (meme ligne)
        tk.Label(iw, text="Fournisseur *", font=('Segoe UI',9,'bold'),
                bg=C['white'], fg=C['text_sec']).grid(row=1,column=0, sticky='w', pady=(0,4))
        fc = AutocompleteEntry(iw, fn, textvariable=self.nom_four, on_select=lambda v: self._on_four(), font=('Segoe UI',10))
        fc.grid(row=1,column=1, sticky='ew', padx=(0,18), pady=(0,12))
        Tooltip(fc.entry, "Selectionner un fournisseur")

        tk.Label(iw, text="Adresse", font=('Segoe UI',9,'bold'),
                bg=C['white'], fg=C['text_sec']).grid(row=1,column=2, sticky='w', pady=(0,4))
        ae = tk.Entry(iw, textvariable=self.adresse, font=('Segoe UI',10),
                     fg=C['text'], bg=C['white'], relief=tk.SOLID, bd=1)
        ae.grid(row=1,column=3, sticky='ew', pady=(0,12), ipady=5)
        Tooltip(ae, "Adresse du fournisseur")

        # Matricule
        tk.Label(iw, text="Matricule Fiscal", font=('Segoe UI',9,'bold'),
                bg=C['white'], fg=C['text_sec']).grid(row=2,column=0, sticky='w', pady=(0,4))
        tk.Entry(iw, textvariable=self.mat, font=('Segoe UI',10),
                fg=C['text'], bg=C['white'], relief=tk.SOLID, bd=1
                ).grid(row=2,column=1, sticky='ew', padx=(0,18), pady=(0,12), ipady=5)

        # Mode paiement
        tk.Label(iw, text="Mode Paiement", font=('Segoe UI',9,'bold'),
                bg=C['white'], fg=C['text_sec']).grid(row=2,column=2, sticky='w', pady=(0,4))
        ttk.Combobox(iw, textvariable=self.mode, values=MODES_PAIEMENT,
                    state='readonly', font=('Segoe UI',10)
                    ).grid(row=2,column=3, sticky='ew', pady=(0,12))

        # ── Carte lignes de produits ──
        lc = tk.Frame(sf, bg=C['white'], relief=tk.FLAT, bd=0,
                      highlightthickness=1, highlightbackground=C['border'])
        lc.pack(fill='both', expand=True, padx=10, pady=6)

        lh = tk.Frame(lc, bg=C['primary'], height=40)
        lh.pack(fill='x')
        lh.pack_propagate(False)
        tk.Label(lh, text="LIGNES DE PRODUITS", font=('Segoe UI',11,'bold'),
                bg=C['primary'], fg=C['white']).pack(side='left', padx=15, pady=9)

        # En-tetes colonnes
        ch = tk.Frame(lc, bg=C['bg'])
        ch.pack(fill='x', padx=10, pady=(10,4))
        cols_data = [("", 3), ("Nom Produit *", 3), ("Ref", 1), ("Cat.", 1),
                     ("Design", 1), ("Qte *", 1), ("Prix U. *", 1), ("Montant", 1), ("", 0)]
        for i, (t, w) in enumerate(cols_data):
            if w > 0: ch.columnconfigure(i, weight=w)
            tk.Label(ch, text=t, font=('Segoe UI',9,'bold'),
                    bg=C['bg'], fg=C['text']).grid(row=0,column=i, padx=2, sticky='ew' if i>0 else 'w')

        self._lc = tk.Frame(lc, bg=C['bg'])
        self._lc.pack(fill='both', expand=True, padx=6, pady=(0,10))

        # Bouton ajouter
        af = tk.Frame(lc, bg=C['white'])
        af.pack(pady=10)
        ab = tk.Button(af, text="+ AJOUTER LIGNE", font=('Segoe UI',11,'bold'),
                      bg=C['primary'], fg=C['white'], relief=tk.FLAT,
                      cursor='hand2', padx=28, pady=10, bd=0, command=self._add)
        ab.pack()
        ab.bind('<Enter>', lambda e: e.widget.config(bg=C['primary_light']))
        ab.bind('<Leave>', lambda e: e.widget.config(bg=C['primary']))
        Tooltip(ab, "Ajouter une ligne de produit")

        self._add()

        # ── Total ──
        tc = tk.Frame(sf, bg=C['primary'], relief=tk.FLAT, bd=0)
        tc.pack(fill='x', padx=10, pady=(6,0))
        tk.Frame(tc, bg=C['primary_dark'], height=4).pack(fill='x', side='bottom')

        ti = tk.Frame(tc, bg=C['primary'])
        ti.pack(fill='x', padx=28, pady=18)

        tk.Label(ti, text="TOTAL:", font=('Segoe UI',14,'bold'),
                bg=C['primary'], fg=C['white']).pack(side='left')
        tk.Label(ti, text="TND", font=('Segoe UI',14,'bold'),
                bg=C['primary'], fg=C['white']).pack(side='right', padx=(6,0))
        tk.Entry(ti, textvariable=self.total, font=('Segoe UI',24,'bold'),
                state='readonly', bg=C['primary'], fg=C['white'],
                relief=tk.FLAT, justify='right', width=15, bd=0
                ).pack(side='right')

        # ── Boutons action ──
        af = tk.Frame(sf, bg=C['bg'])
        af.pack(fill='x', padx=10, pady=(10,20))
        ai = tk.Frame(af, bg=C['bg'])
        ai.pack()

        for txt, bg, fg, cmd, hl in [
            ("ENREGISTRER", C['primary'], C['white'], self.save, C['primary_light']),
            ("REINITIALISER", C['white'], C['primary'], self.reset, C['bg']),
        ]:
            b = tk.Button(ai, text=txt, font=('Segoe UI',12,'bold' if txt=='ENREGISTRER' else 'normal'),
                         bg=bg, fg=fg, relief=tk.FLAT if txt=='ENREGISTRER' else tk.SOLID,
                         cursor='hand2', padx=40, pady=16, bd=2 if txt!='ENREGISTRER' else 0,
                         command=cmd)
            b.pack(side='left', padx=6)
            b.bind('<Enter>', lambda e,bb=b,hh=hl: bb.config(bg=hh))
            b.bind('<Leave>', lambda e,bb=b,bbg=bg: bb.config(bg=bbg))

    # ── HISTORIQUE ──
    def _history(self, parent):
        # Recherche
        sf = tk.Frame(parent, bg=C['white'], relief=tk.FLAT, bd=0,
                      highlightthickness=1, highlightbackground=C['border'])
        sf.pack(fill='x')

        si = tk.Frame(sf, bg=C['white'])
        si.pack(fill='x', padx=15, pady=10)

        tk.Label(si, text="Rechercher :", font=('Segoe UI',11,'bold'),
                bg=C['white'], fg=C['text']).pack(side='left', padx=(5,10))

        self._search = tk.StringVar()
        self._search.trace_add('write', lambda *_: self._do_search())
        se = tk.Entry(si, textvariable=self._search, font=('Segoe UI',11),
                     relief=tk.FLAT, bd=0, bg=C['bg'], fg=C['text'])
        se.pack(side='left', fill='both', expand=True, padx=(0,10), ipady=8)

        rs = tk.Button(si, text="Tout", font=('Segoe UI',10,'bold'),
                      bg=C['primary'], fg=C['white'], relief=tk.FLAT,
                      cursor='hand2', padx=16, pady=7, bd=0,
                      command=lambda: self._search.set(''))
        rs.pack(side='right')
        rs.bind('<Enter>', lambda e: e.widget.config(bg=C['primary_light']))
        rs.bind('<Leave>', lambda e: e.widget.config(bg=C['primary']))

        # Paned vertical
        vp = tk.PanedWindow(parent, orient=tk.VERTICAL, sashwidth=6,
                           bg=C['border'], sashrelief=tk.FLAT, bd=0)
        vp.pack(fill='both', expand=True, pady=(4,0))

        # ── Entetes ──
        ec = tk.Frame(vp, bg=C['white'], relief=tk.FLAT, bd=0,
                      highlightthickness=1, highlightbackground=C['border'])
        vp.add(ec, minsize=230)

        eh = tk.Frame(ec, bg=C['primary'], height=45)
        eh.pack(fill='x')
        eh.pack_propagate(False)
        tk.Frame(eh, bg=C['primary_dark'], height=2).pack(fill='x', side='bottom')

        tk.Label(eh, text="HISTORIQUE DES FACTURES", font=('Segoe UI',12,'bold'),
                bg=C['primary'], fg=C['white']).pack(side='left', padx=18, pady=11)

        bf = tk.Frame(eh, bg=C['primary'])
        bf.pack(side='right', padx=12)

        for txt, bcol, cmd in [
            ("Voir", C['primary'], self._view),
            ("Editer", C['primary_light'], self._edit),
            ("Supprimer", C['primary_dark'], self._delete)
        ]:
            btn = tk.Button(bf, text=txt, font=('Segoe UI',9,'bold'),
                          bg=bcol, fg=C['white'], relief=tk.FLAT,
                          cursor='hand2', padx=14, pady=6, bd=0, command=cmd)
            btn.pack(side='left', padx=2)
            btn.bind('<Enter>', lambda e,b=btn: b.config(bg=C['primary']))
            btn.bind('<Leave>', lambda e,b=btn,c=bcol: b.config(bg=c))

        eb = tk.Frame(ec, bg=C['bg'])
        eb.pack(fill='both', expand=True, padx=12, pady=10)

        cols = ("num_facture","date_achat","nom_fournisseur","mode_paiement","total_achat")
        self._et = ttk.Treeview(eb, columns=cols, show='headings', height=7, selectmode='browse')

        for col, txt, anc, w in [
            ("num_facture","N\u00b0 Facture",'center',100),
            ("date_achat","Date",'center',100),
            ("nom_fournisseur","Fournisseur",'w',190),
            ("mode_paiement","Paiement",'center',100),
            ("total_achat","Total (TND)",'e',115)
        ]:
            self._et.heading(col, text=txt, anchor=anc)
            self._et.column(col, width=w, minwidth=w-20, anchor=anc)

        sb1 = ttk.Scrollbar(eb, orient='vertical', command=self._et.yview)
        self._et.configure(yscrollcommand=sb1.set)
        self._et.pack(side='left', fill='both', expand=True)
        sb1.pack(side='right', fill='y')
        self._et.bind('<<TreeviewSelect>>', self._on_select)

        # ── Lignes ──
        lc = tk.Frame(vp, bg=C['white'], relief=tk.FLAT, bd=0,
                      highlightthickness=1, highlightbackground=C['border'])
        vp.add(lc, minsize=200)

        lh = tk.Frame(lc, bg=C['primary'], height=45)
        lh.pack(fill='x')
        lh.pack_propagate(False)
        tk.Frame(lh, bg=C['primary_dark'], height=2).pack(fill='x', side='bottom')

        self._ll = tk.Label(lh, text="LIGNES DE LA FACTURE",
                           font=('Segoe UI',12,'bold'), bg=C['primary'], fg=C['white'])
        self._ll.pack(side='left', padx=18, pady=11)

        lb = tk.Frame(lc, bg=C['bg'])
        lb.pack(fill='both', expand=True, padx=12, pady=10)

        lcols = ("nom_produit","reference","categorie","design","quantite","prix_unitaire","montant_ligne")
        self._lt = ttk.Treeview(lb, columns=lcols, show='headings', height=5, selectmode='browse')

        for col, txt, anc, w in [
            ("nom_produit","Produit",'w',140),("reference","Ref",'center',80),
            ("categorie","Cat.",'center',75),("design","Design",'center',75),
            ("quantite","Qte",'center',70),
            ("prix_unitaire","Prix U.",'e',90),("montant_ligne","Montant",'e',95)
        ]:
            self._lt.heading(col, text=txt, anchor=anc)
            self._lt.column(col, width=w, minwidth=w-20)

        sb2 = ttk.Scrollbar(lb, orient='vertical', command=self._lt.yview)
        self._lt.configure(yscrollcommand=sb2.set)
        self._lt.pack(side='left', fill='both', expand=True)
        sb2.pack(side='right', fill='y')

    # ── Actions ──
    def _add(self):
        l = Ligne(self._lc, self._calc, self._del_line, self.cnt)
        self.lines.append(l); self.cnt += 1

    def _del_line(self, line):
        if len(self.lines) <= 1: return
        line.destroy(); self.lines.remove(line)
        for i, l in enumerate(self.lines, 1): l.idx = i
        self._calc()

    def _calc(self):
        t = Decimal('0')
        for l in self.lines:
            try:
                if l.mt.get(): t += dec(l.mt.get())
            except: pass
        self.total.set(fmt_money(t))

    def _on_four(self):
        n = self.nom_four.get().strip()
        for f in get_fournisseurs():
            if f['nom'] == n:
                self.mat.set(f['mat'])
                self.adresse.set(f['adresse'])
                break

    def _on_select(self, e):
        sel = self._et.selection()
        if not sel: return
        v = self._et.item(sel[0])['values']
        nf = str(v[0]).strip()
        self._ll.config(text=f"LIGNES DE LA FACTURE N\u00b0 {nf}")

        for i in self._lt.get_children(): self._lt.delete(i)
        for l in read_csv(LIGNE_FILE):
            if str(l['num_facture']).strip() == nf:
                self._lt.insert('','end', values=(
                    l.get('nom_produit',''), l.get('reference',''),
                    l.get('categorie',''), l.get('design',''),
                    l.get('quantite',''),
                    l.get('prix_unitaire',''), l.get('montant_ligne','')
                ))

    def _do_search(self):
        q = self._search.get().strip().lower()
        for i in self._et.get_children(): self._et.delete(i)
        if not q: self.refresh(); return
        for e in self.all_entetes:
            if (q in str(e.get('num_facture','')).lower() or
                q in str(e.get('nom_fournisseur','')).lower() or
                q in str(e.get('mode_paiement','')).lower()):
                self._et.insert('','end', values=(
                    e.get('num_facture',''), fmt_date_display(e.get('date_achat','')),
                    e.get('nom_fournisseur',''), e.get('mode_paiement',''),
                    e.get('total_achat','')
                ))

    # ── Save ──
    def save(self):
        try:
            if not self.num_fac.get().strip(): raise ValueError("N\u00b0 facture requis")
            if not self.date.get().strip(): raise ValueError("Date requise")
            if not self.nom_four.get().strip(): raise ValueError("Fournisseur requis")
            try: datetime.strptime(self.date.get().strip(),'%d/%m/%Y')
            except: raise ValueError("Format date invalide (JJ/MM/AAAA)")
            if not self.lines: raise ValueError("Au moins 1 ligne requise")
            for l in self.lines: l.valid()

            nf = self.num_fac.get().strip()
            append_csv(ENTETE_FILE, ENTETE_HEADERS, {
                'num_facture': nf, 'date_achat': fmt_date_iso(self.date.get().strip()),
                'nom_fournisseur': self.nom_four.get().strip(),
                'matricule_fiscal': self.mat.get().strip(),
                'adresse_fournisseur': self.adresse.get().strip(),
                'mode_paiement': self.mode.get().strip(),
                'total_achat': self.total.get()
            })
            for l in self.lines:
                d = l.get(); d['num_facture'] = nf
                append_csv(LIGNE_FILE, LIGNE_HEADERS, d)

            messagebox.showinfo("Succes",
                              f"Facture N\u00b0 {nf} enregistree !\nTotal: {self.total.get()} TND\nLignes: {len(self.lines)}",
                              parent=self)
            self.reset(); self.refresh()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e), parent=self)

    def reset(self):
        self.num_fac.set(str(next_facture()))
        self.date.set(today()); self.nom_four.set('')
        self.mat.set(str(next_mat())); self.adresse.set(''); self.mode.set("Especes"); self.total.set("0.000")
        for l in self.lines: l.destroy()
        self.lines.clear(); self.cnt = 1; self._add()
        self._page_title.config(text="Nouvelle Facture")

    def refresh(self):
        for i in self._et.get_children(): self._et.delete(i)
        self.all_entetes = read_csv(ENTETE_FILE)
        for e in self.all_entetes:
            self._et.insert('','end', values=(
                e.get('num_facture',''), fmt_date_display(e.get('date_achat','')),
                e.get('nom_fournisseur',''), e.get('mode_paiement',''),
                e.get('total_achat','')
            ))
        for i in self._lt.get_children(): self._lt.delete(i)
        self._ll.config(text="LIGNES DE LA FACTURE")

    def _view(self):
        sel = self._et.selection()
        if not sel: return messagebox.showwarning("Attention","Selectionnez une facture", parent=self)
        v = self._et.item(sel[0])['values']; nf = str(v[0]).strip()
        entete = next((e for e in self.all_entetes if str(e['num_facture']).strip()==nf), None)
        if not entete: return
        lignes = [l for l in read_csv(LIGNE_FILE) if str(l['num_facture']).strip()==nf]
        ViewInvoice(self, entete, lignes)

    def _edit(self):
        sel = self._et.selection()
        if not sel: return messagebox.showwarning("Attention","Selectionnez une facture", parent=self)
        v = self._et.item(sel[0])['values']; nf = str(v[0]).strip()
        entete = next((e for e in self.all_entetes if str(e['num_facture']).strip()==nf), None)
        if not entete: return
        lignes = [l for l in read_csv(LIGNE_FILE) if str(l['num_facture']).strip()==nf]
        EditWindow(self, nf, entete, lignes)

    def _delete_silent(self, nf):
        try:
            write_csv(ENTETE_FILE, ENTETE_HEADERS,
                     [e for e in read_csv(ENTETE_FILE) if str(e['num_facture']).strip()!=nf])
            write_csv(LIGNE_FILE, LIGNE_HEADERS,
                     [l for l in read_csv(LIGNE_FILE) if str(l['num_facture']).strip()!=nf])
            self.refresh()
        except Exception as e:
            messagebox.showerror("Erreur", str(e), parent=self)

    def _delete(self):
        sel = self._et.selection()
        if not sel: return messagebox.showwarning("Attention","Selectionnez une facture", parent=self)
        v = self._et.item(sel[0])['values']; nf, nom, tot = str(v[0]).strip(), v[2], v[4]
        if not messagebox.askyesno("Confirmation",
                                   f"Supprimer la facture N\u00b0 {nf} ?\n\nFournisseur: {nom}\nTotal: {tot} TND",
                                   parent=self): return
        try:
            all_l = read_csv(LIGNE_FILE)
            nb = len([l for l in all_l if str(l['num_facture']).strip()==nf])
            write_csv(ENTETE_FILE, ENTETE_HEADERS,
                     [e for e in read_csv(ENTETE_FILE) if str(e['num_facture']).strip()!=nf])
            write_csv(LIGNE_FILE, LIGNE_HEADERS,
                     [l for l in all_l if str(l['num_facture']).strip()!=nf])
            messagebox.showinfo("Succes",f"Facture N\u00b0 {nf} supprimee\nLignes: {nb}", parent=self)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Erreur", str(e), parent=self)

    def _open_products(self):
        ProductManager(self)

    def _open_fournisseurs(self):
        FournisseurManager(self)

    def _help(self):
        msg = (
            "WissemArt Achat v2.0\n\n"
            "Connexion: wissem / admin\n\n"
            "Fonctionnalites:\n"
            "- Gestion des factures d'achat\n"
            "- Edition et suppression\n"
            "- Gestion des produits et fournisseurs\n"
            "- Recherche en temps reel\n\n"
            "Developpe avec Tkinter & Python"
        )
        messagebox.showinfo("Aide", msg, parent=self)


if __name__ == "__main__":
    App().mainloop()
