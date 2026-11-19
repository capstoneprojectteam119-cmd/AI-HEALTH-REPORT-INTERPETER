import React from "react";
import { SignUp } from "@clerk/react";
import AuthLayout from "../components/AuthLayout";
import { clerkTheme } from "../clerkTheme";

export function SignUpPage() {
  return (
    <AuthLayout
      title="Create Account"
      subtitle="Join to securely analyze your clinical lab and imaging reports with AI."
    >
      <SignUp
        path="/sign-up"
        routing="path"
        signInUrl="/sign-in"
        fallbackRedirectUrl="/"
        appearance={clerkTheme}
      />
    </AuthLayout>
  );
}

export default SignUpPage;
