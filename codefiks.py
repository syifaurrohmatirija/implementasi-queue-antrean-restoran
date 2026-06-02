import queue 
import os 
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup 
from kivy.uix.widget import Widget 
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.clock import Clock
from kivy.metrics import dp

# ==============================================================================
# DATABASE GLOBAL RESTORAN & WARNA
# ==============================================================================
KREM_BG      = (0.97, 0.96, 0.94, 1)  
PUTIH_MURNI  = (1.00, 1.00, 1.00, 1)  
PINK_AKSEN   = (0.93, 0.45, 0.53, 1)  
CHARCOAL     = (0.18, 0.18, 0.18, 1) 
CHARCOAL_SEC = (0.40, 0.40, 0.40, 1)  
MATCHY_GREEN = (0.15, 0.50, 0.25, 1)  
ABU_GARIS    = (0.88, 0.86, 0.82, 1)  

ANTREAN_RESTORAN = queue.Queue() 
KERANJANG_SEMENTARA = None
RIWAYAT_NOTA = []                
STATUS_DATABASE_MEJA = {i: None for i in range(1, 13)}

DAPUR_AKTIF = True
WAKTU_MULAI_AKTIF = datetime.now()
DURASI_PROSES_DAPUR = 60 

WAKTU_MENU_REF = {
    "Ramyeon": 6, "Kimchi Fried Rice": 6, "Tteokbokki": 6, "Rabokki": 6, "Jjajangmyeon": 7, 
    "K-Fried Chicken w/ Rice": 9, "French Fries": 3, "Mandu (Korean Dumpling)": 5, 
    "Corn Dog Mozzarella": 6, "Bungeoppang": 5, "Croffle": 5, "Bingsu": 6,
    "Es Teh Manis": 2, "Lemon Tea": 2, "Mineral Water": 1, "Iced Americano": 2, 
    "Banana Milk": 2, "Matcha Latte": 3, "Korean Strawberry Milk": 3
}

# ==============================================================================
# DATA AWAL 
# ==============================================================================
DATA_TERBARU_INPUT = [
    "Gaeul | Ramyeon, Es Teh Manis | 36000 | Dine In | 1",
    "Reyhan | Kimchi Fried Rice, Lemon Tea | 47000 | Take Away | -",
    "Ziva | Tteokbokki, Mineral Water | 38000 | Dine In | 2",
    "Aris | Rabokki, Banana Milk | 58000 | Dine In | 3",
    "Wulan | Jjajangmyeon, Iced Americano | 62000 | Take Away | -",
    "Kenzie | K-Fried Chicken w/ Rice, Matcha Latte | 70000 | Dine In | 4",
    "Nabila | French Fries, Es Teh Manis | 28000 | Take Away | -",
    "Farel | Mandu (Korean Dumpling), Lemon Tea | 40000 | Dine In | 5",
    "Gisella | Corn Dog Mozzarella, Mineral Water | 31000 | Take Away | -",
    "Radit | Bungeoppang, Korean Strawberry Milk | 45000 | Dine In | 6",
    "Naomi | Croffle, Iced Americano | 44000 | Dine In | 7",
    "Anton | Bingsu, Es Teh Manis | 40000 | Take Away | -",
    "Karina | Ramyeon, Banana Milk | 52000 | Dine In | 8",
    "Bintang | Kimchi Fried Rice, Matcha Latte | 60000 | Take Away | -",
    "Winter | Tteokbokki, Korean Strawberry Milk | 59000 | Dine In | 9",
    "Arka | Rabokki, Lemon Tea | 46000 | Take Away | -",
    "Nadin | Jjajangmyeon, Mineral Water | 48000 | Dine In | 10",
    "Gavin | K-Fried Chicken w/ Rice, Iced Americano | 65000 | Take Away | -",
    "Tiara | French Fries, Banana Milk | 44000 | Dine In | 11",
    "Elang | Mandu (Korean Dumpling), Matcha Latte | 53000 | Take Away | -",
    "Shena | Corn Dog Mozzarella, Korean Strawberry Milk | 52000 | Take Away | -",
    "Carmen | Bungeoppang, Es Teh Manis | 26000 | Take Away | -",
    "Amara | Croffle, Lemon Tea | 36000 | Take Away | -",
    "Bagas | Bingsu, Mineral Water | 38000 | Take Away | -",
    "Clara | Ramyeon, Iced Americano | 48000 | Take Away | -",
    "Devan | Kimchi Fried Rice, Banana Milk | 59000 | Take Away | -",
    "Leya | Tteokbokki, Matcha Latte | 57000 | Take Away | -",
    "Farhan | Rabokki, Korean Strawberry Milk | 61000 | Take Away | -",
    "Grace | Jjajangmyeon, Es Teh Manis | 50000 | Take Away | -",
    "Hanif | K-Fried Chicken w/ Rice, Lemon Tea | 57000 | Take Away | -",
    "Indah | French Fries, Mineral Water | 26000 | Take Away | -",
    "Joni | Mandu (Korean Dumpling), Iced Americano | 48000 | Take Away | -",
    "Keisha | Corn Dog Mozzarella, Banana Milk | 49000 | Take Away | -",
    "Lino | Bungeoppang, Matcha Latte | 43000 | Take Away | -",
    "Maura | Croffle, Korean Strawberry Milk | 51000 | Take Away | -",
    "Niko | Bingsu, Es Teh Manis | 40000 | Take Away | -",
    "Olivia | Ramyeon, Lemon Tea | 40000 | Take Away | -",
    "Putra | Kimchi Fried Rice, Mineral Water | 41000 | Take Away | -",
    "Suzy | Tteokbokki, Iced Americano | 52000 | Take Away | -",
    "Rian | Rabokki, Banana Milk | 58000 | Take Away | -",
    "Salsa | Jjajangmyeon, Matcha Latte | 67000 | Take Away | -",
    "Tomi | K-Fried Chicken w/ Rice, Korean Strawberry Milk | 72000 | Take Away | -",
    "Ufa | French Fries, Es Teh Manis | 28000 | Take Away | -",
    "Vino | Mandu (Korean Dumpling), Lemon Tea | 40000 | Take Away | -",
    "Wanda | Corn Dog Mozzarella, Mineral Water | 31000 | Take Away | -",
    "Xavi | Bungeoppang, Iced Americano | 38000 | Take Away | -",
    "Yuna | Croffle, Banana Milk | 48000 | Take Away | -",
    "Zaki | Bingsu, Matcha Latte | 57000 | Take Away | -",
    "Ziva | Ramyeon, Korean Strawberry Milk | 55000 | Take Away | -",
    "Giri | Kimchi Fried Rice, Es Teh Manis | 43000 | Take Away | -"
]

