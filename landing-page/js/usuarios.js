// Configuração da API
const API_BASE_URL = "http://127.0.0.1:5000";
const API_ENDPOINTS = {
  usuarios: `${API_BASE_URL}/usuarios/`,
};

// Estado de autenticação
let authToken = null;
let currentUser = null;

// Estado global
let users = [];

// Função auxiliar para obter headers com autenticação
function getAuthHeaders(customHeaders = {}) {
  // Garantir que o token está carregado
  if (!authToken) {
    authToken = localStorage.getItem("auth_token");
  }

  const headers = {
    Accept: "application/json",
    ...customHeaders,
  };

  // Adicionar Authorization apenas se o token existir
  if (authToken) {
    headers.Authorization = `Bearer ${authToken}`;
  } else {
    console.warn("⚠️ Token não encontrado! A requisição pode falhar.");
  }

  return headers;
}

// Elementos DOM
const elements = {
  loading: document.getElementById("users-loading"),
  usersList: document.getElementById("users-list"),
  noUsers: document.getElementById("no-users"),
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

    // Verificar se é admin
    if (currentUser.nivel_acesso !== "administrativo") {
      showToast("Apenas administradores podem acessar esta página", "error");
      setTimeout(() => {
        window.location.href = "index.html";
      }, 2000);
      return;
    }

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

    // Atualizar informações do usuário
    updateUserInfo();

    // Carregar usuários
    await loadUsers();
  } catch (error) {
    // Se erro 401, redirecionar para login
    if (error.message.includes("401")) {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("current_user");
      window.location.href = "login.html";
      return;
    }

    showToast("Erro ao carregar usuários", "error");
    console.error("Erro na inicialização:", error);
  }
}

// Configurar event listeners
function setupEventListeners() {
  // Modal de alterar nível
  const changeRoleModal = document.getElementById("change-role-modal");
  if (changeRoleModal) {
    document
      .getElementById("close-role-modal")
      .addEventListener("click", () => {
        changeRoleModal.style.display = "none";
      });
    document
      .getElementById("cancel-role-change")
      .addEventListener("click", () => {
        changeRoleModal.style.display = "none";
      });
    document
      .getElementById("change-role-form")
      .addEventListener("submit", handleChangeRole);
  }

  // Toast
  const toastClose = document.querySelector(".toast-close");
  if (toastClose) {
    toastClose.addEventListener("click", hideToast);
  }
}

// Atualizar informações do usuário
function updateUserInfo() {
  const userNameElement = document.getElementById("user-name");
  if (userNameElement && currentUser) {
    userNameElement.textContent = currentUser.nome || "Usuário";
  }

  const userRoleElement = document.getElementById("user-role");
  if (userRoleElement && currentUser) {
    const nivelAcesso = currentUser.nivel_acesso || "visualizacao";
    const roleLabels = {
      visualizacao: "👤 Visualização",
      gerencial: "👔 Gerencial",
      administrativo: "🔐 Administrador",
    };
    userRoleElement.textContent = roleLabels[nivelAcesso] || nivelAcesso;
    userRoleElement.className = `user-role role-${nivelAcesso}`;
  }
}

