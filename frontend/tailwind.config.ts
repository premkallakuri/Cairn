import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./features/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#fef2f0",
          100: "#fce0da",
          200: "#f9c0b5",
          300: "#f3978a",
          400: "#d4715a",
          500: "#c2543d",
          600: "#a3412c",
          700: "#8b3424",
          800: "#6e291c",
          900: "#5a2218",
          950: "#3d150f",
        },
        accent: {
          50: "#f0fdfa",
          100: "#ccfbf1",
          200: "#99f6e4",
          300: "#5eead4",
          400: "#2dd4bf",
          500: "#14b8a6",
          600: "#0d9488",
          700: "#0f766e",
        },
        surface: {
          0: "var(--surface-0)",
          1: "var(--surface-1)",
          2: "var(--surface-2)",
          3: "var(--surface-3)",
        },
        border: {
          DEFAULT: "var(--border)",
          subtle: "var(--border-subtle)",
        },
        content: {
          DEFAULT: "var(--content)",
          secondary: "var(--content-secondary)",
          tertiary: "var(--content-tertiary)",
          inverse: "var(--content-inverse)",
        },
      },
      borderRadius: {
        "2xl": "1rem",
        "3xl": "1.25rem",
        "4xl": "1.5rem",
      },
      boxShadow: {
        card: "var(--shadow-card)",
        "card-hover": "var(--shadow-card-hover)",
        glow: "var(--shadow-glow)",
      },
      keyframes: {
        "fade-in": {
          from: { opacity: "0", transform: "translateY(8px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "slide-in": {
          from: { opacity: "0", transform: "translateX(-12px)" },
          to: { opacity: "1", transform: "translateX(0)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        pulse_ring: {
          "0%": { boxShadow: "0 0 0 0 rgba(194, 84, 61, 0.4)" },
          "70%": { boxShadow: "0 0 0 10px rgba(194, 84, 61, 0)" },
          "100%": { boxShadow: "0 0 0 0 rgba(194, 84, 61, 0)" },
        },
      },
      animation: {
        "fade-in": "fade-in 0.4s ease-out both",
        "slide-in": "slide-in 0.3s ease-out both",
        shimmer: "shimmer 2s infinite linear",
        pulse_ring: "pulse_ring 2s infinite",
      },
    },
  },
  plugins: [],
};

export default config;
