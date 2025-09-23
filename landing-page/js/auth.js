// Configuração da API
const API_BASE = "http://localhost:5000";

// Elementos do DOM
const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const twofaForm = document.getElementById("2fa-form");
const tabs = document.querySelectorAll(".tab");
const tabContents = document.querySelectorAll(".tab-content");

// Estado da aplicação
let currentUser = null;
let authToken = null;

// Inicialização
document.addEventListener("DOMContentLoaded", function () {
  // Verificar se já está logado
  const savedToken = localStorage.getItem("auth_token");
  if (savedToken) {
    verifyToken(savedToken);
  }

  // Configurar tabs
  setupTabs();

  // Configurar formulários
  setupForms();
});

// Configurar sistema de tabs
function setupTabs() {
  tabs.forEach((tab) => {
    tab.addEventListener("click", function () {
      const tabName = this.dataset.tab;
      switchTab(tabName);
    });
  });
}

function switchTab(tabName) {
  // Remover classe active de todas as tabs
  tabs.forEach((tab) => tab.classList.remove("active"));
  tabContents.forEach((content) => content.classList.remove("active"));

  // Ativar tab selecionada
  document.querySelector(`[data-tab="${tabName}"]`).classList.add("active");
  document.getElementById(`${tabName}-tab`).classList.add("active");

  // Limpar mensagens de erro
  clearMessages();
}

// Configurar formulários
function setupForms() {
  // Login
  loginForm.addEventListener("submit", handleLogin);

  // Registro
  registerForm.addEventListener("submit", handleRegister);

  // 2FA
  twofaForm.addEventListener("submit", handle2FA);
}

// Função de login
async function handleLogin(e) {
  e.preventDefault();

  const formData = new FormData(loginForm);
  const data = {
    email: formData.get("email"),
    senha: formData.get("senha"),
  };

  showLoading("login");
  clearMessages();

  try {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok) {
      // Login bem-sucedido
      authToken = result.token;
      currentUser = result.usuario;

      // Salvar token no localStorage
      localStorage.setItem("auth_token", authToken);
      localStorage.setItem("current_user", JSON.stringify(currentUser));

      // Verificar se precisa configurar 2FA
      if (result.qr_code_url) {
        show2FASetup(result.qr_code_url);
      } else {
        // Redirecionar para o app
        window.location.href = "index.html";
      }
    } else {
      showError("login", result.message || "Erro ao fazer login");
    }
  } catch (error) {
    showError("login", "Erro de conexão. Verifique se a API está rodando.");
  } finally {
    hideLoading("login");
  }
}

// Função de registro
async function handleRegister(e) {
  e.preventDefault();

  const formData = new FormData(registerForm);
  const data = {
    nome: formData.get("nome"),
    email: formData.get("email"),
    senha: formData.get("senha"),
  };

  showLoading("register");
  clearMessages();

  try {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok) {
      showSuccess(
        "register",
        "Usuário criado com sucesso! Faça login para continuar."
      );
      switchTab("login");
      registerForm.reset();
    } else {
      showError("register", result.message || "Erro ao criar usuário");
    }
  } catch (error) {
    showError("register", "Erro de conexão. Verifique se a API está rodando.");
  } finally {
    hideLoading("register");
  }
}

// Função de verificação 2FA
async function handle2FA(e) {
  e.preventDefault();

  const formData = new FormData(twofaForm);
  const codigo = formData.get("codigo");

  showLoading("2fa");
  clearMessages();

  try {
    const response = await fetch(`${API_BASE}/auth/verify-2fa`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      body: JSON.stringify({ codigo }),
    });

    const result = await response.json();

    if (response.ok) {
      showSuccess("2fa", "2FA configurado com sucesso!");
      setTimeout(() => {
        window.location.href = "index.html";
      }, 1500);
    } else {
      showError("2fa", result.message || "Código inválido");
    }
  } catch (error) {
    showError("2fa", "Erro de conexão");
  } finally {
    hideLoading("2fa");
  }
}

// Verificar token salvo
async function verifyToken(token) {
  try {
    const response = await fetch(`${API_BASE}/auth/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.ok) {
      const user = await response.json();
      currentUser = user;
      authToken = token;
      // Redirecionar para o app
      window.location.href = "index.html";
    } else {
      // Token inválido, limpar localStorage
      localStorage.removeItem("auth_token");
      localStorage.removeItem("current_user");
    }
  } catch (error) {
    console.error("Erro ao verificar token:", error);
  }
}

// Mostrar configuração 2FA
function show2FASetup(qrCodeUrl) {
  switchTab("2fa");

  const qrContainer = document.getElementById("qr-code-container");
  qrContainer.innerHTML = `
        <img src="${API_BASE}${qrCodeUrl}" alt="QR Code para 2FA">
        <p>Escaneie com o Google Authenticator</p>
    `;
}

// Funções de UI
function showLoading(formType) {
  const loading = document.getElementById(`${formType}-loading`);
  const button = document.getElementById(`${formType}-btn`);

  if (loading) loading.style.display = "block";
  if (button) button.disabled = true;
}

function hideLoading(formType) {
  const loading = document.getElementById(`${formType}-loading`);
  const button = document.getElementById(`${formType}-btn`);

  if (loading) loading.style.display = "none";
  if (button) button.disabled = false;
}

function showError(formType, message) {
  const errorDiv = document.getElementById(`${formType}-error`);
  if (errorDiv) {
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
  }
}

function showSuccess(formType, message) {
  const successDiv = document.getElementById(`${formType}-success`);
  if (successDiv) {
    successDiv.textContent = message;
    successDiv.style.display = "block";
  }
}

function clearMessages() {
  const messages = document.querySelectorAll(
    ".error-message, .success-message"
  );
  messages.forEach((msg) => {
    msg.style.display = "none";
    msg.textContent = "";
  });
}

// Função de logout
function logout() {
  if (authToken) {
    fetch(`${API_BASE}/auth/logout`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    }).catch(console.error);
  }

  // Limpar dados locais
  localStorage.removeItem("auth_token");
  localStorage.removeItem("current_user");
  authToken = null;
  currentUser = null;

  // Redirecionar para login
  window.location.href = "login.html";
}

// Exportar funções para uso global
window.logout = logout;
window.getAuthToken = () => authToken;
window.getCurrentUser = () => currentUser;
