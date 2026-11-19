import React from "react";
import { useAuth } from "@clerk/react";
import { Navigate } from "react-router-dom";

export function PublicOnlyRoute({ children }) {
  const { isLoaded, isSignedIn } = useAuth();

  if (!isLoaded) {
    return (
      <div className="auth-loading-screen">
        <div className="spinner auth-spinner" />
        <p>Checking authentication...</p>
      </div>
    );
  }

  if (isSignedIn) {
    return <Navigate to="/" replace />;
  }

  return children;
}

export default PublicOnlyRoute;
