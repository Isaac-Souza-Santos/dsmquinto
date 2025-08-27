// Configuração da API
const API_BASE_URL = "http://localhost:5000";
const API_ENDPOINTS = {
  tarefas: `${API_BASE_URL}/tarefas`,
};

// Estado global da aplicação
let tasks = [];
let currentFilter = "todas";

// Elementos DOM
const elements = {
  loading: document.getElementById("loading"),
  tasksList: document.getElementById("tasks-list"),
  noTasks: document.getElementById("no-tasks"),
  totalTarefas: document.getElementById("total-tarefas"),
  tarefasPendentes: document.getElementById("tarefas-pendentes"),
  tarefasConcluidas: document.getElementById("tarefas-concluidas"),
  progressFill: document.getElementById("progress-fill"),
  progressText: document.getElementById("progress-text"),
  productivity: document.getElementById("productivity"),
  dailyGoal: document.getElementById("daily-goal"),
  newTaskForm: document.getElementById("new-task-form"),
  editModal: document.getElementById("edit-modal"),
  editTaskForm: document.getElementById("edit-task-form"),
  toast: document.getElementById("toast"),
  toastMessage: document.getElementById("toast-message"),
};

// Inicialização da aplicação
document.addEventListener("DOMContentLoaded", function () {
  initializeApp();
  setupEventListeners();
});

// Inicializar aplicação
async function initializeApp() {
  try {
    await loadTasks();
    updateStatistics();
  } catch (error) {
    showToast("Erro ao carregar tarefas", "error");
    console.error("Erro na inicialização:", error);
  }
}

// Configurar event listeners
function setupEventListeners() {
  // Filtros
  document.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      setActiveFilter(btn.dataset.filter);
    });
  });

  // Formulário nova tarefa
  elements.newTaskForm.addEventListener("submit", handleCreateTask);

  // Formulário edição
  elements.editTaskForm.addEventListener("submit", handleEditTask);

  // Modal
  document
    .getElementById("close-modal")
    .addEventListener("click", closeEditModal);
  document
    .getElementById("cancel-edit")
    .addEventListener("click", closeEditModal);

  // Toast
  document.querySelector(".toast-close").addEventListener("click", hideToast);

  // Smooth scrolling
  setupSmoothScrolling();
}

// Carregar tarefas da API
async function loadTasks() {
  try {
    showLoading(true);

    const response = await fetch(API_ENDPOINTS.tarefas);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    tasks = data.tarefas || [];

    renderTasks();
    showLoading(false);
  } catch (error) {
    showLoading(false);
    throw error;
  }
}

// Renderizar lista de tarefas
function renderTasks() {
  if (tasks.length === 0) {
    elements.tasksList.style.display = "none";
    elements.noTasks.style.display = "block";
    return;
  }

  elements.noTasks.style.display = "none";
  elements.tasksList.style.display = "block";

  const filteredTasks = filterTasks(tasks, currentFilter);

  elements.tasksList.innerHTML = filteredTasks
    .map(
      (task) => `
    <div class="task-item ${task.status}" data-id="${task.id}">
      <div class="task-header">
        <div>
          <h3 class="task-title">${escapeHtml(task.titulo)}</h3>
          <span class="task-status ${task.status}">${task.status}</span>
        </div>
      </div>
      
      ${
        task.descricao
          ? `<p class="task-description">${escapeHtml(task.descricao)}</p>`
          : ""
      }
      
      <div class="task-actions">
        <button class="task-btn btn-edit" onclick="openEditModal(${task.id})">
          ✏️ Editar
        </button>
        <button class="task-btn btn-toggle" onclick="toggleTaskStatus(${
          task.id
        })">
          ${task.status === "pendente" ? "✅ Concluir" : "🔄 Reabrir"}
        </button>
        <button class="task-btn btn-delete" onclick="deleteTask(${task.id})">
          🗑️ Excluir
        </button>
      </div>
    </div>
  `
    )
    .join("");
}

// Filtrar tarefas
function filterTasks(tasks, filter) {
  switch (filter) {
    case "pendentes":
      return tasks.filter((task) => task.status === "pendente");
    case "concluidas":
      return tasks.filter((task) => task.status === "concluida");
    default:
      return tasks;
  }
}

// Definir filtro ativo
function setActiveFilter(filter) {
  currentFilter = filter;

  // Atualizar botões
  document.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.filter === filter);
  });

  renderTasks();
}

