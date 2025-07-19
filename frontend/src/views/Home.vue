<template>
  <div class="home">
    <div class="hero-section">
      <div class="container">
        <h1 class="title">🔐 SecureMail Analyzer</h1>
        <p class="subtitle">
          Ein sicheres, webbasiertes Tool für E-Mail-Sicherheitsanalyse mit KI-gestützter Bedrohungserkennung
        </p>
        <div class="features">
          <div class="feature">
            <i class="pi pi-shield"></i>
            <h3>Multi-IMAP-Support</h3>
            <p>Mehrere Mailkonten pro Nutzer</p>
          </div>
          <div class="feature">
            <i class="pi pi-brain"></i>
            <h3>KI-gestützte Analyse</h3>
            <p>OpenRouter API + lokale LLM-Unterstützung</p>
          </div>
          <div class="feature">
            <i class="pi pi-exclamation-triangle"></i>
            <h3>Sicherheitsanalyse</h3>
            <p>Spam, Phishing, Malware-Erkennung</p>
          </div>
        </div>
        <div class="actions">
          <router-link to="/login" class="btn btn-primary">
            <i class="pi pi-sign-in"></i>
            Anmelden
          </router-link>
          <router-link to="/register" class="btn btn-secondary">
            <i class="pi pi-user-plus"></i>
            Registrieren
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-section {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
}

.container {
  max-width: 1200px;
  text-align: center;
  color: white;
}

.title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 1.3rem;
  margin-bottom: 3rem;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature i {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  display: block;
}

.feature h3 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.feature p {
  opacity: 0.8;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background: #45a049;
  transform: translateY(-2px);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .title {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1.1rem;
  }
  
  .features {
    grid-template-columns: 1fr;
  }
  
  .actions {
    flex-direction: column;
    align-items: center;
  }
}
</style> 