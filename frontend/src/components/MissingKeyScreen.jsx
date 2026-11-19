import React from "react";
import AuthLayout from "./AuthLayout";

export function MissingKeyScreen() {
  return (
    <AuthLayout
      title="Clerk Setup Required"
      subtitle="Configure your Clerk Publishable Key to activate authentication."
    >
      <div className="auth-missing-key-card">
        <h3>🔑 Publishable Key Missing</h3>
        <p>
          Clerk authentication requires a publishable key. To activate login and signup:
        </p>

        <ol className="auth-config-steps">
          <li>
            Open your <strong>Clerk Dashboard</strong> at{" "}
            <a
              href="https://dashboard.clerk.com"
              target="_blank"
              rel="noreferrer"
              style={{ color: "#0284C7", fontWeight: 700 }}
            >
              dashboard.clerk.com
            </a>.
          </li>
          <li>Navigate to <strong>API Keys</strong> in the sidebar.</li>
          <li>Copy your <strong>Publishable key</strong> (starts with <code>pk_test_</code>).</li>
          <li>
            Add it to your <code>frontend/.env</code> file:
          </li>
        </ol>

        <code>VITE_CLERK_PUBLISHABLE_KEY=pk_test_your_key_here</code>

        <p style={{ fontSize: "12.5px", color: "#64748B" }}>
          After creating or updating <code>frontend/.env</code>, restart your Vite dev server to view the live login page at <code>/sign-in</code>.
        </p>
      </div>
    </AuthLayout>
  );
}

export default MissingKeyScreen;
