import tkinter as tk
from tkinter import messagebox, ttk

# Definisi Aturan CNF berdasarkan dokumen Kelompok 5 TBO
cnf_rules = {
    # Non-terminal -> [ (Non-terminal, Non-terminal), ... ]
    'S': [('PP', 'NP'), ('PP', 'C1'), ('PP', 'C2'), ('PP', 'C3'), ('PP', 'C4')],
    'C1': [('NP', 'PP')],
    'C2': [('NP', 'VP')],
    'C3': [('VP', 'NP')],
    'C4': [('VP', 'C5')],
    'C5': [('NP', 'PP')],
    'PP': [('Prep', 'NP'), ('N_lok', 'NP'), ('Prep_time', 'N_time')],
    'NP': [('N_lok', 'N')],
    'VP': [('Aux', 'V'), ('V', 'NP')],
    
    # Aturan Terminal (A -> a) berdasarkan simbol terminal dokumen
    'Prep': ['ring', 'ka', 'saking'],
    'N_lok': ['duur', 'betén', 'tengah', 'sisin'],
    'N': ['temboké', 'kranjangé', 'lemariné', 'punyan kayuné', 'tukadé', 'carik', 'pasar', 
          'balé banjar', 'paon', 'hotél', 'meongé', 'siapé', 'bajuné', 'kedisé', 
          'umahné', 'tamuné', 'bikul', 'amah', 'gerang', 'panggung', 'arit', 'baas', 'nyrati', 'mémé'],
    'PropN': ['Bli Wayan', 'Mbok Putu', 'I Nyoman', 'Luh Sari'],
    'Aux': ['lakar', 'suba', 'tusing', 'sedek', 'iteh'],
    'V': ['nguber', 'adep', 'anggon', 'ngalih', 'kontrakang', 'manyi', 'meblanja', 'rapat', 
          'ngoreng', 'nginep', 'pules', 'mati', 'melah', 'memunyi', 'dadi', 'ngaba', 'numbas', 'malajah', 'nulungin', 'madaar'],
    'Prep_time': ['uli', 'dugas', 'saking', 'rikala', 'mara'],
    'N_time': ['tuni', 'sanja', 'ibi', 'ujan', 'pidan', 'semeng', 'tengai', 'liburan', 'pagi', 'tuni semeng', 'ibi sanja', 'mara pisan', 'uli mara']
}

def cyk_algorithm(sentence):
    temp_sentence = sentence.lower().replace('.', '').strip()
    # Menangani frasa multi-kata dari dokumen
    special_phrases = ['bli wayan', 'mbok putu', 'i nyoman', 'luh sari', 'punyan kayuné', 
                       'balé banjar', 'tuni semeng', 'ibi sanja', 'mara pisan', 'uli mara']
    
    for phrase in special_phrases:
        if phrase in temp_sentence:
            temp_sentence = temp_sentence.replace(phrase, phrase.replace(' ', '_'))
    
    words = [w.replace('_', ' ') for w in temp_sentence.split()]
    n = len(words)
    if n == 0: return False, [], []

    # Inisialisasi tabel CYK (n x n)
    table = [[set() for _ in range(n + 1)] for _ in range(n + 1)]

    # Langkah 1: Terminal filling
    for i in range(1, n + 1):
        word = words[i-1]
        for lhs, rhs_list in cnf_rules.items():
            if isinstance(rhs_list, list) and word in rhs_list:
                table[i][1].add(lhs)
        
        # Penanganan unit production (NP -> N, NP -> PropN, VP -> V)
        if 'N' in table[i][1] or 'PropN' in table[i][1]: table[i][1].add('NP')
        if 'V' in table[i][1]: table[i][1].add('VP')

    # Langkah 2: Filling the rest of the table
    for j in range(2, n + 1):
        for i in range(1, n - j + 2):
            for k in range(1, j):
                for lhs, rhs_list in cnf_rules.items():
                    for rhs in rhs_list:
                        if isinstance(rhs, tuple) and len(rhs) == 2:
                            if rhs[0] in table[i][k] and rhs[1] in table[i+k][j-k]:
                                table[i][j].add(lhs)
    
    return 'S' in table[1][n], table, words

class CYKVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Balinese Syntax Checker - CYK Visualization")
        self.root.geometry("900x650")
        self.root.configure(bg="#1e272e")

        # Header
        tk.Label(root, text="CYK Parsing Table Visualizer", font=("Arial", 20, "bold"), 
                 fg="#f5f6fa", bg="#1e272e").pack(pady=15)

        # Input Area
        input_frame = tk.Frame(root, bg="#1e272e")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Kalimat Bali:", font=("Arial", 11), fg="#dcdde1", bg="#1e272e").grid(row=0, column=0, padx=5)
        self.entry = tk.Entry(input_frame, font=("Arial", 12), width=50)
        self.entry.grid(row=0, column=1, padx=10)
        self.entry.insert(0, "Ring hotél pules tamuné") # Contoh dari gambar Anda

        self.btn = tk.Button(input_frame, text="Proses CYK", command=self.run_analysis, 
                             bg="#00d2d3", fg="black", font=("Arial", 10, "bold"), padx=15)
        self.btn.grid(row=0, column=2, padx=5)

        # Result Label
        self.res_label = tk.Label(root, text="Hasil: -", font=("Arial", 14), bg="#1e272e", fg="white")
        self.res_label.pack(pady=5)

        # Table Container
        self.table_frame = tk.Frame(root, bg="#2f3640", bd=2, relief="sunken")
        self.table_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def run_analysis(self):
        # Clear existing table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        sentence = self.entry.get()
        is_valid, table, words = cyk_algorithm(sentence)
        n = len(words)

        if n == 0: return

        # Update Result
        status = "VALID (Sesuai Tata Bahasa)" if is_valid else "TIDAK VALID"
        color = "#1dd1a1" if is_valid else "#ff6b6b"
        self.res_label.config(text=f"Hasil: {status}", fg=color)

        # Build Table Grid
        # Header baris (Header token)
        for idx, word in enumerate(words):
            tk.Label(self.table_frame, text=word, font=("Arial", 10, "bold"), bg="#57606f", fg="white", 
                     width=12, height=2, borderwidth=1, relief="solid").grid(row=0, column=idx+1)
        
        # Header kolom (Token samping)
        for idx, word in enumerate(words):
            tk.Label(self.table_frame, text=word, font=("Arial", 10, "bold"), bg="#57606f", fg="white", 
                     width=12, height=2, borderwidth=1, relief="solid").grid(row=idx+1, column=0)

        # Content Cells
        # Transformasi tabel CYK ke format grid visual sesuai gambar user
        for j in range(1, n + 1): # Panjang sub-string
            for i in range(1, n - j + 2): # Start index
                content = ", ".join(sorted(list(table[i][j]))) if table[i][j] else "Ø"
                fg_cell = "#1dd1a1" if 'S' in table[i][j] else "white"
                
                # Menentukan posisi sel di grid (diagonal terbalik)
                tk.Label(self.table_frame, text=content, font=("Arial", 10), bg="#2f3640", fg=fg_cell,
                         width=12, height=2, borderwidth=1, relief="solid").grid(row=i + j - 1, column=i)

if __name__ == "__main__":
    root = tk.Tk()
    app = CYKVisualizer(root)
    root.mainloop()