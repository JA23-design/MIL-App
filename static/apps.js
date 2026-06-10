const input = document.getElementById("baseSearch");
const box = document.getElementById("suggestions");
const hidden = document.getElementById("base_id");

input.addEventListener("input", async () => {
    const res = await fetch(`/api/search/bases?q=${input.value}`);
    const data = await res.json();

    box.innerHTML = "";

    data.forEach(b => {
        const div = document.createElement("div");
        div.innerText = `${b.name} (${b.state})`;

        div.onclick = () => {
            input.value = b.name;
            hidden.value = b.id;
            box.innerHTML = "";
        };

        box.appendChild(div);
    });
});
