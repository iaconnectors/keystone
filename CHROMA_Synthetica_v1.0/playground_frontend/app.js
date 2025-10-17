const API_BASE = "http://localhost:8000";

const THEMES = [
  "cinematografico",
  "publicitario",
  "design",
  "arquitetura",
  "montagem_de_stands",
  "criacao_de_personagem",
  "criacao_de_cena",
  "estudo_de_objeto",
  "estudo_de_personagem",
];

const state = {
  currentSession: null,
  history: [],
  references: [],
  cases: {},
  activeHistoryTab: "all",
  selectedCaseId: null,
};

const elements = {
  brief: document.getElementById("brief"),
  theme: document.getElementById("theme"),
  model: document.getElementById("model"),
  tags: document.getElementById("tags"),
  status: document.getElementById("status-message"),
  resultsSection: document.getElementById("results-section"),
  blueprintOutput: document.getElementById("blueprint-output"),
  promptsOutput: document.getElementById("prompts-output"),
  notesBlock: document.getElementById("notes-block"),
  notesList: document.getElementById("notes-list"),
  likeBtn: document.getElementById("like-btn"),
  copyBlueprintBtn: document.getElementById("copy-blueprint-btn"),
  casesList: document.getElementById("cases-list"),
  historyList: document.getElementById("history-list"),
  historyTabs: document.querySelectorAll("#history-panel .tab"),
  form: document.getElementById("prompt-form"),
};

function populateThemes() {
  elements.theme.innerHTML = "";
  THEMES.forEach((theme) => {
    const option = document.createElement("option");
    option.value = theme;
    option.textContent = theme.replace(/_/g, " ");
    elements.theme.appendChild(option);
  });
}

async function loadCases() {
  try {
    const response = await fetch("../playgrounds/seedream_cases.json");
    if (!response.ok) throw new Error("Falha ao carregar presets.");
    const data = await response.json();
    state.cases = data.cases || {};
    renderCases();
  } catch (error) {
    console.warn(error.message);
    elements.casesList.innerHTML =
      '<p class="muted">Nao foi possivel carregar os presets.</p>';
  }
}

function renderCases() {
  elements.casesList.innerHTML = "";
  const entries = Object.entries(state.cases);
  if (!entries.length) {
    elements.casesList.innerHTML =
      '<p class="muted">Nenhum preset encontrado.</p>';
    return;
  }

  entries.forEach(([caseId, caseData]) => {
    const card = document.createElement("div");
    card.className = "card";

    const title = document.createElement("h3");
    title.textContent = caseData.title || caseId;

    const theme = document.createElement("div");
    theme.className = "theme-pill";
    theme.textContent = (caseData.theme || "default").replace(/_/g, " ");

    const desc = document.createElement("p");
    desc.className = "card-brief";
    desc.textContent = caseData.brief || "Brief nao definido.";

    const buttonRow = document.createElement("div");
    buttonRow.className = "card-actions";
    const useBtn = document.createElement("button");
    useBtn.className = "use-btn";
    useBtn.textContent = "Carregar preset";
    useBtn.addEventListener("click", () => {
      elements.brief.value = caseData.brief || "";
      elements.theme.value =
        THEMES.includes(caseData.theme) ? caseData.theme : elements.theme.value;
      elements.tags.value = (caseData.tags || []).join(", ");
      state.selectedCaseId = caseId;
      elements.brief.focus();
      showStatus(`Preset "${caseData.title || caseId}" carregado.`, "success");
    });
    buttonRow.appendChild(useBtn);

    card.appendChild(title);
    card.appendChild(theme);
    card.appendChild(desc);
    card.appendChild(buttonRow);
    elements.casesList.appendChild(card);
  });
}

function showStatus(message, type = "info") {
  elements.status.textContent = message;
  elements.status.dataset.statusType = type;
}

async function fetchHistory() {
  try {
    const res = await fetch(`${API_BASE}/history`);
    if (!res.ok) throw new Error("Falha ao obter historico.");
    const data = await res.json();
    state.history = data.items || [];
  } catch (error) {
    console.warn(error.message);
    state.history = [];
  }
}

async function fetchReferences() {
  try {
    const res = await fetch(`${API_BASE}/references`);
    if (!res.ok) throw new Error("Falha ao obter referencias.");
    const data = await res.json();
    state.references = data.items || [];
  } catch (error) {
    console.warn(error.message);
    state.references = [];
  }
}

function renderHistory() {
  const template = document.getElementById("prompt-card-template");
  elements.historyList.innerHTML = "";
  let items = state.history;
  if (state.activeHistoryTab === "liked") {
    items = items.filter((item) => item.liked);
  }

  if (!items.length) {
    elements.historyList.innerHTML =
      '<p class="muted">Nenhum registro disponivel.</p>';
    return;
  }

  items.forEach((session) => {
    const fragment = template.content.cloneNode(true);
    fragment.querySelector(".theme-pill").textContent = session.theme.replace(
      /_/g,
      " "
    );
    fragment.querySelector(".timestamp").textContent = new Date(
      session.created_at
    ).toLocaleString();
    fragment.querySelector(".card-brief").textContent = session.brief.slice(
      0,
      160
    );

    const useBtn = fragment.querySelector(".use-btn");
    useBtn.addEventListener("click", () => {
      elements.brief.value = session.brief;
      elements.theme.value = session.theme;
      elements.tags.value = (session.tags || []).join(", ");
      state.selectedCaseId = session.case_id || null;
      showStatus("Sessao carregada no formulario.", "success");
    });

    const likeBtn = fragment.querySelector(".like-toggle");
    if (session.liked) {
      likeBtn.classList.add("liked");
      likeBtn.textContent = "Curtido";
    } else {
      likeBtn.textContent = "Curtir";
    }
    likeBtn.addEventListener("click", () => toggleLike(session.id, !session.liked));

    elements.historyList.appendChild(fragment);
  });
}

