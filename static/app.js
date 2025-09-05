const API = "/api/todos";
const listEl = document.getElementById("list");
const formEl = document.getElementById("new-form");
const inputEl = document.getElementById("new-title");

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = inputEl.value.trim();
  if (!title) return;
  await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title })
  });
  inputEl.value = "";
  await load();
});

async function load() {
  const res = await fetch(API);
  const todos = await res.json();
  render(todos);
}

function render(todos) {
  listEl.innerHTML = "";
  todos.forEach(t => listEl.appendChild(row(t)));
}

function row(todo) {
  const li = document.createElement("li");
  if (todo.completed) li.classList.add("done");

  // checkbox
  const cb = document.createElement("input");
  cb.type = "checkbox";
  cb.checked = todo.completed;
  cb.addEventListener("change", () => toggle(todo.id, cb.checked));

  // title (editable)
  const span = document.createElement("span");
  span.className = "title";
  span.textContent = todo.title;
  span.contentEditable = "true";
  span.addEventListener("blur", () => {
    const newTitle = span.textContent.trim();
    if (newTitle && newTitle !== todo.title) {
      update(todo.id, { title: newTitle });
    } else {
      span.textContent = todo.title; // restore
    }
  });

  // spacer
  const spacer = document.createElement("div");
  spacer.className = "spacer";

  // delete
  const del = document.createElement("button");
  del.textContent = "Delete";
  del.addEventListener("click", () => removeTodo(todo.id));

  li.append(cb, span, spacer, del);
  return li;
}

async function toggle(id, completed) {
  await update(id, { completed });
  await load();
}

async function update(id, payload) {
  await fetch(`${API}/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

async function removeTodo(id) {
  await fetch(`${API}/${id}`, { method: "DELETE" });
  await load();
}

load();
