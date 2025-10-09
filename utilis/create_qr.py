import qrcode
from qrcode.constants import ERROR_CORRECT_M
import argparse
from pathlib import Path

def make_qr(url: str, out: Path, box_size: int = 10, border: int = 4):
    qr = qrcode.QRCode(
        version=None,               # otomatik boyut
        error_correction=ERROR_CORRECT_M,  # %15 hata düzeltme
        box_size=box_size,          # piksel kutu boyu
        border=border,              # kenar boşluğu (modül)
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out)
    return out

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Verilen link için QR kodu üretir.")
    p.add_argument("link", help="QR koda dönüştürülecek URL/metin")
    p.add_argument("-o", "--out", default="qrcode.png", help="Çıktı dosya adı (PNG)")
    p.add_argument("--box", type=int, default=10, help="Kutu boyutu (px)")
    p.add_argument("--border", type=int, default=4, help="Kenar boşluğu (modül)")
    args = p.parse_args()

    path = Path(args.out)
    out = make_qr(args.link, path, args.box, args.border)
    print(f"QR kod kaydedildi: {out.resolve()}")

# run commands :  python create_qr.py "https://www.linkedin.com/in/hatice-eris-b82b69269" -o hatice.png
