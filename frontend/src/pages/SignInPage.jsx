import React from "react";
import { SignIn } from "@clerk/react";
import AuthLayout from "../components/AuthLayout";
import { clerkTheme } from "../clerkTheme";

export function SignInPage() {
  return (
    <AuthLayout
      title="Welcome Back"
      subtitle="Sign in to understand your medical reports with AI."
    >
      <SignIn
        path="/sign-in"
        routing="path"
        signUpUrl="/sign-up"
        fallbackRedirectUrl="/"
        appearance={clerkTheme}
      />
    </AuthLayout>
  );
}

export default SignInPage;
