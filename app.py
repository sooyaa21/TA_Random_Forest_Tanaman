
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dataset training: 14 data kesehatan tanaman
data_training = [
    ["Hijau", "Lembap", "Kuat", "Cukup", "Sehat"],
    ["Hijau", "Lembap", "Kuat", "Kurang", "Sehat"],
    ["Kuning", "Kering", "Layu", "Kurang", "Tidak Sehat"],
    ["Kuning", "Kering", "Layu", "Cukup", "Tidak Sehat"],
    ["Hijau", "Lembap", "Kuat", "Cukup", "Sehat"],
    ["Kuning", "Lembap", "Layu", "Cukup", "Tidak Sehat"],
    ["Hijau", "Kering", "Kuat", "Cukup", "Sehat"],
    ["Kuning", "Kering", "Kuat", "Kurang", "Tidak Sehat"],
    ["Hijau", "Lembap", "Layu", "Cukup", "Sehat"],
    ["Kuning", "Lembap", "Kuat", "Cukup", "Sehat"],
    ["Hijau", "Kering", "Layu", "Kurang", "Tidak Sehat"],
    ["Hijau", "Lembap", "Kuat", "Kurang", "Sehat"],
    ["Kuning", "Kering", "Layu", "Kurang", "Tidak Sehat"],
    ["Hijau", "Lembap", "Kuat", "Cukup", "Sehat"]
]

# Bootstrap sample yang sama dengan perhitungan manual laporan
bootstrap_samples = {
    "Pohon 1": [12, 3, 9, 13, 2, 8, 3, 9, 5, 12, 14, 6, 7, 2],
    "Pohon 2": [1, 3, 4, 5, 6, 7, 8, 10, 10, 11, 12, 13, 14, 1],
    "Pohon 3": [1, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
}

# Struktur pohon sesuai hasil perhitungan manual
trees = {
    "Pohon 1": {
        "akar": "Warna Daun",
        "cabang": {
            "Hijau": "Sehat",
            "Kuning": "Tidak Sehat"
        }
    },
    "Pohon 2": {
        "akar": "Kondisi Batang",
        "cabang": {
            "Layu": "Tidak Sehat",
            "Kuat": {
                "atribut": "Kelembapan Tanah",
                "cabang": {
                    "Lembap": "Sehat",
                    "Kering": {
                        "atribut": "Warna Daun",
                        "cabang": {
                            "Hijau": "Sehat",
                            "Kuning": "Tidak Sehat"
                        }
                    }
                }
            }
        }
    },
    "Pohon 3": {
        "akar": "Warna Daun",
        "cabang": {
            "Hijau": {
                "atribut": "Kelembapan Tanah",
                "cabang": {
                    "Lembap": "Sehat",
                    "Kering": {
                        "atribut": "Kondisi Batang",
                        "cabang": {
                            "Kuat": "Sehat",
                            "Layu": "Tidak Sehat"
                        }
                    }
                }
            },
            "Kuning": {
                "atribut": "Kondisi Batang",
                "cabang": {
                    "Layu": "Tidak Sehat",
                    "Kuat": {
                        "atribut": "Kelembapan Tanah",
                        "cabang": {
                            "Kering": "Tidak Sehat",
                            "Lembap": "Sehat"
                        }
                    }
                }
            }
        }
    }
}

def ambil_nilai(data, atribut):
    indeks = {
        "Warna Daun": 0,
        "Kelembapan Tanah": 1,
        "Kondisi Batang": 2,
        "Intensitas Cahaya": 3
    }
    return data[indeks[atribut]]

def prediksi_pohon(pohon, data):
    hasil = pohon
    while isinstance(hasil, dict):
        if "akar" in hasil:
            atribut = hasil["akar"]
            hasil = hasil["cabang"][ambil_nilai(data, atribut)]
        else:
            atribut = hasil["atribut"]
            hasil = hasil["cabang"][ambil_nilai(data, atribut)]
    return hasil

@app.route("/")
def index():
    return render_template(
        "index.html",
        data_training=data_training,
        bootstrap_samples=bootstrap_samples,
        trees=trees
    )

@app.route("/prediksi", methods=["POST"])
def prediksi():
    data = request.get_json()

    input_data = [
        data["warna"],
        data["kelembapan"],
        data["batang"],
        data["cahaya"]
    ]

    hasil_pohon = {}
    for nama, pohon in trees.items():
        hasil_pohon[nama] = prediksi_pohon(pohon, input_data)

    sehat = list(hasil_pohon.values()).count("Sehat")
    tidak_sehat = list(hasil_pohon.values()).count("Tidak Sehat")

    hasil_akhir = "Sehat" if sehat > tidak_sehat else "Tidak Sehat"

    return jsonify({
        "hasil_pohon": hasil_pohon,
        "sehat": sehat,
        "tidak_sehat": tidak_sehat,
        "hasil_akhir": hasil_akhir
    })

if __name__ == "__main__":
    app.run(debug=True)
