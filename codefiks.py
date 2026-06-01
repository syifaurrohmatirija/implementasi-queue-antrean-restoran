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

# ======================
# DATABASE GLOBAL RESTORAN
# ======================
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

def cari_gambar_valid(nama_base):
    ekstensi_dicoba = ['.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG']
    for ext in ekstensi_dicoba:
        nama_file_lengkap = nama_base + ext
        if os.path.exists(nama_file_lengkap):
            return nama_file_lengkap
    return ""  

# ======================
# KOMPONEN WIDGET UTAMA
# ======================
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
        if self.qty == 0:
            self.current_note = "" 
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

# ======================
# SCREEN: SPLASH SCREEN
# ======================
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = Background(orientation='vertical', padding=[25, 40, 25, 40], spacing=20)
       
        self.logo_img = Image(source='korean_food.png', size_hint_y=0.43, allow_stretch=True, keep_ratio=True)
        layout.add_widget(self.logo_img)
        
        text_box = BoxLayout(orientation='vertical', size_hint_y=0.30, spacing=12)
        text_box.add_widget(Label(text='CRASH LANDING\nON FOOD', font_size='28sp', bold=True, color=CHARCOAL, halign='center'))
        text_box.add_widget(Label(text='Korean Restaurant', font_size='18sp', color=PINK_AKSEN, bold=True, halign='center'))
        text_box.add_widget(Label(text='Delicious Korean Food\nMade With Love', font_size='14sp', color=CHARCOAL_SEC, halign='center'))
        layout.add_widget(text_box)
        
        btn_container = BoxLayout(orientation='horizontal', size_hint_y=0.10)
        btn_container.add_widget(Widget(size_hint_x=0.35)) 
        
        start_btn = Button(
            text='START ORDERING', 
            size_hint_x=0.30, 
            background_normal='', 
            background_color=PINK_AKSEN, 
            color=PUTIH_MURNI, 
            font_size='16sp', 
            bold=True
        )
        start_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        
        btn_container.add_widget(start_btn)
        btn_container.add_widget(Widget(size_hint_x=0.35)) 
        layout.add_widget(btn_container)
        layout.add_widget(Widget(size_hint_y=0.08)) 
        self.add_widget(layout)

# ======================
# SCREEN: HOME SCREEN
# ======================
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = Background(orientation='vertical', padding=[120, 20, 120, 20], spacing=10)
        
        header_box = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        header_box.add_widget(Label(text='Annyeong!', font_size='32sp', bold=True, color=PINK_AKSEN, halign='center'))
        header_box.add_widget(Label(text='Mau makan apa hari ini?', font_size='18sp', color=CHARCOAL, halign='center'))
        layout.add_widget(header_box)
        
        self.img_resto = Image(source='korean_food.png', size_hint_y=0.45, allow_stretch=True, keep_ratio=True)
        layout.add_widget(self.img_resto)
        
        grid = GridLayout(cols=2, rows=2, spacing=15, size_hint_y=0.35)
        menus = [('Pesan Makanan', 'pesan_makanan'), ('Booking Meja', 'booking_meja'), ('Nota Pesanan', 'nota_pesanan'), ('Status Antrean', 'status_antrean')]
        for text, scr in menus:
            btn = Button(
                text=text, 
                background_normal='', 
                background_color=(0.96, 0.65, 0.71, 0.9), 
                color=PUTIH_MURNI, 
                font_size='16sp', 
                bold=True
            )
            btn.bind(on_press=lambda instance, s=scr: self.pindah_screen(s))
            grid.add_widget(btn)
        layout.add_widget(grid)
        self.add_widget(layout)

    def pindah_screen(self, screen_name):
        target = self.manager.get_screen(screen_name)
        if hasattr(target, 'refresh_nota'): 
            target.refresh_nota()
        elif hasattr(target, 'refresh_tampilan'):
            target.refresh_tampilan()
        self.manager.current = screen_name

# ======================
# SCREEN: PESAN MAKANAN
# ======================
class PesanMakananScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.daftar_menu = {
            "Ramyeon": {"kategori": "Main Course", "waktu": 5, "harga": 28000, "gambar_base": "ramyeon"},
            "Kimchi Fried Rice": {"kategori": "Main Course", "waktu": 5, "harga": 35000, "gambar_base": "kimchi_rice"},
            "Tteokbokki": {"kategori": "Main Course", "waktu": 6, "harga": 32000, "gambar_base": "tteokbokki"},
            "Rabokki": {"kategori": "Main Course", "waktu": 6, "harga": 34000, "gambar_base": "rabokki"},
            "Jjajangmyeon": {"kategori": "Main Course", "waktu": 7, "harga": 42000, "gambar_base": "jjajang"},
            "K-Fried Chicken w/ Rice": {"kategori": "Main Course", "waktu": 9, "harga": 45000, "gambar_base": "kfc_rice"},
            
            "French Fries": {"kategori": "Side Dish", "waktu": 3, "harga": 20000, "gambar_base": "fries"},
            "Mandu (Korean Dumpling)": {"kategori": "Side Dish", "waktu": 5, "harga": 28000, "gambar_base": "mandu"},
            "Corn Dog Mozzarella": {"kategori": "Side Dish", "waktu": 6, "harga": 25000, "gambar_base": "corndog"},
            
