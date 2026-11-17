
async function prediksiTanaman() {
    const warna = document.getElementById("warna").value;
    const kelembapan = document.getElementById("kelembapan").value;
    const batang = document.getElementById("batang").value;
    const cahaya = document.getElementById("cahaya").value;

    const tombol = document.getElementById("predictButton");
    const hasil = document.getElementById("predictionResult");

    tombol.disabled = true;
    tombol.innerText = "Sedang Menganalisis...";

    try {
        const response = await fetch("/prediksi", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                warna: warna,
                kelembapan: kelembapan,
                batang: batang,
                cahaya: cahaya
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Prediksi gagal dilakukan.");
        }

        const sehat = data.sehat;
        const tidakSehat = data.tidak_sehat;
        const status = data.hasil_akhir;

        const kelas = status === "Sehat" ? "healthy" : "unhealthy";
        const simbol = status === "Sehat" ? "🌱" : "⚠️";

        let detailPohon = "";

        for (const [nama, prediksi] of Object.entries(data.hasil_pohon)) {
            detailPohon += `
                <div class="vote-row">
                    <span>${nama}</span>
                    <strong class="${prediksi === 'Sehat' ? 'healthy' : 'unhealthy'}">
                        ${prediksi}
                    </strong>
                </div>
            `;
        }

        hasil.innerHTML = `
            <h3 class="output-title">Hasil Analisis Tanaman</h3>

            <div class="final-result ${kelas}">
                <div style="font-size:35px">${simbol}</div>
                <p>HASIL KLASIFIKASI RANDOM FOREST</p>
                <h2>${status}</h2>
                <p>Berdasarkan hasil Majority Voting dari 3 pohon keputusan</p>
            </div>

            <h3 style="font-size:13px; margin-bottom:10px;">
                Hasil Setiap Decision Tree
            </h3>

            ${detailPohon}

            <div class="vote-summary">
                <div class="vote-box">
                    <strong style="color:#16845b">${sehat}</strong>
                    <small>Vote Sehat</small>
                </div>
                <div class="vote-box">
                    <strong style="color:#d65d53">${tidakSehat}</strong>
                    <small>Vote Tidak Sehat</small>
                </div>
            </div>
        `;

    } catch (error) {
        hasil.innerHTML = `
            <div class="result-placeholder">
                <h3>Terjadi Kesalahan</h3>
                <p>${error.message}</p>
            </div>
        `;
    } finally {
        tombol.disabled = false;
        tombol.innerText = "Analisis Kesehatan Tanaman →";
    }
}
