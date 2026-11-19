/**
 * Clerk theme customization matching the Bright Sky Blue healthcare palette
 */
export const clerkTheme = {
  variables: {
    colorPrimary: "#0EA5E9",
    colorText: "#16324F",
    colorTextSecondary: "#33597D",
    colorBackground: "#FFFFFF",
    colorInputBackground: "#FFFFFF",
    colorInputBorder: "#BAE6FD",
    colorDanger: "#DC2626",
    colorSuccess: "#16A34A",
    colorWarning: "#D97706",
    borderRadius: "12px",
    fontFamily: "'Inter', 'Noto Sans', -apple-system, BlinkMacSystemFont, sans-serif",
  },
  elements: {
    rootBox: {
      width: "100%",
      maxWidth: "440px",
    },
    card: {
      border: "1.5px solid #BAE6FD",
      borderRadius: "18px",
      boxShadow: "0 16px 40px -6px rgba(22, 50, 79, 0.12), 0 4px 14px -2px rgba(14, 165, 233, 0.08)",
      background: "#FFFFFF",
    },
    headerTitle: {
      color: "#16324F",
      fontWeight: "800",
      letterSpacing: "-0.02em",
    },
    headerSubtitle: {
      color: "#33597D",
      fontSize: "14px",
    },
    socialButtonsBlockButton: {
      border: "1.5px solid #BAE6FD",
      borderRadius: "10px",
      fontWeight: "650",
      color: "#16324F",
      "&:hover": {
        borderColor: "#38BDF8",
        backgroundColor: "#F0F9FF",
      },
    },
    formFieldLabel: {
      color: "#16324F",
      fontWeight: "700",
      fontSize: "13px",
    },
    formFieldInput: {
      borderRadius: "10px",
      border: "1.5px solid #BAE6FD",
      color: "#16324F",
      backgroundColor: "#FFFFFF",
      "&:focus": {
        borderColor: "#38BDF8",
        boxShadow: "0 0 0 3px rgba(56, 189, 248, 0.25)",
      },
    },
    formButtonPrimary: {
      background: "linear-gradient(135deg, #38BDF8 0%, #0EA5E9 100%)",
      color: "#FFFFFF",
      fontWeight: "750",
      fontSize: "14.5px",
      borderRadius: "10px",
      boxShadow: "0 4px 14px rgba(14, 165, 233, 0.35)",
      transition: "all 0.2s ease",
      "&:hover": {
        background: "linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%)",
        boxShadow: "0 6px 18px rgba(14, 165, 233, 0.45)",
      },
    },
    footerActionLink: {
      color: "#0284C7",
      fontWeight: "700",
      "&:hover": {
        color: "#0EA5E9",
      },
    },
    userButtonAvatarBox: {
      width: "36px",
      height: "36px",
      border: "1.5px solid #38BDF8",
      boxShadow: "0 2px 8px rgba(14, 165, 233, 0.2)",
    },
  },
};