            "Bungeoppang": {"kategori": "Dessert", "waktu": 5, "harga": 18000, "gambar_base": "bungeoppang"},
            "Croffle": {"kategori": "Dessert", "waktu": 5, "harga": 24000, "gambar_base": "croffle"},
            "Bingsu": {"kategori": "Dessert", "waktu": 6, "harga": 32000, "gambar_base": "bingsu"},
            
            "Es Teh Manis": {"kategori": "Minuman", "waktu": 2, "harga": 8000, "gambar_base": "esteh"},
            "Lemon Tea": {"kategori": "Minuman", "waktu": 2, "harga": 12000, "gambar_base": "lemontea"},
            "Mineral Water": {"kategori": "Minuman", "waktu": 1, "harga": 6000, "gambar_base": "water"},
            "Iced Americano": {"kategori": "Minuman", "waktu": 2, "harga": 20000, "gambar_base": "americano"},
            "Banana Milk": {"kategori": "Minuman", "waktu": 2, "harga": 24000, "gambar_base": "bananamilk"},
            "Matcha Latte": {"kategori": "Minuman", "waktu": 3, "harga": 25000, "gambar_base": "matcha"},
            "Korean Strawberry Milk": {"kategori": "Minuman", "waktu": 3, "harga": 27000, "gambar_base": "strawberry_milk"}
        }
        self.keranjang_jumlah = {m: 0 for m in self.daftar_menu}
        self.keranjang_catatan = {m: "" for m in self.daftar_menu} 
        self.capsule_widgets_dict = {}

        layout = Background(orientation='vertical', padding=15, spacing=8)

        header = BoxLayout(orientation='horizontal', size_hint_y=0.07)
        back = Button(text='KEMBALI', size_hint_x=0.18, background_normal='', background_color=PINK_AKSEN, bold=True, font_size='12sp')
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        title = Label(text='PILIH MENU', size_hint_x=0.64, font_size='20sp', bold=True, color=CHARCOAL, halign='center', valign='middle')
        title.bind(size=title.setter('text_size'))
        header.add_widget(back); header.add_widget(title); header.add_widget(Widget(size_hint_x=0.18))
        layout.add_widget(header)

        layout.add_widget(Label(text="Nama Pemesan:", font_size='13sp', color=CHARCOAL_SEC, size_hint_y=0.03))
        box_n = BoxLayout(orientation='horizontal', size_hint_y=0.06)
        box_n.add_widget(Widget(size_hint_x=0.15))
        self.input_nama = TextInput(multiline=False, size_hint_x=0.7, hint_text="Nama kamu...", halign='center', background_color=PUTIH_MURNI)
        box_n.add_widget(self.input_nama); box_n.add_widget(Widget(size_hint_x=0.15))
        layout.add_widget(box_n)

        layout.add_widget(Label(text="Daftar Menu Korea Terpopuler:", font_size='13sp', color=CHARCOAL_SEC, size_hint_y=0.03))
        scroll = ScrollView(size_hint_y=0.52)
        grid_m = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=[0, 5, 0, 15])
        grid_m.bind(minimum_height=grid_m.setter('height'))

        kategori_tercetak = set()
        for m, info in self.daftar_menu.items():
            if info['kategori'] not in kategori_tercetak:
                kategori_tercetak.add(info['kategori'])
                header_kat = Label(
                    text=f"\n[b]{info['kategori']}[/b]", 
                    font_size='14sp', 
                    color=PINK_AKSEN, 
                    markup=True,
                    size_hint_y=None, 
                    height=35,
                    halign='left'
                )
                header_kat.bind(size=header_kat.setter('text_size'))
                grid_m.add_widget(header_kat)

            row = MenuDividerRow(orientation='horizontal', size_hint_y=None, height=dp(75)) 

            img_box = BoxLayout(size_hint_x=0.2, padding=[0, 2, 0, 2])
            file_gambar_ditemukan = cari_gambar_valid(info['gambar_base'])
            img_menu = Image(source=file_gambar_ditemukan)
            img_box.add_widget(img_menu)
            row.add_widget(img_box)
            
            info_b = BoxLayout(orientation='vertical', size_hint_x=0.48)
            info_b.add_widget(Label(text=m, font_size='14sp', bold=True, color=CHARCOAL, halign='left', valign='bottom'))
            info_b.add_widget(Label(text=f"Rp {info['harga']:,}\n{info['waktu']} mnt", font_size='11sp', color=CHARCOAL_SEC, halign='left', valign='top'))
            row.add_widget(info_b)
            
            cw = BoxLayout(orientation='vertical', size_hint_x=0.32, padding=[0, 2, 0, 2])
            capsule = CapsuleCounter(menu_name=m, callback_change=self.ubah_qty, callback_note=self.buka_popup_catatan)
            self.capsule_widgets_dict[m] = capsule
            cw.add_widget(capsule)
            row.add_widget(cw)
            
            grid_m.add_widget(row)

        scroll.add_widget(grid_m); layout.add_widget(scroll)

        self.lbl_keranjang = Label(text="Belum ada makanan terpilih.", font_size='14sp', color=CHARCOAL_SEC, size_hint_y=0.15, halign='center', valign='middle')
        self.lbl_keranjang.bind(size=self.lbl_keranjang.setter('text_size'))
        layout.add_widget(self.lbl_keranjang)

        bot = BoxLayout(orientation='horizontal', size_hint_y=0.07, spacing=10)
        b_sub = Button(text='LANJUTKAN PESANAN', background_normal='', background_color=MATCHY_GREEN, color=PUTIH_MURNI, font_size='14sp', bold=True)
        b_sub.bind(on_press=self.proses_pilihan_tipe)
        b_not = Button(text='LIHAT NOTA', background_normal='', background_color=(0.55, 0.72, 0.85, 1), color=PUTIH_MURNI, font_size='14sp', bold=True)
        b_not.bind(on_press=self.pindah_ke_halaman_nota)
        bot.add_widget(b_sub); bot.add_widget(b_not); layout.add_widget(bot)
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
        content.add_widget(Label(text=f"Catatan khusus untuk {menu_name}:", font_size='14sp', bold=True, color=PUTIH_MURNI))
        
        txt_input = TextInput(text=current_note_text, multiline=True, hint_text="Contoh: Ekstra pedas...", size_hint_y=0.5)
        content.add_widget(txt_input)
        
        btn_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.3)
        btn_batal = Button(text="BATAL", background_normal='', background_color=(0.9, 0.4, 0.4, 1), bold=True)
        btn_simpan = Button(text="SIMPAN", background_normal='', background_color=MATCHY_GREEN, bold=True)
        btn_box.add_widget(btn_batal); btn_box.add_widget(btn_simpan); content.add_widget(btn_box)
        
        popup_note = Popup(title='Tambah Catatan Menu', content=content, size_hint=(0.85, 0.45), auto_dismiss=False)
        btn_batal.bind(on_press=popup_note.dismiss)
        
        def simpan_catatan_internal(instance):
            catatan_user = txt_input.text.strip()
            self.keranjang_catatan[menu_name] = catatan_user
            self.capsule_widgets_dict[menu_name].update_note_text(catatan_user)
            popup_note.dismiss()
            
        btn_simpan.bind(on_press=simpan_catatan_internal)
        popup_note.open()

    def hitung_total_keranjang(self):
        m_list = []; w_total = 0; h_total = 0
        for m, q in self.keranjang_jumlah.items():
            if q > 0:
                m_list.append(f"{m} (x{q})")
                w_total += self.daftar_menu[m]['waktu'] * q
                h_total += self.daftar_menu[m]['harga'] * q
        if not m_list:
            self.lbl_keranjang.text = "Belum ada makanan terpilih."
            self.lbl_keranjang.color = CHARCOAL_SEC
        else:
            self.lbl_keranjang.text = f"Total: Rp {h_total:,}\nEstimasi Masak: {w_total} Menit"
            self.lbl_keranjang.color = MATCHY_GREEN

    # --- POPUP PILIHAN DINE IN / TAKE AWAY ---
    
    def proses_pilihan_tipe(self, instance):
        nama = self.input_nama.text.strip()
        final_m = []; final_w = 0; final_h = 0
        final_notes_dict = {}
        
        for m, q in self.keranjang_jumlah.items():
            if q > 0:
                final_m.extend([m]*q)
                final_w += self.daftar_menu[m]['waktu']*q
                final_h += self.daftar_menu[m]['harga']*q
                if self.keranjang_catatan[m]:
                    final_notes_dict[m] = self.keranjang_catatan[m]
                    
        if not nama or not final_m:
            self.lbl_keranjang.text = "Lengkapi nama dan menu!"; self.lbl_keranjang.color = (0.9, 0.2, 0.2, 1)
            return

        global KERANJANG_SEMENTARA
        KERANJANG_SEMENTARA = {
            "nama_panggilan": nama, 
            "nama": "",            
            "makanan": final_m,
            "catatan_per_menu": final_notes_dict,
            "estimasi": final_w,          
            "total_harga": final_h,
            "jam_datang": "", 
            "jam_siap": ""    
        }

        # --- MEMBUAT POPUP RINGKASAN & KONFIRMASI PESANAN ---
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        content.add_widget(Label(text="KONFIRMASI DETAIL PESANAN", font_size='15sp', bold=True, color=PINK_AKSEN, size_hint_y=0.1))
        content.add_widget(Label(text=f"Nama Pelanggan: {nama}", font_size='13sp', color=PUTIH_MURNI, halign='left', size_hint_y=0.08))
        
        scroll_review = ScrollView(size_hint_y=0.5)
        review_grid = GridLayout(cols=1, spacing=4, size_hint_y=None)
        review_grid.bind(minimum_height=review_grid.setter('height'))
        
        counts = {}
        for item_m in final_m:
            counts[item_m] = counts.get(item_m, 0) + 1
            
        for menu_nama, qty in counts.items():
            text_item = f"• {menu_nama} (x{qty}) - Rp {self.daftar_menu[menu_nama]['harga']*qty:,}"
            if menu_nama in final_notes_dict:
                text_item += f"\n  [Req: {final_notes_dict[menu_nama]}]"
            
            lbl_item = Label(text=text_item, font_size='12sp', color=(0.9, 0.9, 0.9, 1), halign='left', size_hint_y=None, height=40)
            lbl_item.bind(size=lbl_item.setter('text_size'))
            review_grid.add_widget(lbl_item)
            
        scroll_review.add_widget(review_grid)
        content.add_widget(scroll_review)
        
        # Informasi Total Ringkasan
        content.add_widget(Label(text=f"Total Bayar: Rp {final_h:,}  |  Estimasi: {final_w} Menit", font_size='13sp', bold=True, color=PUTIH_MURNI, size_hint_y=0.08))
        
        # Pertanyaan Metode Penyajian
        content.add_widget(Label(text="Pilih Metode Penyajian untuk Memproses:", font_size='12sp', color=(0.8, 0.8, 0.8, 1), size_hint_y=0.06))
        
        # Tombol Eksekusi di Bagian Bawah Popup
        btn_box = BoxLayout(orientation='horizontal', spacing=12, size_hint_y=0.18)
        btn_dine = Button(text="DINE IN\n(Makan Sini)", background_normal='', background_color=PINK_AKSEN, bold=True, halign='center', font_size='12sp')
        btn_take = Button(text="TAKE AWAY\n(Bawa Pulang)", background_normal='', background_color=(0.55, 0.72, 0.85, 1), bold=True, halign='center', font_size='12sp')
        btn_batal = Button(text="BATAL", background_normal='', background_color=(0.4, 0.4, 0.4, 1), bold=True, font_size='12sp')
        
        btn_box.add_widget(btn_dine)
        btn_box.add_widget(btn_take)
        btn_box.add_widget(btn_batal)
        content.add_widget(btn_box)
        
        popup_tipe = Popup(title='Konfirmasi & Metode Penyajian', content=content, size_hint=(0.88, 0.65), auto_dismiss=False)
        # Pemicu Event Tombol Popup
        btn_dine.bind(on_press=lambda x: self.eksekusi_dine_in(popup_tipe, nama))
        btn_take.bind(on_press=lambda x: self.eksekusi_take_away(popup_tipe, nama))
        btn_batal.bind(on_press=popup_tipe.dismiss)
        
        popup_tipe.open()

    def eksekusi_dine_in(self, popup, nama):
        popup.dismiss()
        self.manager.get_screen('booking_meja').in_nama.text = nama
        self.manager.get_screen('booking_meja').refresh_tampilan()
        self.manager.current = 'booking_meja'

    def eksekusi_take_away(self, popup, nama):
        global KERANJANG_SEMENTARA
        popup.dismiss()
        
        waktu_sekarang = datetime.now()
        waktu_siap = waktu_sekarang + timedelta(minutes=KERANJANG_SEMENTARA["estimasi"])
        
        KERANJANG_SEMENTARA["nama"] = f"{nama} (Take Away)"
        KERANJANG_SEMENTARA["jam_datang"] = waktu_sekarang.strftime("%H:%M:%S")
        KERANJANG_SEMENTARA["jam_siap"] = waktu_siap.strftime("%H:%M:%S")
        
        ANTREAN_RESTORAN.put(KERANJANG_SEMENTARA)
        RIWAYAT_NOTA.append(KERANJANG_SEMENTARA)
        
        KERANJANG_SEMENTARA = None
        self.refresh_tampilan()
        
        self.manager.get_screen('nota_pesanan').refresh_nota()
        self.manager.current = 'nota_pesanan'

    def pindah_ke_halaman_nota(self, instance):
        self.manager.get_screen('nota_pesanan').refresh_nota()
        self.manager.current = 'nota_pesanan'


