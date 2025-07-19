<template>
  <div class="email-detail-page">
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <button @click="$router.go(-1)" class="btn-back">
            <i class="pi pi-arrow-left"></i>
            Zurück
          </button>
          <h1>📧 E-Mail Details</h1>
        </div>
        <div class="header-actions">
          <button @click="deleteEmail" class="btn-delete">
            <i class="pi pi-trash"></i>
            Löschen
          </button>
        </div>
      </div>
    </header>
    
    <main class="email-detail-main">
      <div v-if="loading" class="loading">
        <i class="pi pi-spin pi-spinner"></i>
        E-Mail wird geladen...
      </div>
      
      <div v-else-if="!email" class="not-found">
        <i class="pi pi-exclamation-triangle"></i>
        <h3>E-Mail nicht gefunden</h3>
        <p>Die angeforderte E-Mail konnte nicht gefunden werden.</p>
      </div>
      
      <div v-else class="email-detail-container">
        <div class="email-header">
          <div class="email-status" :class="email.riskLevel">
            <i :class="getRiskIcon(email.riskLevel)"></i>
          </div>
          <div class="email-info">
            <h2>{{ email.subject }}</h2>
            <div class="email-meta">
              <div class="meta-item">
                <strong>Von:</strong> {{ email.from }}
              </div>
              <div class="meta-item">
                <strong>An:</strong> {{ email.to }}
              </div>
              <div class="meta-item">
                <strong>Datum:</strong> {{ formatDate(email.date) }}
              </div>
            </div>
          </div>
        </div>
        
        <div class="email-content">
          <div class="content-section">
            <h3>📄 Inhalt</h3>
            <div class="email-body" v-html="email.content"></div>
          </div>
          
          <div v-if="email.attachments && email.attachments.length > 0" class="content-section">
            <h3>📎 Anhänge</h3>
            <div class="attachments-list">
              <div v-for="attachment in email.attachments" :key="attachment.id" class="attachment-item">
                <div class="attachment-icon">
                  <i class="pi pi-paperclip"></i>
                </div>
                <div class="attachment-info">
                  <h4>{{ attachment.filename }}</h4>
                  <p>{{ attachment.size }} • {{ attachment.mimeType }}</p>
                </div>
                <div class="attachment-actions">
                  <button @click="downloadAttachment(attachment)" class="btn-download">
                    <i class="pi pi-download"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="content-section">
            <h3>🔍 Sicherheitsanalyse</h3>
            <div class="analysis-results">
              <div class="risk-summary">
                <div class="risk-level" :class="email.riskLevel">
                  <i :class="getRiskIcon(email.riskLevel)"></i>
                  <span>{{ getRiskText(email.riskLevel) }}</span>
                </div>
                <div class="risk-score">
                  Gesamt-Risiko-Score: {{ email.riskScore || 'N/A' }}/100
                </div>
              </div>
              
              <div class="analysis-pipeline">
                <h4>Analyse-Pipeline Ergebnisse:</h4>
                
                <div class="pipeline-step">
                  <div class="step-header">
                    <i class="pi pi-shield"></i>
                    <h5>Metadaten-Check</h5>
                    <span class="step-status" :class="email.analysis.metadata.status">
                      {{ getStatusText(email.analysis.metadata.status) }}
                    </span>
                  </div>
                  <div class="step-details">
                    <p><strong>Score:</strong> {{ email.analysis.metadata.score }}/100</p>
                    <ul>
                      <li v-for="(detail, index) in email.analysis.metadata.details" :key="index">
                        {{ detail }}
                      </li>
                    </ul>
                  </div>
                </div>
                
                <div class="pipeline-step">
                  <div class="step-header">
                    <i class="pi pi-file"></i>
                    <h5>Header-Analyse</h5>
                    <span class="step-status" :class="email.analysis.headers.status">
                      {{ getStatusText(email.analysis.headers.status) }}
                    </span>
                  </div>
                  <div class="step-details">
                    <p><strong>Score:</strong> {{ email.analysis.headers.score }}/100</p>
                    <ul>
                      <li v-for="(detail, index) in email.analysis.headers.details" :key="index">
                        {{ detail }}
                      </li>
                    </ul>
                  </div>
                </div>
                
                <div class="pipeline-step">
                  <div class="step-header">
                    <i class="pi pi-file-edit"></i>
                    <h5>Inhaltsanalyse</h5>
                    <span class="step-status" :class="email.analysis.content.status">
                      {{ getStatusText(email.analysis.content.status) }}
                    </span>
                  </div>
                  <div class="step-details">
                    <p><strong>Score:</strong> {{ email.analysis.content.score }}/100</p>
                    <ul>
                      <li v-for="(detail, index) in email.analysis.content.details" :key="index">
                        {{ detail }}
                      </li>
                    </ul>
                  </div>
                </div>
                
                <div class="pipeline-step">
                  <div class="step-header">
                    <i class="pi pi-link"></i>
                    <h5>Link-Analyse</h5>
                    <span class="step-status" :class="email.analysis.links.status">
                      {{ getStatusText(email.analysis.links.status) }}
                    </span>
                  </div>
                  <div class="step-details">
                    <p><strong>Score:</strong> {{ email.analysis.links.score }}/100</p>
                    <ul>
                      <li v-for="(detail, index) in email.analysis.links.details" :key="index">
                        {{ detail }}
                      </li>
                    </ul>
                    
                    <div v-if="email.analysis.links.links && email.analysis.links.links.length > 0" class="link-details">
                      <h6>Gefundene Links:</h6>
                      <div v-for="(link, index) in email.analysis.links.links" :key="index" class="link-item">
                        <div class="link-header">
                          <span class="link-status" :class="link.status">
                            {{ getStatusText(link.status) }}
                          </span>
                          <span class="link-score">Score: {{ link.score }}/100</span>
                        </div>
                        <div class="link-url">
                          <strong>URL:</strong> 
                          <a :href="link.url" target="_blank" rel="noopener noreferrer" class="link-text">
                            {{ link.url }}
                          </a>
                        </div>
                        <div v-if="link.display_text !== link.url" class="link-text">
                          <strong>Angezeigter Text:</strong> {{ link.display_text }}
                        </div>
                        <div v-if="link.threats && link.threats.length > 0" class="link-threats">
                          <strong>Bedrohungen:</strong>
                          <ul>
                            <li v-for="(threat, threatIndex) in link.threats" :key="threatIndex">
                              {{ getThreatText(threat) }}
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="pipeline-step">
                  <div class="step-header">
                    <i class="pi pi-paperclip"></i>
                    <h5>Anhangsanalyse</h5>
                    <span class="step-status" :class="email.analysis.attachments.status">
                      {{ getStatusText(email.analysis.attachments.status) }}
                    </span>
                  </div>
                  <div class="step-details">
                    <p><strong>Score:</strong> {{ email.analysis.attachments.score }}/100</p>
                    <div v-if="email.analysis.attachments.virusTotal" class="virustotal-results">
                      <h6>VirusTotal Ergebnisse:</h6>
                      <div class="vt-stats">
                        <span class="vt-stat">
                          <i class="pi pi-check-circle"></i>
                          {{ email.analysis.attachments.virusTotal.clean }} sauber
                        </span>
                        <span class="vt-stat">
                          <i class="pi pi-times-circle"></i>
                          {{ email.analysis.attachments.virusTotal.malicious }} verdächtig
                        </span>
                        <span class="vt-stat">
                          <i class="pi pi-question-circle"></i>
                          {{ email.analysis.attachments.virusTotal.undetected }} unerkannt
                        </span>
                      </div>
                    </div>
                    <ul>
                      <li v-for="(detail, index) in email.analysis.attachments.details" :key="index">
                        {{ detail }}
                      </li>
                    </ul>
                  </div>
                </div>
                
                <div class="pipeline-step">
                  <div class="step-header">
                    <i class="pi pi-brain"></i>
                    <h5>KI-Analyse</h5>
                    <span class="step-status" :class="email.analysis.ai.status">
                      {{ getStatusText(email.analysis.ai.status) }}
                    </span>
                  </div>
                  <div class="step-details">
                    <p><strong>Score:</strong> {{ email.analysis.ai.score }}/100</p>
                    <p><strong>Confidence:</strong> {{ email.analysis.ai.confidence }}%</p>
                    <p><strong>Begründung:</strong> {{ email.analysis.ai.reasoning }}</p>
                  </div>
                </div>
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
  name: 'EmailDetail',
  data() {
    return {
      email: null,
      loading: true
    }
  },
  mounted() {
    this.loadEmail()
  },
  methods: {
    async loadEmail() {
      this.loading = true
      try {
        const emailId = this.$route.params.id
        
        // TODO: Load real data from API
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Mock data
        this.email = {
          id: emailId,
          subject: 'Wichtige Sicherheitswarnung',
          from: 'security@company.com',
          to: 'user@example.com',
          date: new Date(),
          riskLevel: 'high',
          riskScore: 85,
          content: `
            <p>Sehr geehrte Damen und Herren,</p>
            <p>wir haben verdächtige Aktivitäten in Ihrem Konto festgestellt. Bitte überprüfen Sie sofort Ihre Sicherheitseinstellungen und ändern Sie Ihr Passwort.</p>
            <p>Klicken Sie auf den folgenden Link, um Ihr Konto zu sichern:</p>
            <p><a href="https://secure-login.example.com">Sicheres Login</a></p>
            <p>Oder nutzen Sie unseren URL-Shortener: <a href="https://bit.ly/secure-login">https://bit.ly/secure-login</a></p>
            <p>Für weitere Informationen: <a href="http://192.168.1.100/login">http://192.168.1.100/login</a></p>
            <p>Mit freundlichen Grüßen,<br>Ihr Sicherheitsteam</p>
          `,
          attachments: [
            {
              id: 1,
              filename: 'security_report.pdf',
              size: '2.5 MB',
              mimeType: 'application/pdf'
            }
          ],
          analysis: {
            metadata: {
              status: 'danger',
              score: 75,
              details: [
                'Absender-Domain "company.com" nicht authentifiziert',
                'DKIM-Signatur fehlt',
                'SPF-Check fehlgeschlagen',
                'Reply-To weicht vom From ab'
              ]
            },
            headers: {
              status: 'warning',
              score: 60,
              details: [
                'Received-Header-Kette zeigt verdächtige Umleitung',
                'X-Mailer-Header fehlt',
                'Message-ID Format ungewöhnlich'
              ]
            },
            content: {
              status: 'danger',
              score: 80,
              details: [
                'Dringender Ton im Betreff erkannt',
                'Aufforderung zu sofortiger Aktion',
                'Verdächtige Keywords gefunden: "Konto", "sofort", "sichern"'
              ]
            },
            links: {
              status: 'critical',
              score: 90,
              details: [
                '3 kritisch verdächtige Links gefunden',
                '1x Lookalike-Domains',
                '3x Phishing-Keywords',
                '1x Text-URL-Mismatches',
                '1x URL-Shortener',
                '1x IP-Adressen',
                '1x Nicht-HTTPS Links'
              ],
              links: [
                {
                  url: 'https://secure-login.example.com',
                  display_text: 'Sicheres Login',
                  status: 'critical',
                  score: 90,
                  details: [
                    'Lookalike-Domain erkannt: example → example.com',
                    'Phishing-Keywords gefunden: secure, login',
                    'Link-Text stimmt nicht mit Ziel-URL überein'
                  ],
                  threats: ['lookalike_domain', 'phishing_keywords', 'text_mismatch'],
                  domain: 'secure-login.example.com',
                  parsed_url: {
                    scheme: 'https',
                    netloc: 'secure-login.example.com',
                    path: '',
                    query: ''
                  }
                },
                {
                  url: 'https://bit.ly/secure-login',
                  display_text: 'https://bit.ly/secure-login',
                  status: 'danger',
                  score: 75,
                  details: [
                    'URL-Shortener erkannt (kann versteckte Ziele haben)',
                    'Phishing-Keywords gefunden: secure, login'
                  ],
                  threats: ['url_shortener', 'phishing_keywords'],
                  domain: 'bit.ly',
                  parsed_url: {
                    scheme: 'https',
                    netloc: 'bit.ly',
                    path: '/secure-login',
                    query: ''
                  }
                },
                {
                  url: 'http://192.168.1.100/login',
                  display_text: 'http://192.168.1.100/login',
                  status: 'critical',
                  score: 95,
                  details: [
                    'IP-Adresse statt Domain verwendet',
                    'Nicht-HTTPS Verbindung (unsicher)',
                    'Phishing-Keywords gefunden: login'
                  ],
                  threats: ['ip_address', 'non_https', 'phishing_keywords'],
                  domain: '192.168.1.100',
                  parsed_url: {
                    scheme: 'http',
                    netloc: '192.168.1.100',
                    path: '/login',
                    query: ''
                  }
                }
              ]
            },
            attachments: {
              status: 'safe',
              score: 20,
              details: [
                'PDF-Datei als sicher eingestuft',
                'Keine ausführbaren Dateien gefunden',
                'Dateigröße im normalen Bereich'
              ],
              virusTotal: {
                clean: 45,
                malicious: 2,
                undetected: 3
              }
            },
            ai: {
              status: 'danger',
              score: 85,
              confidence: 92,
              reasoning: 'Die E-Mail zeigt typische Phishing-Muster: Dringender Ton, Aufforderung zu sofortiger Aktion, verdächtige Links und fehlende Authentifizierung. Die Kombination dieser Faktoren deutet stark auf einen Phishing-Versuch hin.'
            }
          }
        }
      } catch (error) {
        console.error('Failed to load email:', error)
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
    
    getRiskText(riskLevel) {
      const texts = {
        low: 'Niedriges Risiko',
        medium: 'Mittleres Risiko',
        high: 'Hohes Risiko',
        critical: 'Kritisches Risiko'
      }
      return texts[riskLevel] || 'Unbekanntes Risiko'
    },
    
    getStatusText(status) {
      const texts = {
        safe: 'Sicher',
        warning: 'Warnung',
        danger: 'Gefährlich',
        critical: 'Kritisch'
      }
      return texts[status] || 'Unbekannt'
    },
    
    getThreatText(threat) {
      const texts = {
        lookalike_domain: 'Lookalike-Domain erkannt',
        phishing_keywords: 'Phishing-Keywords in URL',
        url_shortener: 'URL-Shortener (kann versteckte Ziele haben)',
        ip_address: 'IP-Adresse statt Domain',
        text_mismatch: 'Link-Text stimmt nicht mit URL überein',
        non_https: 'Nicht-HTTPS Verbindung',
        suspicious_tld: 'Verdächtige Top-Level-Domain',
        suspicious_subdomain: 'Verdächtige Subdomain',
        invalid_url: 'Ungültige URL-Format',
        parse_error: 'URL konnte nicht geparst werden'
      }
      return texts[threat] || threat
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
    
    downloadAttachment(attachment) {
      // TODO: Implement download logic
      console.log('Downloading attachment:', attachment.filename)
    },
    
    async deleteEmail() {
      if (confirm('Möchten Sie diese E-Mail wirklich löschen?')) {
        // TODO: Implement delete logic
        console.log('Deleting email:', this.email.id)
        this.$router.push('/emails')
      }
    }
  }
}
</script>

<style scoped>
.email-detail-page {
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

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-back:hover {
  background: #5a6268;
}

.header-content h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.btn-delete {
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

.btn-delete:hover {
  background: #c82333;
}

.email-detail-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.loading,
.not-found {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.loading i {
  font-size: 2rem;
  margin-bottom: 1rem;
  display: block;
}

.not-found i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
  color: #ffc107;
}

.email-detail-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.email-header {
  background: #f8f9fa;
  padding: 2rem;
  border-bottom: 1px solid #e1e5e9;
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.email-status {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
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

.email-info {
  flex: 1;
}

.email-info h2 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
  color: #333;
}

.email-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.meta-item {
  color: #666;
  font-size: 0.9rem;
}

.email-content {
  padding: 2rem;
}

.content-section {
  margin-bottom: 2rem;
}

.content-section:last-child {
  margin-bottom: 0;
}

.content-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  color: #333;
  border-bottom: 2px solid #e1e5e9;
  padding-bottom: 0.5rem;
}

.email-body {
  line-height: 1.6;
  color: #333;
}

.email-body p {
  margin-bottom: 1rem;
}

.email-body a {
  color: #667eea;
  text-decoration: none;
}

.email-body a:hover {
  text-decoration: underline;
}

.attachments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.attachment-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  background: #f8f9fa;
}

.attachment-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #667eea;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.attachment-info {
  flex: 1;
}

.attachment-info h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  color: #333;
}

.attachment-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.btn-download {
  background: #28a745;
  color: white;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-download:hover {
  background: #218838;
}

.analysis-results {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.risk-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e1e5e9;
}

.risk-level {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1.1rem;
}

.risk-level.low {
  color: #155724;
}

.risk-level.medium {
  color: #856404;
}

.risk-level.high {
  color: #721c24;
}

.risk-level.critical {
  color: #721c24;
}

.risk-score {
  color: #666;
  font-size: 0.9rem;
}

.analysis-pipeline h4 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  color: #333;
  border-bottom: 1px solid #e1e5e9;
  padding-bottom: 0.5rem;
}

.pipeline-step {
  margin-bottom: 1.5rem;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  overflow: hidden;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e1e5e9;
}

.step-header i {
  font-size: 1.2rem;
  color: #667eea;
}

.step-header h5 {
  margin: 0;
  font-size: 1rem;
  color: #333;
  flex: 1;
}

.step-status {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.step-status.safe {
  background: #d4edda;
  color: #155724;
}

.step-status.warning {
  background: #fff3cd;
  color: #856404;
}

.step-status.danger {
  background: #f8d7da;
  color: #721c24;
}

.step-status.critical {
  background: #f5c6cb;
  color: #721c24;
}

.step-details {
  padding: 1rem;
}

.step-details p {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.step-details ul {
  margin: 0;
  padding-left: 1.5rem;
  color: #666;
}

.step-details li {
  margin-bottom: 0.25rem;
}

.virustotal-results {
  margin: 1rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.virustotal-results h6 {
  margin: 0 0 0.75rem 0;
  font-size: 0.9rem;
  color: #333;
}

.vt-stats {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.vt-stat {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  color: #666;
}

.vt-stat i {
  font-size: 0.9rem;
}

.vt-stat:first-child i {
  color: #28a745;
}

.vt-stat:nth-child(2) i {
  color: #dc3545;
}

.vt-stat:nth-child(3) i {
  color: #ffc107;
}

.link-details {
  margin: 1rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.link-details h6 {
  margin: 0 0 0.75rem 0;
  font-size: 0.9rem;
  color: #333;
}

.link-item {
  margin-bottom: 1rem;
  padding: 0.75rem;
  border: 1px solid #e1e5e9;
  border-radius: 4px;
  background: white;
}

.link-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.link-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.link-status.safe {
  background: #d4edda;
  color: #155724;
}

.link-status.warning {
  background: #fff3cd;
  color: #856404;
}

.link-status.danger {
  background: #f8d7da;
  color: #721c24;
}

.link-status.critical {
  background: #f5c6cb;
  color: #721c24;
}

.link-score {
  font-size: 0.8rem;
  color: #666;
  font-weight: 600;
}

.link-url, .link-text {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.link-url a {
  color: #007bff;
  text-decoration: none;
  word-break: break-all;
}

.link-url a:hover {
  text-decoration: underline;
}

.link-threats {
  margin-top: 0.5rem;
}

.link-threats ul {
  margin: 0.25rem 0 0 0;
  padding-left: 1.5rem;
  font-size: 0.85rem;
  color: #dc3545;
}

.link-threats li {
  margin-bottom: 0.125rem;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .header-left {
    justify-content: space-between;
  }
  
  .email-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .risk-summary {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style> 