def inisialisasi_antrean_coding():
    global RIWAYAT_NOTA, STATUS_DATABASE_MEJA
    waktu_base = datetime.now()
    
    for idx, baris_string in enumerate(DATA_TERBARU_INPUT):
        bagian = baris_string.split(" | ")
        nama_pelanggan = bagian[0].strip()
        list_makanan = [m.strip() for m in bagian[1].split(",")]
        harga_total = int(bagian[2].strip())
        tipe_servis = bagian[3].strip().lower().replace(" ", "_")
        no_meja_raw = bagian[4].strip()
        no_meja = int(no_meja_raw) if no_meja_raw.isdigit() else None

        waktu_masuk_logis = waktu_base + timedelta(minutes=(idx * 2))
        total_estimasi_menit = sum(WAKTU_MENU_REF.get(m, 2) for m in list_makanan)
        waktu_siap_logis = waktu_masuk_logis + timedelta(minutes=total_estimasi_menit)
        
        if "dine_in" in tipe_servis and no_meja:
            if no_meja <= 12 and STATUS_DATABASE_MEJA[no_meja] is None:
                STATUS_DATABASE_MEJA[no_meja] = nama_pelanggan
            nama_final = f"{nama_pelanggan} (Meja {no_meja})"
            tipe_label = f"DINE IN (Meja: {no_meja})"
        else:
            nama_final = f"{nama_pelanggan} (Take Away)"
            tipe_label = "TAKE AWAY"
            
        data_pesanan = {
            "nama_panggilan": nama_pelanggan,
            "nama": nama_final,
            "makanan": list_makanan,
            "catatan_per_menu": {},
            "total_harga": harga_total,
            "jam_datang": waktu_masuk_logis.strftime("%H:%M:%S")
        }
        ANTREAN_RESTORAN.put(data_pesanan)
        
        counts = {}
        for m in list_makanan: counts[m] = counts.get(m, 0) + 1
        teks_rincian_menu = "".join([f"   • {m_nama} (x{qty})\n" for m_nama, qty in counts.items()])
            
        nota_teks = (
            f"============ NOTA DIGITAL ============\n"
            f"Pelanggan : {nama_pelanggan}\n"
            f"Metode    : {tipe_label}\n"
            f"Jam Masuk : {waktu_masuk_logis.strftime('%H:%M:%S')} WIB\n"
            f"Est. Siap : {waktu_siap_logis.strftime('%H:%M:%S')} WIB ({total_estimasi_menit} mnt)\n"
            f"--------------------------------------\n"
            f"Pesanan:\n{teks_rincian_menu}"
            f"--------------------------------------\n"
            f"TOTAL     : Rp {harga_total:,}\n"
            f"Status    : LUNAS (Koding Import)\n"
            f"======================================"
        )
        RIWAYAT_NOTA.append(nota_teks)

inisialisasi_antrean_coding()

def cari_gambar_valid(nama_base):
    ekstensi_dicoba = ['.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG']
    for ext in ekstensi_dicoba:
        nama_file_lengkap = nama_base + ext
        if os.path.exists(nama_file_lengkap):
            return nama_file_lengkap
    return ""  

class Background(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*KREM_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MenuDividerRow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*ABU_GARIS)
            self.line = Line(points=[self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1]], width=1)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.line.points = [self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1]]