async function toggleLike(sessionId, liked) {
  try {
    const res = await fetch(`${API_BASE}/history/${sessionId}/like`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ liked }),
    });
    if (!res.ok) throw new Error("Nao foi possivel atualizar o like.");
    await refreshHistory();
    if (state.currentSession && state.currentSession.id === sessionId) {
      state.currentSession.liked = liked;
      updateLikeButton();
    }
  } catch (error) {
    showStatus(error.message, "error");
  }
}

async function refreshHistory() {
  await fetchHistory();
  await fetchReferences();
  renderHistory();
}

function renderResult(session) {
  elements.resultsSection.hidden = false;
  elements.blueprintOutput.textContent = session.blueprint;
  elements.promptsOutput.innerHTML = "";
  Object.entries(session.prompts || {}).forEach(([modelName, promptText]) => {
    const wrapper = document.createElement("div");
    wrapper.className = "prompt-item";
    const header = document.createElement("header");
    header.innerHTML = `<span>${modelName}</span>`;

    const copyBtn = document.createElement("button");
    copyBtn.className = "copy-btn";
    copyBtn.textContent = "Copiar";
    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(promptText);
      showStatus(`Prompt para ${modelName} copiado.`, "success");
    });
    header.appendChild(copyBtn);
    wrapper.appendChild(header);

    const body = document.createElement("pre");
    body.className = "mono";
    body.textContent = promptText;
    wrapper.appendChild(body);

    elements.promptsOutput.appendChild(wrapper);
  });

  const notes = (session.checklist_questions || []).concat(
    session.notes || []
  );
  if (notes.length) {
    elements.notesBlock.hidden = false;
    elements.notesList.innerHTML = "";
    notes.forEach((note) => {
      const li = document.createElement("li");
      li.textContent = note;
      elements.notesList.appendChild(li);
    });
  } else {
    elements.notesBlock.hidden = true;
  }

  updateLikeButton();
}

function updateLikeButton() {
  if (!state.currentSession) {
    elements.likeBtn.disabled = true;
    return;
  }
  elements.likeBtn.disabled = false;
  if (state.currentSession.liked) {
    elements.likeBtn.textContent = "Curtido";
    elements.likeBtn.classList.add("liked");
  } else {
    elements.likeBtn.textContent = "Curtir referencia";
    elements.likeBtn.classList.remove("liked");
  }
}

async function handleSubmit(event) {
  event.preventDefault();
  const brief = elements.brief.value.trim();
  const theme = elements.theme.value;
  const model = elements.model.value;
  const tags = elements.tags.value
    .split(",")
    .map((tag) => tag.trim())
    .filter(Boolean);

  if (!brief) {
    showStatus("Informe um briefing valido.", "error");
    return;
  }

  showStatus("Gerando prompts...", "info");
  elements.form.classList.add("loading");

  try {
    const res = await fetch(`${API_BASE}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        brief,
        theme,
        model,
        case_id: state.selectedCaseId || null,
        tags,
      }),
    });

    if (res.status === 422) {
      const data = await res.json();
      const missing = data.detail?.missing_fields || [];
      const formatted = missing
        .map((item) =>
          item.field
            ? `${item.component}.${item.field}`
            : item.component
        )
        .join(", ");
      throw new Error(
        `O modelo retornou campos incompletos. Revise manualmente: ${formatted}`
      );
    }

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || "Falha ao gerar prompts.");
    }

    const data = await res.json();
    state.currentSession = data.session;
    renderResult(state.currentSession);
    await refreshHistory();
    showStatus("Prompt gerado com sucesso!", "success");
  } catch (error) {
    console.error(error);
    showStatus(error.message, "error");
  } finally {
    elements.form.classList.remove("loading");
  }
}

function initHistoryTabs() {
  elements.historyTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      elements.historyTabs.forEach((btn) => btn.classList.remove("active"));
      tab.classList.add("active");
      state.activeHistoryTab = tab.dataset.tab;
      renderHistory();
    });
  });
}

function initLikeButton() {
  elements.likeBtn.addEventListener("click", () => {
    if (!state.currentSession) return;
    toggleLike(state.currentSession.id, !state.currentSession.liked);
  });
}

function initCopyBlueprint() {
  elements.copyBlueprintBtn.addEventListener("click", () => {
    if (!state.currentSession) return;
    navigator.clipboard.writeText(state.currentSession.blueprint);
    showStatus("Blueprint copiado para a area de transferencia.", "success");
  });
}

async function bootstrap() {
  populateThemes();
  await loadCases();
  await refreshHistory();
  initHistoryTabs();
  initLikeButton();
  initCopyBlueprint();
  elements.form.addEventListener("submit", handleSubmit);
}

bootstrap();

