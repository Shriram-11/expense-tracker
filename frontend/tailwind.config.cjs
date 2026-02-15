/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef9f6",
          100: "#d4efe8",
          200: "#abdccc",
          300: "#78c1a8",
          400: "#49a283",
          500: "#2e8668",
          600: "#216b54",
          700: "#1d5544",
          800: "#1a4337",
          900: "#17382f"
        }
      }
    }
  },
  plugins: []
};