class CapsuleCounter(BoxLayout):
    def __init__(self, menu_name, callback_change, callback_note, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 4
        self.menu_name = menu_name
        self.callback_change = callback_change
        self.callback_note = callback_note
        self.qty = 0
        self.current_note = "" 
        
        self.counter_box = BoxLayout(orientation='horizontal', size_hint_y=0.55)
        self.note_box = BoxLayout(orientation='horizontal', size_hint_y=0.45)
        self.add_widget(self.counter_box)
        self.add_widget(self.note_box)
        self.redraw_ui()
        self.counter_box.bind(pos=self.update_canvas_counter, size=self.update_canvas_counter)

    def update_canvas_counter(self, *args):
        self.counter_box.canvas.before.clear()
        with self.counter_box.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.counter_box.pos, size=self.counter_box.size, radius=[self.counter_box.height/2])
            Color(*MATCHY_GREEN)
            Line(rounded_rectangle=[self.counter_box.pos[0], self.counter_box.pos[1], self.counter_box.size[0], self.counter_box.size[1], self.counter_box.height/2], width=1.2)

    def set_qty(self, value):
        self.qty = value
        if self.qty == 0: self.current_note = "" 
        self.redraw_ui()

    def update_note_text(self, text):
        self.current_note = text
        self.redraw_ui()

    def redraw_ui(self):
        self.counter_box.clear_widgets()
        self.note_box.clear_widgets()
        self.update_canvas_counter()

        if self.qty == 0:
            btn_tambah = Button(text="Tambah", font_size='12sp', bold=True, color=MATCHY_GREEN, background_normal='', background_color=(0,0,0,0))
            btn_tambah.bind(on_press=lambda x: self.callback_change(self.menu_name, 1))
            self.counter_box.add_widget(btn_tambah)
        else:
            btn_minus = Button(text="-", font_size='16sp', bold=True, color=MATCHY_GREEN, size_hint_x=0.3, background_normal='', background_color=(0,0,0,0))
            btn_minus.bind(on_press=lambda x: self.callback_change(self.menu_name, -1))
            lbl_num = Label(text=str(self.qty), font_size='13sp', bold=True, color=CHARCOAL, size_hint_x=0.4)
            btn_plus = Button(text="+", font_size='16sp', bold=True, color=MATCHY_GREEN, size_hint_x=0.3, background_normal='', background_color=(0,0,0,0))
            btn_plus.bind(on_press=lambda x: self.callback_change(self.menu_name, 1))
            self.counter_box.add_widget(btn_minus)
            self.counter_box.add_widget(lbl_num)
            self.counter_box.add_widget(btn_plus)

        if self.qty > 0:
            label_tombol = "Edit Catatan" if self.current_note else "Catatan"
            warna_teks_tombol = MATCHY_GREEN if self.current_note else CHARCOAL_SEC
            
            btn_catatan = Button(text=label_tombol, font_size='10sp', bold=True, color=warna_teks_tombol, background_normal='', background_color=(0,0,0,0))
            btn_catatan.bind(on_press=lambda x: self.callback_note(self.menu_name, self.current_note))
            
            with btn_catatan.canvas.before:
                Color(1, 1, 1, 1)
                self.rect_btn = RoundedRectangle(pos=self.note_box.pos, size=self.note_box.size, radius=[self.note_box.height/2])
                Color(*(MATCHY_GREEN if self.current_note else ABU_GARIS))
                self.line_btn = Line(rounded_rectangle=[self.note_box.pos[0], self.note_box.pos[1], self.note_box.size[0], self.note_box.size[1], self.note_box.height/2], width=1)
            
            def sync_canvas(*args):
                self.rect_btn.pos = self.note_box.pos
                self.rect_btn.size = self.note_box.size
                self.line_btn.rounded_rectangle = [self.note_box.pos[0], self.note_box.pos[1], self.note_box.size[0], self.note_box.size[1], self.note_box.height/2]
            
            self.note_box.bind(pos=sync_canvas, size=sync_canvas)
            self.note_box.add_widget(btn_catatan)

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = Background(orientation='vertical', padding=[25, 40, 25, 40], spacing=20)
        
        self.logo_img = Image(source='korean_food.png', size_hint_y=0.43, fit_mode='contain')
        layout.add_widget(self.logo_img)
        
        text_box = BoxLayout(orientation='vertical', size_hint_y=0.30, spacing=12)
        text_box.add_widget(Label(text='CRASH LANDING\nON FOOD', font_size='28sp', bold=True, color=CHARCOAL, halign='center'))
        text_box.add_widget(Label(text='Korean Restaurant', font_size='18sp', color=PINK_AKSEN, bold=True, halign='center'))
        text_box.add_widget(Label(text='Delicious Korean Food\nMade With Love', font_size='14sp', color=CHARCOAL_SEC, halign='center'))
        layout.add_widget(text_box)
        
        btn_container = BoxLayout(orientation='horizontal', size_hint_y=0.10)
        btn_container.add_widget(Widget(size_hint_x=0.35)) 
        start_btn = Button(text='START ORDERING', size_hint_x=0.30, background_normal='', background_color=PINK_AKSEN, color=PUTIH_MURNI, font_size='16sp', bold=True)
        start_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        btn_container.add_widget(start_btn)
        btn_container.add_widget(Widget(size_hint_x=0.35)) 
        layout.add_widget(btn_container)
        layout.add_widget(Widget(size_hint_y=0.08)) 
        self.add_widget(layout)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = Background(orientation='vertical', padding=[120, 20, 120, 20], spacing=10)
        
        header_box = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        header_box.add_widget(Label(text='Annyeong!', font_size='32sp', bold=True, color=PINK_AKSEN, halign='center'))
        header_box.add_widget(Label(text='Mau makan apa hari ini?', font_size='18sp', color=CHARCOAL, halign='center'))
        layout.add_widget(header_box)
        
        self.img_resto = Image(source='korean_food.png', size_hint_y=0.45, fit_mode='contain')
        layout.add_widget(self.img_resto)
        
        grid = GridLayout(cols=2, rows=2, spacing=15, size_hint_y=0.35)
        menus = [('Pesan Makanan', 'pesan_makanan'), ('Booking Meja', 'booking_meja'), ('Nota Pesanan', 'nota_pesanan'), ('Status Antrean', 'status_antrean')]
        for text, scr in menus:
            btn = Button(text=text, background_normal='', background_color=(0.96, 0.65, 0.71, 0.9), color=PUTIH_MURNI, font_size='16sp', bold=True)
            btn.bind(on_press=lambda instance, s=scr: self.pindah_screen(s))
            grid.add_widget(btn)
        layout.add_widget(grid)
        self.add_widget(layout)

    def pindah_screen(self, screen_name):
        target = self.manager.get_screen(screen_name)
        if hasattr(target, 'refresh_nota'): target.refresh_nota()
        if hasattr(target, 'refresh_tampilan'): target.refresh_tampilan()
        self.manager.current = screen_name

class BookingMejaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.btns_meja = {}
        layout = Background(orientation='vertical', padding=20, spacing=15)
        
        h = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        b = Button(text='KEMBALI', size_hint_x=0.18, background_normal='', background_color=PINK_AKSEN, bold=True, font_size='12sp')
        b.bind(on_press=lambda x: setattr(self.manager, 'current', 'home')) 
        h.add_widget(b)
        h.add_widget(Label(text='STATUS KETERSEDIAAN MEJA', size_hint_x=0.64, bold=True, color=CHARCOAL, halign='center'))
        h.add_widget(Widget(size_hint_x=0.18))
        layout.add_widget(h)
        
        layout.add_widget(Label(text="Peta Meja Restoran:", font_size='14sp', color=CHARCOAL_SEC, size_hint_y=0.06))
        
        grid = GridLayout(cols=3, spacing=12, size_hint_y=0.76) 
        for i in range(1, 13): 
            btn = Button(text=f"Meja {i}", background_normal='', bold=True, halign='center')
            grid.add_widget(btn)
            self.btns_meja[i] = btn
        layout.add_widget(grid)
        layout.add_widget(Widget(size_hint_y=0.10))
        self.add_widget(layout)

    def refresh_tampilan(self):
        for n, nama_pemesan in STATUS_DATABASE_MEJA.items():
            btn = self.btns_meja[n]
            if nama_pemesan: 
                btn.background_color = (0.9, 0.4, 0.4, 1) 
                btn.text = f"Meja {n}\n[{nama_pemesan}]"
                btn.color = PUTIH_MURNI
            else: 
                btn.background_color = PUTIH_MURNI         
                btn.text = f"Meja {n}\n(Kosong)"
                btn.color = CHARCOAL

class PesanMakananScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.daftar_menu = {
            "Ramyeon": {"kategori": "Main Course", "harga": 28000, "gambar_base": "ramyeon"},
            "Kimchi Fried Rice": {"kategori": "Main Course", "harga": 35000, "gambar_base": "kimchi_rice"},
            "Tteokbokki": {"kategori": "Main Course", "harga": 32000, "gambar_base": "tteokbokki"},
            "Rabokki": {"kategori": "Main Course", "harga": 34000, "gambar_base": "rabokki"},
            "Jjajangmyeon": {"kategori": "Main Course", "harga": 42000, "gambar_base": "jjajang"},
            "K-Fried Chicken w/ Rice": {"kategori": "Main Course", "harga": 45000, "gambar_base": "kfc_rice"},
            "French Fries": {"kategori": "Side Dish", "harga": 20000, "gambar_base": "fries"},
            "Mandu (Korean Dumpling)": {"kategori": "Side Dish", "harga": 28000, "gambar_base": "mandu"},
            "Corn Dog Mozzarella": {"kategori": "Side Dish", "harga": 25000, "gambar_base": "corndog"},
            "Bungeoppang": {"kategori": "Dessert", "harga": 18000, "gambar_base": "bungeoppang"},
            "Croffle": {"kategori": "Dessert", "harga": 24000, "gambar_base": "croffle"},
            "Bingsu": {"kategori": "Dessert", "harga": 32000, "gambar_base": "bingsu"},
            "Es Teh Manis": {"kategori": "Minuman", "harga": 8000, "gambar_base": "esteh"},
            "Lemon Tea": {"kategori": "Minuman", "harga": 12000, "gambar_base": "lemontea"},
            "Mineral Water": {"kategori": "Minuman", "harga": 6000, "gambar_base": "water"},
            "Iced Americano": {"kategori": "Minuman", "harga": 20000, "gambar_base": "americano"},
            "Banana Milk": {"kategori": "Minuman", "harga": 24000, "gambar_base": "bananamilk"},
            "Matcha Latte": {"kategori": "Minuman", "harga": 25000, "gambar_base": "matcha"},
            "Korean Strawberry Milk": {"kategori": "Minuman", "harga": 27000, "gambar_base": "strawberry_milk"}
        }
        self.keranjang_jumlah = {m: 0 for m in self.daftar_menu}
        self.keranjang_catatan = {m: "" for m in self.daftar_menu} 
        self.capsule_widgets_dict = {}

        layout = Background(orientation='vertical', padding=15, spacing=8)
        header = BoxLayout(orientation='horizontal', size_hint_y=0.07)
        back = Button(text='KEMBALI', size_hint_x=0.18, background_normal='', background_color=PINK_AKSEN, bold=True, font_size='12sp')
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        title = Label(text='PILIH MENU', size_hint_x=0.64, font_size='20sp', bold=True, color=CHARCOAL, halign='center')
        header.add_widget(back)
        header.add_widget(title)
        header.add_widget(Widget(size_hint_x=0.18))
        layout.add_widget(header)

        layout.add_widget(Label(text="Nama Pemesan:", font_size='13sp', color=CHARCOAL_SEC, size_hint_y=0.03))
        box_n = BoxLayout(orientation='horizontal', size_hint_y=0.06)
        box_n.add_widget(Widget(size_hint_x=0.15))
        self.input_nama = TextInput(multiline=False, size_hint_x=0.7, hint_text="Nama kamu...", halign='center')
        box_n.add_widget(self.input_nama)
        box_n.add_widget(Widget(size_hint_x=0.15))
        layout.add_widget(box_n)

        scroll = ScrollView(size_hint_y=0.55)
        grid_m = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=[0, 5, 0, 15])
        grid_m.bind(minimum_height=grid_m.setter('height'))

        kategori_tercetak = set()
        for m, info in self.daftar_menu.items():
            if info['kategori'] not in kategori_tercetak:
                kategori_tercetak.add(info['kategori'])
                header_kat = Label(text=f"\n[b]{info['kategori']}[/b]", font_size='14sp', color=PINK_AKSEN, markup=True, size_hint_y=None, height=35, halign='left')
                header_kat.bind(size=header_kat.setter('text_size'))
                grid_m.add_widget(header_kat)

            row = MenuDividerRow(orientation='horizontal', size_hint_y=None, height=dp(75)) 
            img_box = BoxLayout(size_hint_x=0.2, padding=[0, 2, 0, 2])
            img_menu = Image(source=cari_gambar_valid(info['gambar_base']), fit_mode='contain')
            img_box.add_widget(img_menu)
            row.add_widget(img_box)
            
            info_b = BoxLayout(orientation='vertical', size_hint_x=0.48)
            info_b.add_widget(Label(text=m, font_size='14sp', bold=True, color=CHARCOAL, halign='left'))
            info_b.add_widget(Label(text=f"Rp {info['harga']:,}", font_size='11sp', color=CHARCOAL_SEC, halign='left'))
            row.add_widget(info_b)
            
            cw = BoxLayout(orientation='vertical', size_hint_x=0.32, padding=[0, 2, 0, 2])
            capsule = CapsuleCounter(menu_name=m, callback_change=self.ubah_qty, callback_note=self.buka_popup_catatan)
            self.capsule_widgets_dict[m] = capsule
            cw.add_widget(capsule)
            row.add_widget(cw)
            grid_m.add_widget(row)

        scroll.add_widget(grid_m)
        layout.add_widget(scroll)

        self.lbl_keranjang = Label(text="Belum ada makanan terpilih.", font_size='14sp', color=CHARCOAL_SEC, size_hint_y=0.12, halign='center')
        layout.add_widget(self.lbl_keranjang)

        b_sub = Button(text='LANJUTKAN PESANAN', size_hint_y=0.07, background_normal='', background_color=MATCHY_GREEN, color=PUTIH_MURNI, font_size='14sp', bold=True)
        b_sub.bind(on_press=self.proses_pilihan_tipe)
        layout.add_widget(b_sub)
        self.add_widget(layout)

    def refresh_tampilan(self):
        self.input_nama.text = ""
        for m in self.keranjang_jumlah:
            self.keranjang_jumlah[m] = 0
            self.keranjang_catatan[m] = ""
            self.capsule_widgets_dict[m].set_qty(0)
        self.hitung_total_keranjang()

    def ubah_qty(self, menu, nilai):
        baru = self.keranjang_jumlah[menu] + nilai
        if baru < 0: return
        self.keranjang_jumlah[menu] = baru
        self.capsule_widgets_dict[menu].set_qty(baru)
        self.hitung_total_keranjang()

    def buka_popup_catatan(self, menu_name, current_note_text):
        content = BoxLayout(orientation='vertical', padding=15, spacing=12)
        content.add_widget(Label(text=f"Catatan khusus untuk {menu_name}:", font_size='14sp', bold=True))
        txt_input = TextInput(text=current_note_text, multiline=True, hint_text="Contoh: Ekstra pedas...", size_hint_y=0.5)
        content.add_widget(txt_input)
        
        btn_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.3)
        btn_batal = Button(text="BATAL", background_normal='', background_color=(0.9, 0.4, 0.4, 1))
        btn_simpan = Button(text="SIMPAN", background_normal='', background_color=MATCHY_GREEN)
        btn_box.add_widget(btn_batal)
        btn_box.add_widget(btn_simpan)
        content.add_widget(btn_box)
        
        popup_note = Popup(title='Tambah Catatan Menu', content=content, size_hint=(0.85, 0.45), auto_dismiss=False)
        btn_batal.bind(on_press=popup_note.dismiss)
        
        def simpan_catatan_internal(instance):
            self.keranjang_catatan[menu_name] = txt_input.text.strip()
            self.capsule_widgets_dict[menu_name].update_note_text(txt_input.text.strip())
            popup_note.dismiss()
            
        btn_simpan.bind(on_press=simpan_catatan_internal)
        popup_note.open()

    def hitung_total_keranjang(self):
        m_list = []
        h_total = 0
        for m, q in self.keranjang_jumlah.items():
            if q > 0:
                m_list.append(m)
                h_total += self.daftar_menu[m]['harga'] * q
        if not m_list:
            self.lbl_keranjang.text = "Belum ada makanan terpilih."
            self.lbl_keranjang.color = CHARCOAL_SEC
        else:
            total_est_menit = sum(WAKTU_MENU_REF.get(m, 2) for m in m_list)
            self.lbl_keranjang.text = f"Total: Rp {h_total:,}\nEstimasi Durasi Masak di Nota: {total_est_menit} Menit"
            self.lbl_keranjang.color = MATCHY_GREEN
    
    def proses_pilihan_tipe(self, instance):
        nama = self.input_nama.text.strip()
        final_m = []
        final_h = 0
        final_notes_dict = {}
        
        for m, q in self.keranjang_jumlah.items():
            if q > 0:
                final_m.extend([m]*q)
                final_h += self.daftar_menu[m]['harga']*q
                if self.keranjang_catatan[m]:
                    final_notes_dict[m] = self.keranjang_catatan[m]
                    
        if not nama or not final_m:
            self.lbl_keranjang.text = "Lengkapi nama dan menu!"
            self.lbl_keranjang.color = (0.9, 0.2, 0.2, 1)
            return

        global KERANJANG_SEMENTARA
        KERANJANG_SEMENTARA = {
            "nama_panggilan": nama, "nama": "", "makanan": final_m,
            "catatan_per_menu": final_notes_dict, "total_harga": final_h, "jam_datang": ""
        }

        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        content.add_widget(Label(text="KONFIRMASI DETAIL PESANAN", font_size='15sp', bold=True, color=PINK_AKSEN))
        
        scroll_review = ScrollView()
        review_grid = GridLayout(cols=1, spacing=4, size_hint_y=None)
        review_grid.bind(minimum_height=review_grid.setter('height'))
        
        counts = {}
        for item_m in final_m: counts[item_m] = counts.get(item_m, 0) + 1
        for menu_nama, qty in counts.items():
            lbl_item = Label(text=f"• {menu_nama} (x{qty})", font_size='12sp', size_hint_y=None, height=30)
            review_grid.add_widget(lbl_item)
            
        scroll_review.add_widget(review_grid)
        content.add_widget(scroll_review)
        
        btn_box = BoxLayout(orientation='horizontal', spacing=12, size_hint_y=0.2)
        btn_dine = Button(text="DINE IN", background_normal='', background_color=PINK_AKSEN, bold=True)
        btn_take = Button(text="TAKE AWAY", background_normal='', background_color=(0.55, 0.72, 0.85, 1), bold=True)
        btn_batal = Button(text="BATAL", background_normal='', background_color=(0.4, 0.4, 0.4, 1), bold=True)
        
        btn_box.add_widget(btn_dine)
        btn_box.add_widget(btn_take)
        btn_box.add_widget(btn_batal)
        content.add_widget(btn_box)
        
        popup_tipe = Popup(title='Metode Penyajian', content=content, size_hint=(0.88, 0.6), auto_dismiss=False)
        btn_dine.bind(on_press=lambda x: self.eksekusi_dine_in(popup_tipe, nama))
        btn_take.bind(on_press=lambda x: self.eksekusi_take_away(popup_tipe, nama))
        btn_batal.bind(on_press=popup_tipe.dismiss)
        popup_tipe.open()

    def eksekusi_dine_in(self, popup, nama):
        popup.dismiss()
        content_meja = BoxLayout(orientation='vertical', padding=15, spacing=10)
        content_meja.add_widget(Label(text="PILIH NOMOR MEJA KOSONG", font_size='16sp', bold=True, color=PINK_AKSEN, size_hint_y=0.15))
        
        grid_meja = GridLayout(cols=3, spacing=8, size_hint_y=0.65)
        self.meja_terpilih_popup = None
        list_tombol_meja = {}
        
        def pilih_meja_internal(instance, nomor_meja):
            if STATUS_DATABASE_MEJA[nomor_meja]: return
            for n_meja, btn_meja in list_tombol_meja.items():
                btn_meja.background_color = (0.9, 0.4, 0.4, 1) if STATUS_DATABASE_MEJA[n_meja] else PUTIH_MURNI
                btn_meja.color = PUTIH_MURNI if STATUS_DATABASE_MEJA[n_meja] else CHARCOAL
            instance.background_color = PINK_AKSEN
            instance.color = PUTIH_MURNI
            self.meja_terpilih_popup = nomor_meja

        for i in range(1, 13):
            nama_terisi = STATUS_DATABASE_MEJA.get(i, None)
            btn = Button(text=f"M {i}\n[{nama_terisi}]" if nama_terisi else f"Meja {i}\n(Kosong)", background_normal='', bold=True, halign='center')
            btn.background_color = (0.9, 0.4, 0.4, 1) if nama_terisi else PUTIH_MURNI
            btn.color = PUTIH_MURNI if nama_terisi else CHARCOAL
            btn.bind(on_press=lambda inst, n=i: pilih_meja_internal(inst, n))
            grid_meja.add_widget(btn)
            list_tombol_meja[i] = btn
            
        content_meja.add_widget(grid_meja)
        
        btn_action_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        btn_batal_meja = Button(text="KEMBALI", background_normal='', background_color=(0.4, 0.4, 0.4, 1), bold=True)
        btn_proses_meja = Button(text="PROSES NOTA", background_normal='', background_color=MATCHY_GREEN, bold=True)
        btn_action_box.add_widget(btn_batal_meja)
        btn_action_box.add_widget(btn_proses_meja)
        content_meja.add_widget(btn_action_box)
        
        popup_meja = Popup(title='Validasi Meja Dine In', content=content_meja, size_hint=(0.9, 0.65), auto_dismiss=False)
        btn_batal_meja.bind(on_press=popup_meja.dismiss)
        
        def simpan_booking_langsung(instance):
            global KERANJANG_SEMENTARA, RIWAYAT_NOTA
            nomor_meja_final = getattr(self, 'meja_terpilih_popup', None)
            if not nomor_meja_final: 
                return
                
            waktu_sekarang = datetime.now()
            total_est_menit = sum(WAKTU_MENU_REF.get(m, 2) for m in KERANJANG_SEMENTARA["makanan"])
            waktu_siap_logis = waktu_sekarang + timedelta(minutes=total_est_menit)
            
            STATUS_DATABASE_MEJA[nomor_meja_final] = nama
            KERANJANG_SEMENTARA["nama"] = f"{nama} (Meja {nomor_meja_final})"
            KERANJANG_SEMENTARA["jam_datang"] = waktu_sekarang.strftime("%H:%M:%S")
            
            counts = {}
            for item_m in KERANJANG_SEMENTARA["makanan"]: counts[item_m] = counts.get(item_m, 0) + 1
            teks_rincian = "".join([f"   • {m_nama} (x{qty})\n" for m_nama, qty in counts.items()])
                
            nota_teks_baru = (
                f"============ NOTA DIGITAL ============\n"
                f"Pelanggan : {nama}\n"
                f"Metode    : DINE IN (Meja {nomor_meja_final})\n"
                f"Jam Masuk : {KERANJANG_SEMENTARA['jam_datang']} WIB\n"
                f"Est. Siap : {waktu_siap_logis.strftime('%H:%M:%S')} WIB ({total_est_menit} mnt)\n"
                f"--------------------------------------\n"
                f"Pesanan:\n{teks_rincian}"
                f"--------------------------------------\n"
                f"TOTAL     : Rp {KERANJANG_SEMENTARA['total_harga']:,}\n"
                f"Status    : LUNAS (Aplikasi)\n"
                f"======================================"
            )
            RIWAYAT_NOTA.append(nota_teks_baru)
            ANTREAN_RESTORAN.put(KERANJANG_SEMENTARA)
            KERANJANG_SEMENTARA = None
            
            popup_meja.dismiss()
            self.refresh_tampilan()
            self.manager.get_screen('nota_pesanan').refresh_nota()
            self.manager.current = 'nota_pesanan'
            
        btn_proses_meja.bind(on_press=simpan_booking_langsung)
        popup_meja.open()

    def eksekusi_take_away(self, popup, nama):
        global KERANJANG_SEMENTARA, RIWAYAT_NOTA
        popup.dismiss()
        waktu_sekarang = datetime.now()
        total_est_menit = sum(WAKTU_MENU_REF.get(m, 2) for m in KERANJANG_SEMENTARA["makanan"])
        waktu_siap_logis = waktu_sekarang + timedelta(minutes=total_est_menit)
        
        KERANJANG_SEMENTARA["nama"] = f"{nama} (Take Away)"
        KERANJANG_SEMENTARA["jam_datang"] = waktu_sekarang.strftime("%H:%M:%S")
        
        counts = {}
        for item_m in KERANJANG_SEMENTARA["makanan"]: counts[item_m] = counts.get(item_m, 0) + 1
        teks_rincian = "".join([f"   • {m_nama} (x{qty})\n" for m_nama, qty in counts.items()])
            
        nota_teks_baru = (
            f"============ NOTA DIGITAL ============\n"
            f"Pelanggan : {nama}\n"
            f"Metode    : TAKE AWAY\n"
            f"Jam Masuk : {KERANJANG_SEMENTARA['jam_datang']} WIB\n"
            f"Est. Siap : {waktu_siap_logis.strftime('%H:%M:%S')} WIB ({total_est_menit} mnt)\n"
            f"--------------------------------------\n"
            f"Pesanan:\n{teks_rincian}"
            f"--------------------------------------\n"
            f"TOTAL     : Rp {KERANJANG_SEMENTARA['total_harga']:,}\n"
            f"Status    : LUNAS (Aplikasi)\n"
            f"======================================"
        )
        RIWAYAT_NOTA.append(nota_teks_baru)
        ANTREAN_RESTORAN.put(KERANJANG_SEMENTARA)
        KERANJANG_SEMENTARA = None
        
        self.refresh_tampilan()
        self.manager.get_screen('nota_pesanan').refresh_nota()
        self.manager.current = 'nota_pesanan'

class NotaPesananScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = Background(orientation='vertical', padding=15, spacing=10)
        
        h = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        b = Button(text='KEMBALI', size_hint_x=0.18, background_normal='', background_color=PINK_AKSEN, bold=True, font_size='12sp')
        b.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        h.add_widget(b)
        h.add_widget(Label(text='DAFTAR NOTA DIGITAL', size_hint_x=0.64, bold=True, color=CHARCOAL))
        h.add_widget(Widget(size_hint_x=0.18))
        layout.add_widget(h)
        
        self.scroll = ScrollView(size_hint_y=0.92)
        self.grid_nota = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=10)
        self.grid_nota.bind(minimum_height=self.grid_nota.setter('height'))
        self.scroll.add_widget(self.grid_nota)
        layout.add_widget(self.scroll)
        self.add_widget(layout)

    def refresh_nota(self):
        self.grid_nota.clear_widgets()
        if not RIWAYAT_NOTA:
            self.grid_nota.add_widget(Label(text="Belum ada transaksi.", font_size='14sp', color=CHARCOAL_SEC, size_hint_y=None, height=100))
            return
            
        for nota_string in reversed(RIWAYAT_NOTA):
            box_nota_wrapper = BoxLayout(orientation='vertical', size_hint_y=None, height=270, padding=10)
            
            def sync_nota_canvas(instance, *args):
                instance.canvas.before.clear()
                with instance.canvas.before:
                    Color(*PUTIH_MURNI)
                    RoundedRectangle(pos=instance.pos, size=instance.size, radius=[8])
                    Color(*ABU_GARIS)
                    Line(rounded_rectangle=[instance.pos[0], instance.pos[1], instance.size[0], instance.size[1], 8], width=1)
            
            box_nota_wrapper.bind(pos=sync_nota_canvas, size=sync_nota_canvas)
            
            lbl_isi_nota = Label(text=nota_string, font_name="Roboto", font_size='11.5sp', color=CHARCOAL, halign='left', valign='top')
            lbl_isi_nota.bind(size=lbl_isi_nota.setter('text_size'))
            box_nota_wrapper.add_widget(lbl_isi_nota)
            self.grid_nota.add_widget(box_nota_wrapper)

class StatusAntreanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = Background(orientation='vertical', padding=15, spacing=10)
        
        h = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        b = Button(text='KEMBALI', size_hint_x=0.18, background_normal='', background_color=PINK_AKSEN, bold=True, font_size='12sp')
        b.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        h.add_widget(b)
        h.add_widget(Label(text='URUTAN ANTREAN MONITORING', size_hint_x=0.64, bold=True, color=CHARCOAL))
        h.add_widget(Widget(size_hint_x=0.18))
        layout.add_widget(h)
        
        self.lbl_status_top = Label(text="SISTEM MONITORING DAPUR (OTOMATIS)", size_hint_y=0.06, bold=True, color=MATCHY_GREEN, font_size='14sp')
        layout.add_widget(self.lbl_status_top)
        
        self.scroll = ScrollView(size_hint_y=0.86)
        self.grid_antrean = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=5)
        self.grid_antrean.bind(minimum_height=self.grid_antrean.setter('height'))
        self.scroll.add_widget(self.grid_antrean)
        layout.add_widget(self.scroll)
        self.add_widget(layout)

    def refresh_tampilan(self):
        self.grid_antrean.clear_widgets()
        temp_list = list(ANTREAN_RESTORAN.queue)
        waktu_sekarang = datetime.now()
        
        if not temp_list:
            self.lbl_status_top.text = "SEMUA ANTREAN SELESAI DIPROSES"
            self.lbl_status_top.color = CHARCOAL_SEC
            self.grid_antrean.add_widget(Label(text="Tidak ada antrean yang aktif saat ini.", font_size='14sp', color=CHARCOAL_SEC, size_hint_y=None, height=100))
            return
            
        self.lbl_status_top.text = f"DAPUR SEDANG MEMASAK ANTREAN NO. 1 ({temp_list[0]['nama_panggilan']})"
        self.lbl_status_top.color = PINK_AKSEN

        for urutan, data in enumerate(temp_list, start=1):
            if urutan == 1 and WAKTU_MULAI_AKTIF is not None:
                selisih = (waktu_sekarang - WAKTU_MULAI_AKTIF).total_seconds()
                sisa_detik = max(0, DURASI_PROSES_DAPUR - int(selisih))  
                label_status = "SEDANG DIMASAK"
            else:
                sisa_detik = DURASI_PROSES_DAPUR  
                label_status = "DIANTREKAN"

            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=65, padding=8)
            warna_teks = PUTIH_MURNI if urutan == 1 else CHARCOAL
            warna_sub = PUTIH_MURNI if urutan == 1 else CHARCOAL_SEC
            pilihan_warna_bg = MATCHY_GREEN if urutan == 1 else PUTIH_MURNI
            
            def buat_render_callback(warna_tetap):
                return lambda instance, *args: self.gambar_ulang_background_row(instance, warna_tetap)
            
            callback_fungsi = buat_render_callback(pilihan_warna_bg)
            row.bind(pos=callback_fungsi, size=callback_fungsi)
            
            info_b = BoxLayout(orientation='vertical', size_hint_x=0.65)
            info_b.add_widget(Label(text=f"No. {urutan} - {data['nama']}", font_size='13sp', bold=True, color=warna_teks, halign='left'))
            info_b.add_widget(Label(text=f"Menu: {', '.join(data['makanan'])}", font_size='11sp', color=warna_sub, halign='left'))
            row.add_widget(info_b)
            
            waktu_b = BoxLayout(orientation='vertical', size_hint_x=0.35)
            waktu_b.add_widget(Label(text=label_status, font_size='11sp', bold=True, color=warna_teks, halign='right'))
            waktu_b.add_widget(Label(text=f"Sisa: {sisa_detik}s" if urutan == 1 else f"Durasi: {sisa_detik}s", font_size='11sp', color=warna_sub, halign='right'))
            row.add_widget(waktu_b)
            
            self.grid_antrean.add_widget(row)

    def gambar_ulang_background_row(self, instance, warna_fix):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*warna_fix)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[6])
            Color(*ABU_GARIS)
            Line(rounded_rectangle=[instance.pos[0], instance.pos[1], instance.size[0], instance.size[1], 6], width=1)

