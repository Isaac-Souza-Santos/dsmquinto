// Configuração da API
const API_BASE_URL = "http://127.0.0.1:5000";
const API_ENDPOINTS = {
  tarefas: `${API_BASE_URL}/tarefas/`,
};

// Estado de autenticação
let authToken = null;
let currentUser = null;

// Função auxiliar para construir URLs corretamente
function buildApiUrl(endpoint, id = null) {
  if (id !== null) {
    // Remove a barra final do endpoint e adiciona o ID
    return endpoint.replace(/\/$/, "") + "/" + id;
  }
  return endpoint;
}

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
  // Verificar autenticação primeiro
  checkAuthentication();
  setupEventListeners();
});

// Verificar se usuário está autenticado
function checkAuthentication() {
  const savedToken = localStorage.getItem("auth_token");
  const savedUser = localStorage.getItem("current_user");

  if (savedToken && savedUser) {
    authToken = savedToken;
    currentUser = JSON.parse(savedUser);
    initializeApp();
  } else {
    // Redirecionar para login
    window.location.href = "login.html";
  }
}

// Inicializar aplicação
async function initializeApp() {
  try {
    // Verificar se o token ainda é válido
    if (!authToken) {
      window.location.href = "login.html";
      return;
    }

    await loadTasks();
    updateStatistics();
  } catch (error) {
    // Se erro 401, redirecionar para login
    if (error.message.includes("401")) {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("current_user");
      window.location.href = "login.html";
      return;
    }

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

    const response = await fetch(API_ENDPOINTS.tarefas, {
      method: "GET",
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      mode: "cors",
      credentials: "same-origin",
    });
    if (!response.ok) {
      if (response.status === 401) {
        throw new Error(`401: Token inválido ou expirado`);
      }
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
    .map((task) => {
      // Validar e normalizar o status da tarefa
      const status =
        task.status && ["pendente", "concluida"].includes(task.status)
          ? task.status
          : "pendente";

      return `
    <div class="task-item ${status}" data-id="${task.id}">
      <div class="task-header">
        <h3 class="task-title">${escapeHtml(task.titulo)}</h3>
        <span class="task-status ${status}">${status}</span>
      </div>
      
      ${
        task.descricao
          ? `<p class="task-description">${escapeHtml(task.descricao)}</p>`
          : ""
      }
      
      <div class="task-actions">
        <button class="task-btn btn-edit" onclick="openEditModal(${task.id})">
          <i class="fas fa-edit"></i>
          Editar
        </button>
        <button class="task-btn btn-toggle" onclick="toggleTaskStatus(${
          task.id
        })">
          <i class="fas fa-${status === "pendente" ? "check" : "undo"}"></i>
          ${status === "pendente" ? "Concluir" : "Reabrir"}
        </button>
        <button class="task-btn btn-delete" onclick="deleteTask(${task.id})">
          <i class="fas fa-trash"></i>
          Excluir
        </button>
      </div>
    </div>
  `;
    })
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
  const status = formData.get("status");

  // Validar e normalizar o status
  const validStatus =
    status && ["pendente", "concluida"].includes(status) ? status : "pendente";

  const taskData = {
    titulo: formData.get("titulo"),
    descricao: formData.get("descricao") || "",
    status: validStatus,
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
        Accept: "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      mode: "cors",
      credentials: "same-origin",
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
    const response = await fetch(buildApiUrl(API_ENDPOINTS.tarefas, taskId), {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      mode: "cors",
      credentials: "same-origin",
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
    const response = await fetch(buildApiUrl(API_ENDPOINTS.tarefas, taskId), {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      mode: "cors",
      credentials: "same-origin",
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
    const response = await fetch(buildApiUrl(API_ENDPOINTS.tarefas, taskId), {
      method: "DELETE",
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      mode: "cors",
      credentials: "same-origin",
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

  // Atualizar porcentagem de progresso
  const progressElement = document.getElementById("progress-percentage");
  if (progressElement) {
    progressElement.textContent = `${progress}%`;
  }

  // Atualizar contador de tarefas
  const tasksCountElement = document.getElementById("tasks-count");
  if (tasksCountElement) {
    const count =
      currentFilter === "todas"
        ? total
        : currentFilter === "pendentes"
        ? pendentes
        : concluidas;
    tasksCountElement.textContent = `${count} tarefa${count !== 1 ? "s" : ""}`;
  }

  // Atualizar nome do usuário
  const userNameElement = document.getElementById("user-name");
  if (userNameElement && currentUser) {
    userNameElement.textContent = currentUser.nome || "Usuário";
  }
}

// Mostrar/esconder loading
function showLoading(show) {
  elements.loading.style.display = show ? "block" : "none";
}

// Mostrar toast
function showToast(message, type = "info") {
  const toastIcon = elements.toast.querySelector(".toast-icon i");

  // Definir ícone baseado no tipo
  switch (type) {
    case "success":
      toastIcon.className = "fas fa-check-circle";
      break;
    case "error":
      toastIcon.className = "fas fa-exclamation-circle";
      break;
    default:
      toastIcon.className = "fas fa-info-circle";
  }

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

// Setup smooth scrolling e navegação
function setupSmoothScrolling() {
  const links = document.querySelectorAll('a[href^="#"]');
  const navLinks = document.querySelectorAll(".nav-link");

  links.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      const targetId = this.getAttribute("href");
      const targetSection = document.querySelector(targetId);

      if (targetSection) {
        // Atualizar link ativo
        navLinks.forEach((nav) => nav.classList.remove("active"));
        const activeNav = document.querySelector(`[href="${targetId}"]`);
        if (activeNav) {
          activeNav.classList.add("active");
        }

        // Scroll suave
        const headerHeight = document.querySelector(".header").offsetHeight;
        const targetPosition = targetSection.offsetTop - headerHeight - 20;

        window.scrollTo({
          top: targetPosition,
          behavior: "smooth",
        });
      }
    });
  });

  // Scroll spy para atualizar navegação
  window.addEventListener("scroll", () => {
    const sections = document.querySelectorAll("section[id]");
    const scrollPos = window.scrollY + 100;

    sections.forEach((section) => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      const sectionId = section.getAttribute("id");

      if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
        navLinks.forEach((nav) => nav.classList.remove("active"));
        const activeNav = document.querySelector(`[href="#${sectionId}"]`);
        if (activeNav) {
          activeNav.classList.add("active");
        }
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
    console.log("🔍 Testando conexão com a API...");
    console.log("📍 URL da API:", API_ENDPOINTS.tarefas);

    const response = await fetch(API_ENDPOINTS.tarefas, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      mode: "cors",
      credentials: "same-origin",
    });

    if (response.ok) {
      console.log("✅ API está funcionando!");
      console.log("📊 Status:", response.status);
      console.log(
        "🔗 Headers:",
        Object.fromEntries(response.headers.entries())
      );
      return true;
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
  } catch (error) {
    console.log("❌ Erro ao conectar com a API:", error.message);
    console.log("💡 Possíveis soluções:");
    console.log("   1. Certifique-se de que a API está rodando");
    console.log("   2. Execute: python main.py");
    console.log("   3. Verifique se a porta 5000 está livre");
    console.log("   4. Verifique se o Flask-CORS está instalado");
    console.log("📍 URL tentada:", API_ENDPOINTS.tarefas);
    return false;
  }
}

// Testar conexão quando a página carregar
window.addEventListener("load", function () {
  setTimeout(testAPIConnection, 1000);
});

// Função de logout global
function logout() {
  // Limpar dados locais
  localStorage.removeItem("auth_token");
  localStorage.removeItem("current_user");
  authToken = null;
  currentUser = null;

  // Redirecionar para login
  window.location.href = "login.html";
}

// Exportar função de logout para uso global
window.logout = logout;
