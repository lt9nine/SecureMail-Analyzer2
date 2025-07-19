<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <h1>📊 Dashboard</h1>
        <div class="user-menu">
          <span>Willkommen, {{ userName }}</span>
          <button @click="logout" class="btn-logout">
            <i class="pi pi-sign-out"></i>
            Abmelden
          </button>
        </div>
      </div>
    </header>
    
    <main class="dashboard-main">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <i class="pi pi-envelope"></i>
          </div>
          <div class="stat-content">
            <h3>{{ totalEmails }}</h3>
            <p>Gesamte E-Mails</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon warning">
            <i class="pi pi-exclamation-triangle"></i>
          </div>
          <div class="stat-content">
            <h3>{{ suspiciousEmails }}</h3>
            <p>Verdächtige E-Mails</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon danger">
            <i class="pi pi-times-circle"></i>
          </div>
          <div class="stat-content">
            <h3>{{ blockedEmails }}</h3>
            <p>Blockierte E-Mails</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon success">
            <i class="pi pi-check-circle"></i>
          </div>
          <div class="stat-content">
            <h3>{{ safeEmails }}</h3>
            <p>Sichere E-Mails</p>
          </div>
        </div>
      </div>
      
      <div class="dashboard-content">
        <div class="content-section">
          <h2>📬 Letzte E-Mails</h2>
          <div class="email-list">
            <div v-for="email in recentEmails" :key="email.id" class="email-item" @click="viewEmail(email.id)">
              <div class="email-status" :class="email.riskLevel">
                <i :class="getRiskIcon(email.riskLevel)"></i>
              </div>
              <div class="email-info">
                <h4>{{ email.subject }}</h4>
                <p>{{ email.from }}</p>
                <span class="email-date">{{ formatDate(email.date) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="content-section">
          <h2>⚙️ Schnellaktionen</h2>
          <div class="action-buttons">
            <router-link to="/emails" class="action-btn">
              <i class="pi pi-envelope"></i>
              Alle E-Mails anzeigen
            </router-link>
            <router-link to="/settings" class="action-btn">
              <i class="pi pi-cog"></i>
              Einstellungen
            </router-link>
            <button class="action-btn" @click="syncEmails">
              <i class="pi pi-refresh"></i>
              E-Mails synchronisieren
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      userName: 'Benutzer',
      totalEmails: 0,
      suspiciousEmails: 0,
      blockedEmails: 0,
      safeEmails: 0,
      recentEmails: []
    }
  },
  mounted() {
    this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      // TODO: Load real data from API
      this.totalEmails = 1250
      this.suspiciousEmails = 23
      this.blockedEmails = 8
      this.safeEmails = 1219
      
      this.recentEmails = [
        {
          id: 1,
          subject: 'Wichtige Sicherheitswarnung',
          from: 'security@company.com',
          date: new Date(),
          riskLevel: 'high'
        },
        {
          id: 2,
          subject: 'Newsletter - März 2024',
          from: 'newsletter@example.com',
          date: new Date(Date.now() - 86400000),
          riskLevel: 'low'
        },
        {
          id: 3,
          subject: 'Ihr Konto wurde kompromittiert',
          from: 'support@fake-bank.com',
          date: new Date(Date.now() - 172800000),
          riskLevel: 'critical'
        }
      ]
    },
    
    getRiskIcon(riskLevel) {
      const icons = {
        low: 'pi pi-check-circle',
        medium: 'pi pi-exclamation-triangle',
        high: 'pi pi-times-circle',
        critical: 'pi pi-ban'
      }
      return icons[riskLevel] || 'pi pi-question-circle'
    },
    
    formatDate(date) {
      return new Intl.DateTimeFormat('de-DE', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    },
    
    viewEmail(emailId) {
      this.$router.push(`/emails/${emailId}`)
    },
    
    async syncEmails() {
      // TODO: Implement email sync
      console.log('Syncing emails...')
    },
    
    logout() {
      // TODO: Implement logout
      localStorage.removeItem('access_token')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f8f9fa;
}

.dashboard-header {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.header-content h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-logout {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-logout:hover {
  background: #c82333;
}

.dashboard-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #667eea;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.stat-icon.warning {
  background: #ffc107;
}

.stat-icon.danger {
  background: #dc3545;
}

.stat-icon.success {
  background: #28a745;
}

.stat-content h3 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  color: #333;
}

.stat-content p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.content-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.content-section h2 {
  margin: 0 0 1rem 0;
  font-size: 1.3rem;
  color: #333;
}

.email-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.email-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e1e5e9;
  cursor: pointer;
  transition: all 0.3s ease;
}

.email-item:hover {
  background: #f8f9fa;
  border-color: #667eea;
}

.email-status {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.email-status.low {
  background: #d4edda;
  color: #155724;
}

.email-status.medium {
  background: #fff3cd;
  color: #856404;
}

.email-status.high {
  background: #f8d7da;
  color: #721c24;
}

.email-status.critical {
  background: #f5c6cb;
  color: #721c24;
}

.email-info {
  flex: 1;
}

.email-info h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  color: #333;
}

.email-info p {
  margin: 0 0 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.email-date {
  font-size: 0.8rem;
  color: #999;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
  background: #f8f9fa;
  border: 1px solid #e1e5e9;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.action-btn:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

@media (max-width: 768px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
}
</style> 