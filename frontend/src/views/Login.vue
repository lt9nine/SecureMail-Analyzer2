<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>🔐 Anmelden</h1>
        <p>Willkommen zurück bei SecureMail Analyzer</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">E-Mail</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            placeholder="ihre.email@beispiel.com"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Passwort</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            placeholder="Ihr Passwort"
          />
        </div>
        
        <button type="submit" class="btn-login" :disabled="loading">
          <span v-if="loading">Anmeldung läuft...</span>
          <span v-else>Anmelden</span>
        </button>
      </form>
      
      <div class="login-footer">
        <p>Noch kein Konto? <router-link to="/register">Registrieren</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      try {
        // TODO: Implement login logic
        console.log('Login attempt:', { email: this.email, password: this.password })
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        this.$router.push('/dashboard')
      } catch (error) {
        console.error('Login failed:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.login-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 3rem;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: #666;
  font-size: 1rem;
}

.login-form {
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

.form-group input {
  padding: 1rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.btn-login {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e1e5e9;
}

.login-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-footer a:hover {
  text-decoration: underline;
}
</style> 