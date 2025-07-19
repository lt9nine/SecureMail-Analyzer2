<template>
  <div class="emails-page">
    <header class="page-header">
      <div class="header-content">
        <h1>📬 E-Mails</h1>
        <div class="header-actions">
          <div class="filters">
            <select v-model="selectedRisk" class="filter-select">
              <option value="">Alle Risikostufen</option>
              <option value="low">Niedrig</option>
              <option value="medium">Mittel</option>
              <option value="high">Hoch</option>
              <option value="critical">Kritisch</option>
            </select>
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="E-Mail durchsuchen..."
              class="search-input"
            />
          </div>
          <button @click="refreshEmails" class="btn-refresh">
            <i class="pi pi-refresh"></i>
            Aktualisieren
          </button>
        </div>
      </div>
    </header>
    
    <main class="emails-main">
      <div class="emails-container">
        <div v-if="loading" class="loading">
          <i class="pi pi-spin pi-spinner"></i>
          E-Mails werden geladen...
        </div>
        
        <div v-else-if="filteredEmails.length === 0" class="no-emails">
          <i class="pi pi-envelope"></i>
          <h3>Keine E-Mails gefunden</h3>
          <p>Es wurden keine E-Mails mit den aktuellen Filtern gefunden.</p>
        </div>
        
        <div v-else class="emails-list">
          <div 
            v-for="email in filteredEmails" 
            :key="email.id" 
            class="email-card"
            @click="viewEmail(email.id)"
          >
            <div class="email-header">
              <div class="email-status" :class="email.riskLevel">
                <i :class="getRiskIcon(email.riskLevel)"></i>
              </div>
              <div class="email-meta">
                <h3>{{ email.subject }}</h3>
                <p class="email-from">{{ email.from }}</p>
                <p class="email-to">{{ email.to }}</p>
              </div>
              <div class="email-date">
                {{ formatDate(email.date) }}
              </div>
            </div>
            
                         <div class="email-preview">
               <p>{{ email.preview }}</p>
               <div class="email-analysis-preview">
                 <div class="analysis-summary">
                   <span class="analysis-score">Score: {{ email.analysisScore }}/100</span>
                   <div class="analysis-indicators">
                     <span v-if="email.analysis?.metadata?.status === 'danger'" class="indicator danger" title="Metadaten verdächtig">
                       <i class="pi pi-shield"></i>
                     </span>
                     <span v-if="email.analysis?.content?.status === 'danger'" class="indicator danger" title="Inhalt verdächtig">
                       <i class="pi pi-file-edit"></i>
                     </span>
                     <span v-if="email.analysis?.attachments?.virusTotal?.malicious > 0" class="indicator danger" title="VirusTotal: Verdächtige Anhänge">
                       <i class="pi pi-paperclip"></i>
                     </span>
                     <span v-if="email.analysis?.ai?.status === 'danger'" class="indicator danger" title="KI-Analyse: Verdächtig">
                       <i class="pi pi-brain"></i>
                     </span>
                     <span v-if="email.analysis?.links?.status === 'danger'" class="indicator danger" title="Link-Analyse: Verdächtig">
                       <i class="pi pi-link"></i>
                     </span>
                   </div>
                 </div>
               </div>
             </div>
            
            <div class="email-footer">
              <div class="email-tags">
                <span v-if="email.hasAttachments" class="tag attachment">
                  <i class="pi pi-paperclip"></i>
                  Anhang
                </span>
                <span v-if="email.isRead" class="tag read">
                  <i class="pi pi-check"></i>
                  Gelesen
                </span>
              </div>
              <div class="email-actions">
                <button @click.stop="deleteEmail(email.id)" class="btn-delete">
                  <i class="pi pi-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Emails',
  data() {
    return {
      emails: [],
      loading: false,
      selectedRisk: '',
      searchQuery: ''
    }
  },
  computed: {
    filteredEmails() {
      let filtered = this.emails
      
      if (this.selectedRisk) {
        filtered = filtered.filter(email => email.riskLevel === this.selectedRisk)
      }
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(email => 
          email.subject.toLowerCase().includes(query) ||
          email.from.toLowerCase().includes(query) ||
          email.preview.toLowerCase().includes(query)
        )
      }
      
      return filtered
    }
  },
  mounted() {
    this.loadEmails()
  },
  methods: {
    async loadEmails() {
      this.loading = true
      try {
        // TODO: Load real data from API
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        this.emails = [
          {
            id: 1,
            subject: 'Wichtige Sicherheitswarnung',
            from: 'security@company.com',
            to: 'user@example.com',
            date: new Date(),
            riskLevel: 'high',
            analysisScore: 85,
            preview: 'Ihr Konto wurde möglicherweise kompromittiert. Bitte überprüfen Sie sofort Ihre Sicherheitseinstellungen...',
            hasAttachments: false,
            isRead: false,
            analysis: {
              metadata: { status: 'danger' },
              content: { status: 'danger' },
              links: { status: 'critical' },
              attachments: { virusTotal: { malicious: 0 } },
              ai: { status: 'danger' }
            }
          },
          {
            id: 2,
            subject: 'Newsletter - März 2024',
            from: 'newsletter@example.com',
            to: 'user@example.com',
            date: new Date(Date.now() - 86400000),
            riskLevel: 'low',
            analysisScore: 15,
            preview: 'Willkommen zu unserem monatlichen Newsletter. Hier sind die neuesten Updates und Nachrichten...',
            hasAttachments: true,
            isRead: true,
            analysis: {
              metadata: { status: 'safe' },
              content: { status: 'safe' },
              links: { status: 'safe' },
              attachments: { virusTotal: { malicious: 0 } },
              ai: { status: 'safe' }
            }
          },
          {
            id: 3,
            subject: 'Ihr Konto wurde kompromittiert',
            from: 'support@fake-bank.com',
            to: 'user@example.com',
            date: new Date(Date.now() - 172800000),
            riskLevel: 'critical',
            analysisScore: 95,
            preview: 'Dringend: Ihr Bankkonto wurde gehackt. Klicken Sie hier, um es sofort zu sichern...',
            hasAttachments: false,
            isRead: false,
            analysis: {
              metadata: { status: 'critical' },
              content: { status: 'critical' },
              links: { status: 'critical' },
              attachments: { virusTotal: { malicious: 0 } },
              ai: { status: 'critical' }
            }
          },
          {
            id: 4,
            subject: 'Meeting-Termin bestätigt',
            from: 'calendar@company.com',
            to: 'user@example.com',
            date: new Date(Date.now() - 259200000),
            riskLevel: 'low',
            analysisScore: 10,
            preview: 'Ihr Meeting für morgen um 14:00 Uhr wurde bestätigt. Bitte seien Sie pünktlich...',
            hasAttachments: false,
            isRead: true,
            analysis: {
              metadata: { status: 'safe' },
              content: { status: 'safe' },
              links: { status: 'safe' },
              attachments: { virusTotal: { malicious: 0 } },
              ai: { status: 'safe' }
            }
          }
        ]
      } catch (error) {
        console.error('Failed to load emails:', error)
      } finally {
        this.loading = false
      }
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
    
    async deleteEmail(emailId) {
      if (confirm('Möchten Sie diese E-Mail wirklich löschen?')) {
        // TODO: Implement delete logic
        console.log('Deleting email:', emailId)
        this.emails = this.emails.filter(email => email.id !== emailId)
      }
    },
    
    async refreshEmails() {
      await this.loadEmails()
    }
  }
}
</script>

