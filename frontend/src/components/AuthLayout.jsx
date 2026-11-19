import React from "react";
import "./AuthLayout.css";

export function AuthLayout({ title, subtitle, children }) {
  return (
    <div className="auth-shell">
      {/* Background medical dot pattern and ambient radial glow */}
      <div className="auth-ambient-glow" aria-hidden="true" />

      <div className="auth-container">
        {/* Left Branding & Highlights Section */}
        <div className="auth-left-col">
          <div className="auth-brand-badge">
            <span className="auth-brand-dot" />
            <span>AI Healthcare Intelligence</span>
          </div>

          <div className="auth-brand-header">
            <div className="auth-brand-logo" aria-hidden="true">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 3V21M3 12H21" stroke="#0EA5E9" strokeWidth="2.5" strokeLinecap="round" />
                <path d="M7 7L17 17M17 7L7 17" stroke="#16324F" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
                <circle cx="12" cy="12" r="3.5" fill="#E0F2FE" stroke="#0284C7" strokeWidth="1.5" />
              </svg>
            </div>
            <h1 className="auth-brand-name">AI Health Report Interpreter</h1>
          </div>

          <div className="auth-hero-copy">
            <h2 className="auth-title">{title}</h2>
            <p className="auth-subtitle">{subtitle}</p>
          </div>

          {/* Healthcare & AI Illustration Mini Card */}
          <div className="auth-illustration-card" aria-hidden="true">
            <div className="auth-card-top-bar">
              <span className="auth-doc-chip">CLINICAL ENGINE</span>
              <span className="auth-pulse-status">● Live Diagnostics</span>
            </div>
            <div className="auth-ecg-trace">
              <svg viewBox="0 0 240 32" fill="none" className="auth-ecg-svg">
                <path
                  d="M0 16 H40 L48 8 L56 26 L64 4 L72 20 L80 16 H140 L148 10 L156 24 L164 6 L172 20 L180 16 H240"
                  stroke="#38BDF8"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <div className="auth-metric-pills">
              <span className="auth-pill normal">✓ Hemoglobin: 14.2 g/dL</span>
              <span className="auth-pill high">↑ Glucose: 105 mg/dL</span>
            </div>
          </div>

          {/* Key Clinical Features */}
          <div className="auth-features-list">
            <div className="auth-feature-item">
              <span className="auth-feature-icon">🧪</span>
              <div className="auth-feature-desc">
                <strong>Biomarker Extraction</strong>
                <span>Instant laboratory range comparison and status tracking</span>
              </div>
            </div>
            <div className="auth-feature-item">
              <span className="auth-feature-icon">🩺</span>
              <div className="auth-feature-desc">
                <strong>Pattern Detection</strong>
                <span>Recognizes clinical signals and diagnostic correlations</span>
              </div>
            </div>
            <div className="auth-feature-item">
              <span className="auth-feature-icon">🌐</span>
              <div className="auth-feature-desc">
                <strong>8 Indian Languages</strong>
                <span>Accessible healthcare insights in native scripts</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Authentication Card Section */}
        <div className="auth-right-col">
          <div className="auth-card-container">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AuthLayout;
