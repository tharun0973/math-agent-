/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          dark: '#1A1A1A',
          darker: '#121212',
          orange: '#FF6B35',
          'orange-hover': '#E55A2B',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography') // ✅ Enables markdown styling
  ],
}
