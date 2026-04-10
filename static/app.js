const results = document.getElementById("results");
const form = document.getElementById("search-form");
const queryInput = document.getElementById("query");
const heading = document.getElementById("results-heading");

function renderItems(query, items) {
  heading.textContent = `First ${items.length} results for "${query}"`;
  results.innerHTML = "";

  if (!items.length) {
    const li = document.createElement("li");
    li.textContent = "No matching Marketplace items found.";
    results.appendChild(li);
    return;
  }

  items.forEach((item) => {
    const li = document.createElement("li");

    const name = document.createElement("span");
    name.className = "item-name";
    name.textContent = item.name;

    const price = document.createElement("span");
    price.className = "item-price";
    price.textContent = item.price;

    li.appendChild(name);
    li.appendChild(price);
    results.appendChild(li);
  });
}

async function loadItems(query) {
  const response = await fetch(`/api/marketplace?query=${encodeURIComponent(query)}`);
  const data = await response.json();
  renderItems(data.query, data.items);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = queryInput.value.trim() || "mac";
  await loadItems(query);
});

loadItems("mac");
