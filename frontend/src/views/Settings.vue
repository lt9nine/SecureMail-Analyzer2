<template>
  <div class="settings-page">
    <header class="page-header">
      <div class="header-content">
        <h1>⚙️ Einstellungen</h1>
      </div>
    </header>
    
    <main class="settings-main">
      <div class="settings-container">
        <div class="settings-section">
          <h2>👤 Profil</h2>
          <form @submit.prevent="updateProfile" class="settings-form">
            <div class="form-group">
              <label for="name">Vollständiger Name</label>
              <input 
                type="text" 
                id="name" 
                v-model="profile.name" 
                required 
              />
            </div>
            
            <div class="form-group">
              <label for="email">E-Mail</label>
              <input 
                type="email" 
                id="email" 
                v-model="profile.email" 
                required 
              />
            </div>
            
            <button type="submit" class="btn-save" :disabled="saving">
              <span v-if="saving">Speichern...</span>
              <span v-else>Profil speichern</span>
            </button>
          </form>
        </div>
        
        <div class="settings-section">
          <h2>🔐 Passwort ändern</h2>
          <form @submit.prevent="changePassword" class="settings-form">
            <div class="form-group">
              <label for="currentPassword">Aktuelles Passwort</label>
              <input 
                type="password" 
                id="currentPassword" 
                v-model="passwordForm.currentPassword" 
                required 
              />
            </div>
            
            <div class="form-group">
              <label for="newPassword">Neues Passwort</label>
              <input 
                type="password" 
                id="newPassword" 
                v-model="passwordForm.newPassword" 
                required 
                minlength="8"
              />
            </div>
            
            <div class="form-group">
              <label for="confirmPassword">Neues Passwort bestätigen</label>
              <input 
                type="password" 
                id="confirmPassword" 
                v-model="passwordForm.confirmPassword" 
                required 
              />
            </div>
            
            <button type="submit" class="btn-save" :disabled="changingPassword || !passwordsMatch">
              <span v-if="changingPassword">Ändern...</span>
              <span v-else>Passwort ändern</span>
            </button>
          </form>
        </div>
        
        <div class="settings-section">
          <h2>📧 E-Mail-Konten</h2>
          <div class="mail-accounts">
            <div v-for="account in mailAccounts" :key="account.id" class="account-item">
              <div class="account-info">
                <h4>{{ account.email }}</h4>
                <p>{{ account.host }}:{{ account.port }}</p>
                <span class="account-status" :class="account.status">
                  {{ account.status === 'connected' ? 'Verbunden' : 'Getrennt' }}
                </span>
              </div>
              <div class="account-actions">
                <button @click="editAccount(account)" class="btn-edit">
                  <i class="pi pi-pencil"></i>
                </button>
                <button @click="deleteAccount(account.id)" class="btn-delete">
                  <i class="pi pi-trash"></i>
                </button>
              </div>
            </div>
            
            <button @click="addAccount" class="btn-add-account">
              <i class="pi pi-plus"></i>
              E-Mail-Konto hinzufügen
            </button>
          </div>
        </div>
        
        <div class="settings-section">
          <h2>🤖 KI-Einstellungen</h2>
          <div class="ai-settings">
            <div class="form-group">
              <label for="aiProvider">KI-Provider</label>
              <select id="aiProvider" v-model="aiSettings.provider">
                <option value="openrouter">OpenRouter (Empfohlen)</option>
                <option value="ollama">Ollama (Lokal)</option>
              </select>
            </div>
            
            <div v-if="aiSettings.provider === 'openrouter'" class="form-group">
              <label for="openrouterKey">OpenRouter API Key</label>
              <input 
                type="password" 
                id="openrouterKey" 
                v-model="aiSettings.openrouterKey" 
                placeholder="sk-or-..."
              />
            </div>
            
            <div v-if="aiSettings.provider === 'ollama'" class="form-group">
              <label for="ollamaUrl">Ollama URL</label>
              <input 
                type="url" 
                id="ollamaUrl" 
                v-model="aiSettings.ollamaUrl" 
                placeholder="http://localhost:11434"
              />
            </div>
            
            <button @click="saveAISettings" class="btn-save" :disabled="savingAI">
              <span v-if="savingAI">Speichern...</span>
              <span v-else>KI-Einstellungen speichern</span>
            </button>
          </div>
        </div>
        

      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Settings',
  data() {
    return {
      saving: false,
      changingPassword: false,
      savingAI: false,
      profile: {
        name: 'Max Mustermann',
        email: 'max.mustermann@example.com'
      },
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      mailAccounts: [
        {
          id: 1,
          email: 'max.mustermann@example.com',
          host: 'imap.example.com',
          port: 993,
          status: 'connected'
        },
        {
          id: 2,
          email: 'max@company.com',
          host: 'imap.company.com',
          port: 993,
          status: 'disconnected'
        }
      ],
      aiSettings: {
        provider: 'openrouter',
        openrouterKey: '',
        ollamaUrl: 'http://localhost:11434'
      }
    }
  },
  computed: {
    passwordsMatch() {
      return this.passwordForm.newPassword && 
             this.passwordForm.confirmPassword && 
             this.passwordForm.newPassword === this.passwordForm.confirmPassword
    }
  },
  methods: {
    async updateProfile() {
      this.saving = true
      try {
        // TODO: Implement profile update
        await new Promise(resolve => setTimeout(resolve, 1000))
        console.log('Profile updated:', this.profile)
      } catch (error) {
        console.error('Failed to update profile:', error)
      } finally {
        this.saving = false
      }
    },
    
    async changePassword() {
      if (!this.passwordsMatch) {
        alert('Passwörter stimmen nicht überein')
        return
      }
      
      this.changingPassword = true
      try {
        // TODO: Implement password change
        await new Promise(resolve => setTimeout(resolve, 1000))
        console.log('Password changed')
        this.passwordForm = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
      } catch (error) {
        console.error('Failed to change password:', error)
      } finally {
        this.changingPassword = false
      }
    },
    
    addAccount() {
      // TODO: Implement add account modal/form
      console.log('Add account')
    },
    
    editAccount(account) {
      // TODO: Implement edit account modal/form
      console.log('Edit account:', account)
    },
    
    async deleteAccount(accountId) {
      if (confirm('Möchten Sie dieses E-Mail-Konto wirklich löschen?')) {
        // TODO: Implement delete account
        console.log('Delete account:', accountId)
        this.mailAccounts = this.mailAccounts.filter(account => account.id !== accountId)
      }
    },
    
    async saveAISettings() {
      this.savingAI = true
      try {
        // TODO: Implement AI settings save
        await new Promise(resolve => setTimeout(resolve, 1000))
        console.log('AI settings saved:', this.aiSettings)
      } catch (error) {
        console.error('Failed to save AI settings:', error)
      } finally {
        this.savingAI = false
      }
    },
    

  }
}
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
  background: #f8f9fa;
}