// Carregar usuários da API
async function loadUsers() {
  try {
    const loadingElement = elements.loading;
    const usersListElement = elements.usersList;
    const noUsersElement = elements.noUsers;

    if (loadingElement) loadingElement.style.display = "block";
    if (usersListElement) usersListElement.style.display = "none";
    if (noUsersElement) noUsersElement.style.display = "none";

    const response = await fetch(API_ENDPOINTS.usuarios, {
      method: "GET",
      headers: getAuthHeaders(),
      mode: "cors",
      credentials: "same-origin",
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error(`401: Token inválido ou expirado`);
      }
      if (response.status === 403) {
        throw new Error(
          `403: Acesso negado. Apenas administradores podem gerenciar usuários.`
        );
      }
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    users = data.usuarios || [];

    renderUsers();
    updateStatistics();
    if (loadingElement) loadingElement.style.display = "none";
  } catch (error) {
    const loadingElement = elements.loading;
    if (loadingElement) loadingElement.style.display = "none";

    showToast(
      error.message.includes("403")
        ? "Apenas administradores podem gerenciar usuários"
        : "Erro ao carregar usuários",
      "error"
    );
    console.error("Erro ao carregar usuários:", error);
  }
}

// Renderizar lista de usuários
function renderUsers() {
  const usersListElement = elements.usersList;
  const noUsersElement = elements.noUsers;

  if (!usersListElement) return;

  if (users.length === 0) {
    usersListElement.style.display = "none";
    if (noUsersElement) noUsersElement.style.display = "block";
    return;
  }

  if (noUsersElement) noUsersElement.style.display = "none";
  usersListElement.style.display = "block";

  const roleLabels = {
    visualizacao: "👤 Visualização",
    gerencial: "👔 Gerencial",
    administrativo: "🔐 Administrador",
  };

  usersListElement.innerHTML = users
    .map((user) => {
      const roleLabel = roleLabels[user.nivel_acesso] || user.nivel_acesso;
      const isActive = user.ativo !== false;

      return `
    <div class="user-item ${!isActive ? "inactive" : ""}" data-id="${user.id}">
      <div class="user-item-header">
        <div class="user-item-info">
          <h3 class="user-item-name">${escapeHtml(user.nome)}</h3>
          <span class="user-item-email">${escapeHtml(user.email)}</span>
        </div>
        <span class="user-item-role role-${
          user.nivel_acesso
        }">${roleLabel}</span>
      </div>
      
      <div class="user-item-meta">
        <span class="user-item-status ${isActive ? "active" : "inactive"}">
          <i class="fas fa-circle"></i>
          ${isActive ? "Ativo" : "Inativo"}
        </span>
        <span class="user-item-date">
          <i class="fas fa-calendar"></i>
          ${new Date(user.data_criacao).toLocaleDateString("pt-BR")}
        </span>
      </div>
      
      <div class="user-item-actions">
        <button class="user-btn btn-change-role" onclick="openChangeRoleModal(${
          user.id
        })" ${!isActive ? "disabled" : ""}>
          <i class="fas fa-user-shield"></i>
          Alterar Nível
        </button>
      </div>
    </div>
  `;
    })
    .join("");
}

// Atualizar estatísticas
function updateStatistics() {
  const total = users.length;
  const active = users.filter((u) => u.ativo !== false).length;
  const admins = users.filter(
    (u) => u.nivel_acesso === "administrativo"
  ).length;
  const managers = users.filter((u) => u.nivel_acesso === "gerencial").length;

  const totalElement = document.getElementById("total-users");
  const activeElement = document.getElementById("active-users");
  const adminElement = document.getElementById("admin-users");
  const managerElement = document.getElementById("manager-users");

  if (totalElement) totalElement.textContent = total;
  if (activeElement) activeElement.textContent = active;
  if (adminElement) adminElement.textContent = admins;
  if (managerElement) managerElement.textContent = managers;
}

// Abrir modal de alterar nível
function openChangeRoleModal(userId) {
  const user = users.find((u) => u.id === userId);
  if (!user) return;

  const modal = document.getElementById("change-role-modal");
  const form = document.getElementById("change-role-form");
  if (!modal || !form) return;

  document.getElementById("change-role-user-id").value = user.id;
  document.getElementById("change-role-name").value = user.nome;
  document.getElementById("change-role-email").value = user.email;
  document.getElementById("change-role-level").value = user.nivel_acesso;

  modal.style.display = "flex";
}

// Alterar nível de acesso
async function handleChangeRole(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const userId = parseInt(formData.get("id"));
  const nivelAcesso = formData.get("nivel_acesso");

  try {
    const response = await fetch(`${API_ENDPOINTS.usuarios}${userId}/nivel`, {
      method: "PUT",
      headers: getAuthHeaders({
        "Content-Type": "application/json",
      }),
      mode: "cors",
      credentials: "same-origin",
      body: JSON.stringify({ nivel_acesso: nivelAcesso }),
    });

    if (!response.ok) {
      if (response.status === 403) {
        throw new Error(
          "Apenas administradores podem alterar níveis de acesso"
        );
      }
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const result = await response.json();

    // Atualizar usuário na lista
    const index = users.findIndex((u) => u.id === userId);
    if (index !== -1) {
      users[index].nivel_acesso = nivelAcesso;
    }

    renderUsers();
    updateStatistics();
    document.getElementById("change-role-modal").style.display = "none";

    showToast("Nível de acesso alterado com sucesso!", "success");
  } catch (error) {
    showToast(error.message || "Erro ao alterar nível de acesso", "error");
    console.error("Erro ao alterar nível:", error);
  }
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

// Utilitário para escapar HTML
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

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

// Exportar funções para uso global
window.loadUsers = loadUsers;
window.openChangeRoleModal = openChangeRoleModal;
window.logout = logout;
