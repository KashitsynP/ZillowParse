const form = document.getElementById("dataForm");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    
    try {
        const response = await fetch("/fetch_and_process_data", {
            method: "POST",
            body: formData,
        });
        if (response.ok) {
            let data = await response.json();
            data = JSON.parse(data);
            // Очищаем содержимое div с результатами
            resultDiv.innerHTML = "";
            // Перебираем список словарей и отображаем данные
    data.data.forEach((item) => {
        const itemDiv = document.createElement("div");
        
        itemDiv.innerHTML = `
            <br>
            <p>Адрес: ${item.address}</p>
            <p>Цена: ${item.price}$</p>
            <p>Тип недвижимости: ${item.listingStatus}</p>
            <p>Спальни: ${item.bedrooms}</p>
            <p>Сан.узлы: ${item.bathrooms}</p>
            <p>Жилая площадь: ${item.livingArea} кв. футов</p>
            <p>zpid: ${item.zpid}</p>
            `;
        item.wfm.forEach((store_wfm) => {
            itemDiv.innerHTML += `
            <p>Wholefoodsmarket: ${store_wfm} миль</p>
            `;
        });
        item.tj.forEach((store_tj) => {
            itemDiv.innerHTML += `
            <p>Trader Joe\`s: ${store_tj} миль</p>
            `;
        });
        if (item.imgSrc) {
            const img = document.createElement("img");
            img.src = item.imgSrc;
            itemDiv.appendChild(img);
            itemDiv.innerHTML += `<hr class="my-5">`
        }
        resultDiv.appendChild(itemDiv);
    });
        } else {
            resultDiv.innerHTML = "<p>Произошла ошибка при запросе данных.</p>";
        }
    } catch (error) {
        console.error("Ошибка:", error);
        resultDiv.innerHTML = "<p>Произошла ошибка при выполнении запроса.</p>";
    }
});