// Criar nova tarefa
async function handleCreateTask(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const taskData = {
    titulo: formData.get("titulo"),
    descricao: formData.get("descricao") || "",
    status: formData.get("status"),
  };

  try {
    const submitBtn = event.target.querySelector(".submit-btn");
    const btnText = submitBtn.querySelector(".btn-text");
    const btnLoading = submitBtn.querySelector(".btn-loading");

    // Mostrar loading
    btnText.style.display = "none";
    btnLoading.style.display = "inline";
    submitBtn.disabled = true;

    const response = await fetch(API_ENDPOINTS.tarefas, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const newTask = await response.json();
    tasks.push(newTask);

    renderTasks();
    updateStatistics();
    event.target.reset();

    showToast("Tarefa criada com sucesso!", "success");
  } catch (error) {
    showToast("Erro ao criar tarefa", "error");
    console.error("Erro ao criar tarefa:", error);
  } finally {
    // Restaurar botão
    const submitBtn = event.target.querySelector(".submit-btn");
    const btnText = submitBtn.querySelector(".btn-text");
    const btnLoading = submitBtn.querySelector(".btn-loading");

    btnText.style.display = "inline";
    btnLoading.style.display = "none";
    submitBtn.disabled = false;
  }
}

// Abrir modal de edição
function openEditModal(taskId) {
  const task = tasks.find((t) => t.id === taskId);
  if (!task) return;

  // Preencher formulário
  document.getElementById("edit-task-id").value = task.id;
  document.getElementById("edit-task-title").value = task.titulo;
  document.getElementById("edit-task-description").value = task.descricao || "";
  document.getElementById("edit-task-status").value = task.status;

  // Mostrar modal
  elements.editModal.style.display = "flex";
}

// Fechar modal de edição
function closeEditModal() {
  elements.editModal.style.display = "none";
}

// Editar tarefa
async function handleEditTask(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const taskId = parseInt(formData.get("id"));
  const taskData = {
    titulo: formData.get("titulo"),
    descricao: formData.get("descricao") || "",
    status: formData.get("status"),
  };

  try {
    const response = await fetch(`${API_ENDPOINTS.tarefas}/${taskId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const updatedTask = await response.json();

    // Atualizar tarefa na lista
    const index = tasks.findIndex((t) => t.id === taskId);
    if (index !== -1) {
      tasks[index] = updatedTask;
    }

    renderTasks();
    updateStatistics();
    closeEditModal();

    showToast("Tarefa atualizada com sucesso!", "success");
  } catch (error) {
    showToast("Erro ao atualizar tarefa", "error");
    console.error("Erro ao atualizar tarefa:", error);
  }
}

// Alternar status da tarefa
async function toggleTaskStatus(taskId) {
  const task = tasks.find((t) => t.id === taskId);
  if (!task) return;

  const newStatus = task.status === "pendente" ? "concluida" : "pendente";

  try {
    const response = await fetch(`${API_ENDPOINTS.tarefas}/${taskId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ...task,
        status: newStatus,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const updatedTask = await response.json();

    // Atualizar tarefa na lista
    const index = tasks.findIndex((t) => t.id === taskId);
    if (index !== -1) {
      tasks[index] = updatedTask;
    }

    renderTasks();
    updateStatistics();

    showToast(`Tarefa marcada como ${newStatus}!`, "success");
  } catch (error) {
    showToast("Erro ao atualizar status", "error");
    console.error("Erro ao atualizar status:", error);
  }
}

// Excluir tarefa
async function deleteTask(taskId) {
  if (!confirm("Tem certeza que deseja excluir esta tarefa?")) {
    return;
  }

  try {
    const response = await fetch(`${API_ENDPOINTS.tarefas}/${taskId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    // Remover tarefa da lista
    tasks = tasks.filter((t) => t.id !== taskId);

    renderTasks();
    updateStatistics();

    showToast("Tarefa excluída com sucesso!", "success");
  } catch (error) {
    showToast("Erro ao excluir tarefa", "error");
    console.error("Erro ao excluir tarefa:", error);
  }
}

// Atualizar estatísticas
function updateStatistics() {
  const total = tasks.length;
  const pendentes = tasks.filter((t) => t.status === "pendente").length;
  const concluidas = tasks.filter((t) => t.status === "concluida").length;
  const progress = total > 0 ? Math.round((concluidas / total) * 100) : 0;

  // Atualizar contadores
  elements.totalTarefas.textContent = total;
  elements.tarefasPendentes.textContent = pendentes;
  elements.tarefasConcluidas.textContent = concluidas;

  // Atualizar barra de progresso
  elements.progressFill.style.width = `${progress}%`;
  elements.progressText.textContent = `${progress}% concluído`;

  // Atualizar produtividade (simulado)
  const productivity = Math.round(total / 7); // Média por dia
  elements.productivity.textContent = `${productivity} tarefas/dia`;

  // Atualizar meta diária
  const dailyGoal = Math.min(pendentes, 5);
  elements.dailyGoal.textContent = `${dailyGoal}/5 tarefas`;
}

// Mostrar/esconder loading
function showLoading(show) {
  elements.loading.style.display = show ? "block" : "none";
}

// Mostrar toast
function showToast(message, type = "info") {
  elements.toastMessage.textContent = message;
  elements.toast.className = `toast ${type}`;
  elements.toast.style.display = "flex";

  // Auto-hide após 5 segundos
  setTimeout(hideToast, 5000);
}

// Esconder toast
function hideToast() {
  elements.toast.style.display = "none";
}

// Setup smooth scrolling
function setupSmoothScrolling() {
  const links = document.querySelectorAll('a[href^="#"]');

  links.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      const targetId = this.getAttribute("href");
      const targetSection = document.querySelector(targetId);

      if (targetSection) {
        const headerHeight = document.querySelector(".header").offsetHeight;
        const targetPosition = targetSection.offsetTop - headerHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: "smooth",
        });
      }
    });
  });
}

// Utilitário para escapar HTML
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Testar conexão com a API
async function testAPIConnection() {
  try {
    const response = await fetch(API_ENDPOINTS.tarefas);
    if (response.ok) {
      console.log("✅ API está funcionando!");
      return true;
    } else {
      throw new Error("API não está respondendo");
    }
  } catch (error) {
    console.log("❌ Erro ao conectar com a API:", error.message);
    console.log(
      "💡 Certifique-se de que a API está rodando em http://localhost:5000"
    );
    return false;
  }
}

// Testar conexão quando a página carregar
window.addEventListener("load", function () {
  setTimeout(testAPIConnection, 1000);
});