# ==========================================
# SCREEN: BOOKING MEJA
# ==========================================
class BookingMejaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meja_terpilih = None; self.btns_meja = {}
        layout = Background(orientation='vertical', padding=20, spacing=15)
        
        h = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        b = Button(text='KEMBALI', size_hint_x=0.18, background_normal='', background_color=PINK_AKSEN, bold=True, font_size='12sp')
        b.bind(on_press=lambda x: setattr(self.manager, 'current', 'pesan_makanan')) 
        h.add_widget(b); h.add_widget(Label(text='PILIH MEJA RESTORAN (DINE IN)', size_hint_x=0.64, bold=True, color=CHARCOAL, halign='center')); h.add_widget(Widget(size_hint_x=0.18))
        layout.add_widget(h)
        
        layout.add_widget(Label(text="Nama Pemesan / Atas Nama:", font_size='13sp', color=CHARCOAL_SEC, size_hint_y=0.05))
        bn = BoxLayout(orientation='horizontal', size_hint_y=0.07)
        bn.add_widget(Widget(size_hint_x=0.15))
        self.in_nama = TextInput(multiline=False, size_hint_x=0.7, hint_text="Ketik nama panggilan...", halign='center')
        bn.add_widget(self.in_nama); bn.add_widget(Widget(size_hint_x=0.15)); layout.add_widget(bn)
        
        layout.add_widget(Label(text="Peta Meja (Merah=Terisi, Putih=Kosong):", font_size='13sp', color=CHARCOAL_SEC, size_hint_y=0.05))
        grid = GridLayout(cols=3, spacing=10, size_hint_y=0.5) 
        for i in range(1, 13): 
            btn = Button(text=f"Meja {i}", background_normal='', bold=True)
            btn.bind(on_press=lambda inst, n=i: self.pilih_meja(inst, n))
            grid.add_widget(btn); self.btns_meja[i] = btn
        layout.add_widget(grid)
        
        self.lbl_s = Label(text="Pilih meja yang tersedia untuk pesananmu.", font_size='14sp', color=CHARCOAL_SEC, size_hint_y=0.15, halign="center")
        layout.add_widget(self.lbl_s)
        
        b_conf = Button(text="KONFIRMASI & PROSES PESANAN", size_hint_y=0.08, background_normal='', background_color=PINK_AKSEN, color=PUTIH_MURNI, bold=True)
        b_conf.bind(on_press=self.simpan_booking); layout.add_widget(b_conf); self.add_widget(layout)

    def refresh_tampilan(self):
        self.meja_terpilih = None
        for n, p in STATUS_DATABASE_MEJA.items():
            btn = self.btns_meja[n]
            if p: 
                btn.background_color = (0.9, 0.4, 0.4, 1)
                btn.text = f"Meja {n}\n[{p}]"
                btn.color = PUTIH_MURNI
            else: 
                btn.background_color = PUTIH_MURNI
                btn.text = f"Meja {n}"
                btn.color = CHARCOAL

    def pilih_meja(self, inst, n):
        if STATUS_DATABASE_MEJA[n]: 
            self.lbl_s.text = f"Meja {n} sudah terisi!"; return
        self.refresh_tampilan()
        inst.background_color = PINK_AKSEN; inst.color = PUTIH_MURNI
        self.meja_terpilih = n
        self.lbl_s.text = f"Memilih Meja {n}. Klik Konfirmasi untuk mengirim."

    def simpan_booking(self, inst):
        global KERANJANG_SEMENTARA
        nm = self.in_nama.text.strip()
        
        if not nm or not self.meja_terpilih:
            self.lbl_s.text = "Lengkapi Nama & Pilih Meja!"; return
            
        if KERANJANG_SEMENTARA is None:
            self.lbl_s.text = "Error: Keranjang makanan kosong!"; return
            
        waktu_sekarang = datetime.now()
        waktu_siap = waktu_sekarang + timedelta(minutes=KERANJANG_SEMENTARA["estimasi"]) 
        
        STATUS_DATABASE_MEJA[self.meja_terpilih] = nm
        
        KERANJANG_SEMENTARA["nama"] = f"{nm} (Meja {self.meja_terpilih})"
        KERANJANG_SEMENTARA["jam_datang"] = waktu_sekarang.strftime("%H:%M:%S")
        KERANJANG_SEMENTARA["jam_siap"] = waktu_siap.strftime("%H:%M:%S")
        
        ANTREAN_RESTORAN.put(KERANJANG_SEMENTARA)
        RIWAYAT_NOTA.append(KERANJANG_SEMENTARA)
            
        self.lbl_s.text = f"Sukses mengirim ke dapur!"
        self.in_nama.text = ""
        KERANJANG_SEMENTARA = None 
        self.refresh_tampilan()
        
        self.manager.get_screen('pesan_makanan').refresh_tampilan()
        self.manager.get_screen('nota_pesanan').refresh_nota()
        self.manager.current = 'nota_pesanan'


