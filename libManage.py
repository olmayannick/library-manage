import tkinter as tk
from tkinter import simpledialog, messagebox

# Dosya işlemleri ve kütüphane sınıfı
def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

class Library:
    def __init__(self, filepath):
        self.filepath = filepath
        self.books = self.load_books()

    def __del__(self):
        self.save_books()

# Dosyadan kitapları yükleme ve kaydetme
    def load_books(self):
        try:
            with open(self.filepath, 'a+') as file:
                file.seek(0)
                books = [line.strip().split(',') for line in file.readlines()]
            return books
        except FileNotFoundError:
            return []
        

# Kitap ekleme, silme ve listeleme
    def save_books(self):
        with open(self.filepath, 'w') as file:
            for book in self.books:
                file.write(','.join(book) + '\n')

    def add_book(self, name, author, release_date, pages):
        if not all([is_integer(release_date), is_integer(pages)]):
            messagebox.showerror("Bilinmeyen Girdi", "Lütfen tarih ya da  Sayfa sayısını doğru formatta girdiğinizden emin olun.")
            return
        self.books.append([name, author, release_date, pages])
        
    def remove_book(self, index):
        try:
            index = int(index) - 1  
            removed_book = self.books.pop(index)
        except (ValueError, IndexError):
            messagebox.showerror("Hata", "Geçersiz index.")

    def list_books(self):
        books_info = "\n".join([f"{index + 1}. {book[0]} by {book[1]}, Released: {book[2]}, Pages: {book[3]}" 
                                for index, book in enumerate(self.books)])
        messagebox.showinfo("Kitaplar", books_info if books_info else "Kütüphanede kitap bulunmuyor.")


# GUI tasarım kısmı

class LibraryApp:
    def __init__(self, master, library):
        self.master = master
        self.library = library
        master.title("Library Yönetim Sistemi")
        master.geometry("400x300")
        master.config(bg='salmon')

        tk.Label(master, text="Hoş Geldiniz", font=("Times new roman", 25, "bold"), bg='salmon').pack(pady=35)

        tk.Button(master, text="Kitap Ekle", command=self.add_book_screen, width=20, height=2, bg='white', fg='black').pack(pady=5)
        tk.Button(master, text="Kitap Sil", command=self.remove_book, width=20, height=2, bg='white', fg='black').pack(pady=5)
        tk.Button(master, text="Kitapları Listele", command=self.library.list_books, width=20, height=2, bg='white', fg='black').pack(pady=5)

# Kitap ekleme ekranı
    def add_book_screen(self):
        self.add_book_window = tk.Toplevel(self.master)
        self.add_book_window.title("Kitap Ekleme Ekranı")
        self.add_book_window.geometry("300x200")

        tk.Label(self.add_book_window, text="Kitap Adı:").pack()
        self.book_name_entry = tk.Entry(self.add_book_window)
        self.book_name_entry.pack()

        tk.Label(self.add_book_window, text="Yazar Adı:").pack()
        self.author_name_entry = tk.Entry(self.add_book_window)
        self.author_name_entry.pack()

        tk.Label(self.add_book_window, text="Yıl:").pack()
        self.year_entry = tk.Entry(self.add_book_window)
        self.year_entry.pack()

        tk.Label(self.add_book_window, text="Sayfa sayısı:").pack()
        self.page_number_entry = tk.Entry(self.add_book_window)
        self.page_number_entry.pack()

        tk.Button(self.add_book_window, text="Kaydet", command=self.save_book).pack(pady=10)

# Kitap ekleme fonksiyonu
    def save_book(self):
        name = self.book_name_entry.get()
        author = self.author_name_entry.get()
        year = self.year_entry.get()
        pages = self.page_number_entry.get()
        if all([name, author, year, pages]) and year.isdigit() and pages.isdigit():
            self.library.add_book(name, author, year, pages)
            messagebox.showinfo("Başarılı", f" '{name}' Başarıyla Eklendi.")
            self.add_book_window.destroy()
        else:
            messagebox.showerror("Hata", "Geçersiz giriş. Lütfen tüm alanların doğru doldurulduğundan emin olun.")

# Kitap silme ekranı
    def remove_book(self):
        index = simpledialog.askstring("Kitap Sil", "Kaldırmak için index i giriniz:")
        if index and index.isdigit():
            self.library.remove_book(index)
            messagebox.showinfo("Başarılı", f"Kitap Başarıyla Silindi.")
        else:
            messagebox.showerror("Hata", "Geçersiz index.")

# Uygulama başlatma 
def main():
    root = tk.Tk()
    library = Library('books.txt') 
    app = LibraryApp(root, library)
    root.mainloop()

if __name__ == "__main__":
    main()