class RestoranApp(App):
    def build(self):
        self.title = "Crash Landing on Food"
        self.sm = ScreenManager()
        self.sm.add_widget(SplashScreen(name='splash'))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(BookingMejaScreen(name='booking_meja'))
        self.sm.add_widget(PesanMakananScreen(name='pesan_makanan'))
        self.sm.add_widget(NotaPesananScreen(name='nota_pesanan'))
        self.sm.add_widget(StatusAntreanScreen(name='status_antrean'))
        
        Clock.schedule_interval(self.mesin_waktu_dapur_global, 1.0)
        return self.sm

    def mesin_waktu_dapur_global(self, dt):
        global WAKTU_MULAI_AKTIF, STATUS_DATABASE_MEJA
        
        if not ANTREAN_RESTORAN.empty():
            waktu_sekarang = datetime.now()
            if WAKTU_MULAI_AKTIF is None:
                WAKTU_MULAI_AKTIF = waktu_sekarang
                
            selisih = (waktu_sekarang - WAKTU_MULAI_AKTIF).total_seconds()
            sisa_waktu = max(0, DURASI_PROSES_DAPUR - int(selisih))
            
            if sisa_waktu <= 0:
                pesanan_selesai = ANTREAN_RESTORAN.get()
                WAKTU_MULAI_AKTIF = datetime.now() 
                
                if "(Meja " in pesanan_selesai["nama"]:
                    try:
                        no_meja = int(pesanan_selesai["nama"].split("(Meja ")[1].replace(")", ""))
                        STATUS_DATABASE_MEJA[no_meja] = None
                    except:
                        pass
                        
        if self.sm.current == 'status_antrean':
            self.sm.get_screen('status_antrean').refresh_tampilan()

if __name__ == '__main__':
    RestoranApp().run()