# ==========================================
# SCREEN: NOTA DIGITAL
# ==========================================
class NotaPesananScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout_u = Background(orientation='vertical', padding=20, spacing=10)
        
        h = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        back = Button(text='KEMBALI', size_hint_x=0.18, background_normal='', background_color=PINK_AKSEN, bold=True, font_size='12sp')
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        h.add_widget(back)
        h.add_widget(Label(text='NOTA DIGITAL', size_hint_x=0.64, bold=True, color=CHARCOAL, halign='center'))
        h.add_widget(Widget(size_hint_x=0.18))
        self.layout_u.add_widget(h)
        
        self.sc = ScrollView(size_hint_y=0.92, do_scroll_x=False)
        self.center_container = BoxLayout(orientation='horizontal', size_hint_y=None)
        self.center_container.bind(minimum_height=self.center_container.setter('height'))
        
        self.kertas_nota = BoxLayout(orientation='vertical', padding=[15, 20, 15, 20], spacing=5, size_hint=(None, None), width=340)
        self.kertas_nota.bind(minimum_height=self.kertas_nota.setter('height'))
        
        with self.kertas_nota.canvas.before:
            Color(1, 1, 1, 1) 
            self.rect_kertas = RoundedRectangle(pos=self.kertas_nota.pos, size=self.kertas_nota.size, radius=[6])
        self.kertas_nota.bind(pos=self.update_kertas, size=self.update_kertas)
        
        self.lbl_n = Label(
            text="Belum ada riwayat pesanan.", 
            color=(0.1, 0.1, 0.1, 1), 
            font_size="11sp",
            halign='left',         
            valign='top', 
            size_hint_y=None
        )
        self.lbl_n.bind(texture_size=lambda instance, size: setattr(instance, 'size', (310, size[1])))
        
        self.kertas_nota.add_widget(self.lbl_n)
        self.center_container.add_widget(Widget(size_hint_x=0.5))
        self.center_container.add_widget(self.kertas_nota)
        self.center_container.add_widget(Widget(size_hint_x=0.5))
        
        self.sc.add_widget(self.center_container)
        self.layout_u.add_widget(self.sc)
        self.add_widget(self.layout_u)  

    def update_kertas(self, *args):
        self.rect_kertas.pos = self.kertas_nota.pos
        self.rect_kertas.size = self.kertas_nota.size
        self.center_container.height = self.kertas_nota.height

    def refresh_nota(self):
        if not RIWAYAT_NOTA: 
            self.lbl_n.text = "Belum ada riwayat pesanan."
            return
        
        t = ""
        for idx, n in enumerate(RIWAYAT_NOTA, 1):
            t += "====================================\n"
            t += "       CRASH LANDING ON FOOD        \n"
            t += "            KOREAN RESTO            \n"
            t += "====================================\n"
            t += f" No. Struk : #CLF{idx:04d}\n"
            t += f" Pelanggan : {n['nama']}\n"
            t += f" Jam Masuk : {n['jam_datang']}\n"
            # --- TAMBAHAN BARU: MENAMPILKAN JAM PERKIRAAN SELESAI ---
            t += f" Perkiraan Selesai : {n['jam_siap']}\n"
            t += "------------------------------------\n"
            
            counts = {}
            for m in n['makanan']: counts[m] = counts.get(m, 0) + 1
                
            for menu_nama, kuantitas in counts.items():
                harga_satuan = self.manager.get_screen('pesan_makanan').daftar_menu[menu_nama]['harga']
                subtotal = harga_satuan * kuantitas
                
                menu_pendek = menu_nama[:20]
                str_qty = f"x{kuantitas}"
                
                spasi_tengah_1 = " " * (35 - len(menu_pendek) - len(str_qty))
                t += f" {menu_pendek}{spasi_tengah_1}{str_qty}\n"
                
                if menu_nama in n['catatan_per_menu'] and n['catatan_per_menu'][menu_nama]:
                    t += f"   *Req: {n['catatan_per_menu'][menu_nama]}\n"
                    
                str_harga = f"   @{harga_satuan:,}"
                str_subtotal = f"Rp {subtotal:,}"
                spasi_tengah_2 = " " * (35 - len(str_harga) - len(str_subtotal))
                t += f" {str_harga}{spasi_tengah_2}{str_subtotal}\n"
                
            t += "------------------------------------\n"
            str_est_label = " Estimasi Masak"
            str_est_val = f"{n['estimasi']} Menit"
            spasi_est = " " * (36 - len(str_est_label) - len(str_est_val))
            t += f"{str_est_label}{spasi_est}{str_est_val}\n"
            t += "------------------------------------\n"
            str_tot_label = " TOTAL BAYAR"
            str_tot_val = f"Rp {n['total_harga']:,}"
            spasi_tot = " " * (36 - len(str_tot_label) - len(str_tot_val))
            t += f"{str_tot_label}{spasi_tot}{str_tot_val}\n"
            t += "====================================\n"
            t += "    Saran & Kritik: @crashlanding   \n"
            t += "  Gamsahamnida! Terima kasih banyak \n"
            t += "====================================\n\n\n"
        self.lbl_n.text = t