<style scoped>
.emails-page {
  min-height: 100vh;
  background: #f8f9fa;
}

.page-header {
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.filters {
  display: flex;
  gap: 1rem;
}

.filter-select,
.search-input {
  padding: 0.5rem;
  border: 1px solid #e1e5e9;
  border-radius: 6px;
  font-size: 0.9rem;
}

.search-input {
  width: 250px;
}

.btn-refresh {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-refresh:hover {
  background: #5a6fd8;
}

.emails-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.loading,
.no-emails {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.loading i {
  font-size: 2rem;
  margin-bottom: 1rem;
  display: block;
}

.no-emails i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
  color: #ccc;
}

.emails-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.email-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}

.email-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.email-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.email-status {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
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

.email-meta {
  flex: 1;
}

.email-meta h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.1rem;
  color: #333;
}

.email-from,
.email-to {
  margin: 0 0 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.email-date {
  color: #999;
  font-size: 0.8rem;
  white-space: nowrap;
}

.email-preview {
  margin-bottom: 1rem;
}

.email-preview p {
  margin: 0 0 0.5rem 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.email-analysis-preview {
  border-top: 1px solid #e1e5e9;
  padding-top: 0.5rem;
}

.analysis-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.analysis-score {
  font-size: 0.8rem;
  color: #666;
  font-weight: 600;
}

.analysis-indicators {
  display: flex;
  gap: 0.25rem;
}

.indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-size: 0.7rem;
  color: white;
}

.indicator.danger {
  background: #dc3545;
}

.indicator.warning {
  background: #ffc107;
  color: #333;
}

.indicator.safe {
  background: #28a745;
}

.email-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.email-tags {
  display: flex;
  gap: 0.5rem;
}

.tag {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.tag.attachment {
  background: #e3f2fd;
  color: #1976d2;
}

.tag.read {
  background: #e8f5e8;
  color: #2e7d32;
}

.btn-delete {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-delete:hover {
  background: #c82333;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .header-actions {
    flex-direction: column;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .search-input {
    width: 100%;
  }
  
  .email-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .email-date {
    align-self: flex-end;
  }
}
</style> 