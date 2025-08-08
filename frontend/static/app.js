const API = "http://127.0.0.1:8000/mr/generate";
document.getElementById("go").onclick = async () => {
  const desc = document.getElementById("desc").value;
  const out = document.getElementById("out");
  out.textContent = "Loading...";
  try {
    const res = await fetch(API, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ description: desc, options: { return_format: "json" } })
    });
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = "Error: " + e;
  }
};
