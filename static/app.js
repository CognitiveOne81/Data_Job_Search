const results = document.getElementById("results");
const form = document.getElementById("search-form");
const queryInput = document.getElementById("query");
const heading = document.getElementById("results-heading");

const DEFAULT_ZIP = "32246";
const DEFAULT_RADIUS = 30;

function renderItems(query, zip, radius, items) {
  heading.textContent = `First ${items.length} results for "${query}" within ${radius} miles of ${zip}`;
  results.innerHTML = "";

  if (!items.length) {
    const li = document.createElement("li");
    li.textContent = "No matching Marketplace items found.";
    results.appendChild(li);
    return;
  }

  items.forEach((item) => {
    const li = document.createElement("li");

    const name = document.createElement("a");
    name.className = "item-name";
    name.href = item.listing_url;
    name.target = "_blank";
    name.rel = "noopener noreferrer";
    name.textContent = item.name;

    const price = document.createElement("span");
    price.className = "item-price";
    price.textContent = `${item.price} • ${item.distance_miles} miles away`;

    li.appendChild(name);
    li.appendChild(price);
    results.appendChild(li);
  });
}

async function loadItems(query) {
  const response = await fetch(
    `/api/marketplace?query=${encodeURIComponent(query)}&zip=${encodeURIComponent(DEFAULT_ZIP)}&radius=${DEFAULT_RADIUS}`,
  );
  const data = await response.json();
  renderItems(data.query, data.zip, data.radius_miles, data.items);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = queryInput.value.trim() || "mac";
  await loadItems(query);
});

loadItems("mac");