# ==========================================
# SCREEN: ANTREAN DAPUR
# ==========================================
class StatusAntreanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = Background(orientation='vertical', padding=20, spacing=10)
        h = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        back = Button(text='KEMBALI', size_hint_x=0.18, background_normal='', background_color=PINK_AKSEN, bold=True, font_size='12sp')
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        h.add_widget(back); h.add_widget(Label(text='ANTREAN DAPUR', size_hint_x=0.64, bold=True, color=CHARCOAL, halign='center')); h.add_widget(Widget(size_hint_x=0.18)); layout.add_widget(h)
        
        self.lbl_m = Label(text="Dapur Standby.", color=PINK_AKSEN, size_hint_y=0.15, halign='center'); layout.add_widget(self.lbl_m)
        self.btn_p = Button(text="MASAK (FIFO)", size_hint_y=0.08, background_normal='', background_color=MATCHY_GREEN, color=PUTIH_MURNI, bold=True)
        self.btn_p.bind(on_press=self.masak_fifo); layout.add_widget(self.btn_p)
        
        self.sc = ScrollView(size_hint_y=0.58)
        self.lbl_i = Label(text="", color=CHARCOAL, halign='left', valign='top', size_hint_y=None)
        self.lbl_i.bind(texture_size=lambda instance, size: setattr(instance, 'size', (instance.width, size[1])))
        self.sc.add_widget(self.lbl_i); layout.add_widget(self.sc)
        layout.add_widget(Widget(size_hint_y=0.02)); self.add_widget(layout)

    def refresh_tampilan(self):
        q = list(ANTREAN_RESTORAN.queue)
        if not q: 
            self.lbl_i.text = "Antrean kosong."
            return
        t = ""
        for idx, p in enumerate(q, 1): 
            counts = {}
            for m in p['makanan']: counts[m] = counts.get(m, 0) + 1
            m_text = ", ".join([f"{k} x{v}" for k, v in counts.items()])
            c_text = " [Note: " + ", ".join([f"{k}: {v}" for k, v in p['catatan_per_menu'].items()]) + "]" if p['catatan_per_menu'] else ""
            t += f"[{idx}] {p['nama']} (Masuk: {p['jam_datang']})\n   Menu: {m_text}{c_text}\n   Target Siap: Jam {p['jam_siap']}\n\n"
        self.lbl_i.text = t

    def masak_fifo(self, inst):
        if ANTREAN_RESTORAN.empty(): 
            self.lbl_m.text = "Antrean sudah kosong!"
            return
        p = ANTREAN_RESTORAN.get()
        self.refresh_tampilan()
        
        self.lbl_m.text = f"Memasak: {p['nama']}\nTarget Selesai: {p['jam_siap']}"
        self.btn_p.disabled = True
        
        Clock.schedule_once(lambda dt: self.selesai(p), 60)

    def selesai(self, pesanan_utuh):
        nama_pelanggan = pesanan_utuh['nama']
        self.lbl_m.text = f"Selesai! Hidangan {nama_pelanggan} Siap Resto."
        self.btn_p.disabled = False
        
        if "(Meja " in nama_pelanggan:
            try:
                bagian_meja = nama_pelanggan.split("(Meja ")[1]
                nomor_meja = int(bagian_meja.split(")")[0])
                if nomor_meja in STATUS_DATABASE_MEJA:
                    STATUS_DATABASE_MEJA[nomor_meja] = None
            except Exception as e:
                print("Gagal mengosongkan meja:", e)
        
        self.refresh_tampilan()
        if self.manager and self.manager.has_screen('booking_meja'):
            self.manager.get_screen('booking_meja').refresh_tampilan()


class CrashLandingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(PesanMakananScreen(name='pesan_makanan'))
        sm.add_widget(BookingMejaScreen(name='booking_meja'))
        sm.add_widget(NotaPesananScreen(name='nota_pesanan'))
        sm.add_widget(StatusAntreanScreen(name='status_antrean'))
        return sm
    
# ======================
# DATA INJEKSI MASSAL (50 ANTREAN AWAL)
# ======================
def inject_50_antrean():
    data_sheet = [
        {"nama": "Gaeul", "makanan": ["Ramyeon", "Es Teh Manis"], "harga": 36000, "tipe": "dine_in", "meja": 1},
        {"nama": "Reyhan", "makanan": ["Kimchi Fried Rice", "Lemon Tea"], "harga": 47000, "tipe": "take_away"},
        {"nama": "Ziva", "makanan": ["Tteokbokki", "Mineral Water"], "harga": 38000, "tipe": "dine_in", "meja": 2},
        {"nama": "Aris", "makanan": ["Rabokki", "Banana Milk"], "harga": 58000, "tipe": "dine_in", "meja": 3},
        {"nama": "Wulan", "makanan": ["Jjajangmyeon", "Iced Americano"], "harga": 62000, "tipe": "take_away"},
        {"nama": "Kenzie", "makanan": ["K-Fried Chicken w/ Rice", "Matcha Latte"], "harga": 70000, "tipe": "dine_in", "meja": 4},
        {"nama": "Nabila", "makanan": ["French Fries", "Es Teh Manis"], "harga": 28000, "tipe": "take_away"},
        {"nama": "Farel", "makanan": ["Mandu (Korean Dumpling)", "Lemon Tea"], "harga": 40000, "tipe": "dine_in", "meja": 5},
        {"nama": "Gisella", "makanan": ["Corn Dog Mozzarella", "Mineral Water"], "harga": 31000, "tipe": "take_away"},
        {"nama": "Radit", "makanan": ["Bungeoppang", "Korean Strawberry Milk"], "harga": 45000, "tipe": "dine_in", "meja": 6},
        {"nama": "Naomi", "makanan": ["Croffle", "Iced Americano"], "harga": 44000, "tipe": "dine_in", "meja": 7},
        {"nama": "Anton", "makanan": ["Bingsu", "Es Teh Manis"], "harga": 40000, "tipe": "take_away"},
        {"nama": "Karina", "makanan": ["Ramyeon", "Banana Milk"], "harga": 52000, "tipe": "dine_in", "meja": 8},
        {"nama": "Bintang", "makanan": ["Kimchi Fried Rice", "Matcha Latte"], "harga": 60000, "tipe": "take_away"},
        {"nama": "Winter", "makanan": ["Tteokbokki", "Korean Strawberry Milk"], "harga": 59000, "tipe": "dine_in", "meja": 9},
        {"nama": "Arka", "makanan": ["Rabokki", "Lemon Tea"], "harga": 46000, "tipe": "take_away"},
        {"nama": "Nadin", "makanan": ["Jjajangmyeon", "Mineral Water"], "harga": 48000, "tipe": "dine_in", "meja": 10},
        {"nama": "Gavin", "makanan": ["K-Fried Chicken w/ Rice", "Iced Americano"], "harga": 65000, "tipe": "take_away"},
        {"nama": "Tiara", "makanan": ["French Fries", "Banana Milk"], "harga": 44000, "tipe": "dine_in", "meja": 11},
        {"nama": "Elang", "makanan": ["Mandu (Korean Dumpling)", "Matcha Latte"], "harga": 53000, "tipe": "take_away"},
        {"nama": "Shena", "makanan": ["Corn Dog Mozzarella", "Korean Strawberry Milk"], "harga": 52000, "tipe": "take_away"},
        {"nama": "Carmen", "makanan": ["Bungeoppang", "Es Teh Manis"], "harga": 26000, "tipe": "take_away"},
        {"nama": "Amara", "makanan": ["Croffle", "Lemon Tea"], "harga": 36000, "tipe": "take_away"},
        {"nama": "Bagas", "makanan": ["Bingsu", "Mineral Water"], "harga": 38000, "tipe": "take_away"},
        {"nama": "Clara", "makanan": ["Ramyeon", "Iced Americano"], "harga": 48000, "tipe": "take_away"},
        {"nama": "Devan", "makanan": ["Kimchi Fried Rice", "Banana Milk"], "harga": 59000, "tipe": "take_away"},
        {"nama": "Leya", "makanan": ["Tteokbokki", "Matcha Latte"], "harga": 57000, "tipe": "take_away"},
        {"nama": "Farhan", "makanan": ["Rabokki", "Korean Strawberry Milk"], "harga": 61000, "tipe": "take_away"},
        {"nama": "Grace", "makanan": ["Jjajangmyeon", "Es Teh Manis"], "harga": 50000, "tipe": "take_away"},
        {"nama": "Hanif", "makanan": ["K-Fried Chicken w/ Rice", "Lemon Tea"], "harga": 57000, "tipe": "take_away"},
        {"nama": "Indah", "makanan": ["French Fries", "Mineral Water"], "harga": 26000, "tipe": "take_away"},
        {"nama": "Joni", "makanan": ["Mandu (Korean Dumpling)", "Iced Americano"], "harga": 48000, "tipe": "take_away"},
        {"nama": "Keisha", "makanan": ["Corn Dog Mozzarella", "Banana Milk"], "harga": 49000, "tipe": "take_away"},
        {"nama": "Lino", "makanan": ["Bungeoppang", "Matcha Latte"], "harga": 43000, "tipe": "take_away"},
        {"nama": "Maura", "makanan": ["Croffle", "Korean Strawberry Milk"], "harga": 51000, "tipe": "take_away"},
        {"nama": "Niko", "makanan": ["Bingsu", "Es Teh Manis"], "harga": 40000, "tipe": "take_away"},
        {"nama": "Olivia", "makanan": ["Ramyeon", "Lemon Tea"], "harga": 40000, "tipe": "take_away"},
        {"nama": "Putra", "makanan": ["Kimchi Fried Rice", "Mineral Water"], "harga": 41000, "tipe": "take_away"},
        {"nama": "Suzy", "makanan": ["Tteokbokki", "Iced Americano"], "harga": 52000, "tipe": "take_away"},
        {"nama": "Rian", "makanan": ["Rabokki", "Banana Milk"], "harga": 58000, "tipe": "take_away"},
        {"nama": "Salsa", "makanan": ["Jjajangmyeon", "Matcha Latte"], "harga": 67000, "tipe": "take_away"},
        {"nama": "Tomi", "makanan": ["K-Fried Chicken w/ Rice", "Korean Strawberry Milk"], "harga": 72000, "tipe": "take_away"},
        {"nama": "Ufa", "makanan": ["French Fries", "Es Teh Manis"], "harga": 28000, "tipe": "take_away"},
        {"nama": "Vino", "makanan": ["Mandu (Korean Dumpling)", "Lemon Tea"], "harga": 40000, "tipe": "take_away"},
        {"nama": "Wanda", "makanan": ["Corn Dog Mozzarella", "Mineral Water"], "harga": 31000, "tipe": "take_away"},
        {"nama": "Xavi", "makanan": ["Bungeoppang", "Iced Americano"], "harga": 38000, "tipe": "take_away"},
        {"nama": "Yuna", "makanan": ["Croffle", "Banana Milk"], "harga": 48000, "tipe": "take_away"},
        {"nama": "Zaki", "makanan": ["Bingsu", "Matcha Latte"], "harga": 57000, "tipe": "take_away"},
        {"nama": "Ziva", "makanan": ["Ramyeon", "Korean Strawberry Milk"], "harga": 55000, "tipe": "take_away"},
        {"nama": "Giri", "makanan": ["Kimchi Fried Rice", "Es Teh Manis"], "harga": 43000, "tipe": "take_away"}
    ]
    
    waktu_menu_ref = {
        "Ramyeon": 5, "Kimchi Fried Rice": 5, "Tteokbokki": 6, "Rabokki": 6, "Jjajangmyeon": 7, "K-Fried Chicken w/ Rice": 9,
        "French Fries": 3, "Mandu (Korean Dumpling)": 5, "Corn Dog Mozzarella": 6, "Bungeoppang": 5, "Croffle": 5, "Bingsu": 6,
        "Es Teh Manis": 2, "Lemon Tea": 2, "Mineral Water": 1, "Iced Americano": 2, "Banana Milk": 2, "Matcha Latte": 3, "Korean Strawberry Milk": 3
    }
    
    waktu_awal = datetime.now()
    for idx, item in enumerate(data_sheet):
        total_estimasi_menit = sum(waktu_menu_ref.get(m, 2) for m in item["makanan"])
        waktu_masuk = waktu_awal + timedelta(minutes=(idx * 2))
        waktu_siap = waktu_masuk + timedelta(minutes=total_estimasi_menit) 
        
        if item["tipe"] == "dine_in":
            no_meja = item["meja"]
            STATUS_DATABASE_MEJA[no_meja] = item["nama"]
            nama_final = f"{item['nama']} (Meja {no_meja})"
        else:
            nama_final = f"{item['nama']} (Take Away)"
        
        data_pesanan = {
            "nama": nama_final,
            "makanan": item["makanan"],
            "catatan_per_menu": {},
            "estimasi": total_estimasi_menit,
            "total_harga": item["harga"],
            "jam_datang": waktu_masuk.strftime("%H:%M:%S"),
            "jam_siap": waktu_siap.strftime("%H:%M:%S")
        }
        
        ANTREAN_RESTORAN.put(data_pesanan)
        RIWAYAT_NOTA.append(data_pesanan)

if __name__ == '__main__': 
    inject_50_antrean() 
    CrashLandingApp().run()