.page-header {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
}

.header-content h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.settings-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.settings-container {
  display: grid;
  gap: 2rem;
}

.settings-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.settings-section h2 {
  margin: 0 0 1.5rem 0;
  font-size: 1.3rem;
  color: #333;
  border-bottom: 2px solid #e1e5e9;
  padding-bottom: 0.5rem;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.btn-save {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: flex-start;
}

.btn-save:hover:not(:disabled) {
  background: #5a6fd8;
  transform: translateY(-1px);
}

.btn-save:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.mail-accounts {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.account-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  background: #f8f9fa;
}

.account-info h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  color: #333;
}

.account-info p {
  margin: 0 0 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.account-status {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
}

.account-status.connected {
  background: #d4edda;
  color: #155724;
}

.account-status.disconnected {
  background: #f8d7da;
  color: #721c24;
}

.account-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit,
.btn-delete {
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.btn-edit {
  color: #667eea;
}

.btn-edit:hover {
  background: #e3f2fd;
}

.btn-delete {
  color: #dc3545;
}

.btn-delete:hover {
  background: #f8d7da;
}

.btn-add-account {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #28a745;
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.btn-add-account:hover {
  background: #218838;
  transform: translateY(-1px);
}

.ai-settings {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  background: #f8f9fa;
}

.setting-info h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  color: #333;
}

.setting-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.setting-toggle {
  position: relative;
}

.setting-toggle input[type="checkbox"] {
  display: none;
}

.setting-toggle label {
  display: block;
  width: 50px;
  height: 24px;
  background: #ccc;
  border-radius: 12px;
  cursor: pointer;
  position: relative;
  transition: background-color 0.3s ease;
}

.setting-toggle label::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
}

.setting-toggle input[type="checkbox"]:checked + label {
  background: #667eea;
}

.setting-toggle input[type="checkbox"]:checked + label::after {
  transform: translateX(26px);
}

@media (max-width: 768px) {
  .settings-container {
    grid-template-columns: 1fr;
  }
  
  .account-item,
  .setting-item {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .account-actions {
    align-self: flex-end;
  }
}
</style> 