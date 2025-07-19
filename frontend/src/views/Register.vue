<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h1>📝 Registrieren</h1>
        <p>Erstellen Sie Ihr Konto für SecureMail Analyzer</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="name">Vollständiger Name</label>
          <input 
            type="text" 
            id="name" 
            v-model="name" 
            required 
            placeholder="Max Mustermann"
          />
        </div>
        
        <div class="form-group">
          <label for="email">E-Mail</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            placeholder="max.mustermann@beispiel.com"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Passwort</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            placeholder="Mindestens 8 Zeichen"
            minlength="8"
          />
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">Passwort bestätigen</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            required 
            placeholder="Passwort wiederholen"
          />
        </div>
        
        <button type="submit" class="btn-register" :disabled="loading || !passwordsMatch">
          <span v-if="loading">Registrierung läuft...</span>
          <span v-else>Registrieren</span>
        </button>
      </form>
      
      <div class="register-footer">
        <p>Bereits ein Konto? <router-link to="/login">Anmelden</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      loading: false
    }
  },
  computed: {
    passwordsMatch() {
      return this.password && this.confirmPassword && this.password === this.confirmPassword
    }
  },
  methods: {
    async handleRegister() {
      if (!this.passwordsMatch) {
        alert('Passwörter stimmen nicht überein')
        return
      }
      
      this.loading = true
      try {
        // TODO: Implement registration logic
        console.log('Register attempt:', { 
          name: this.name, 
          email: this.email, 
          password: this.password 
        })
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        this.$router.push('/login')
      } catch (error) {
        console.error('Registration failed:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.register-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 3rem;
  width: 100%;
  max-width: 450px;
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
}

.register-header p {
  color: #666;
  font-size: 1rem;
}

.register-form {
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

.btn-register {
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

.btn-register:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn-register:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e1e5e9;
}

.register-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.register-footer a:hover {
  text-decoration: underline;
}
</style> 