/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        trivia: {
          geografia: '#3b82f6',     // Blue
          historia: '#f97316',      // Orange
          ciencia: '#22c55e',       // Green
          entretenimiento: '#ec4899', // Pink
          arte: '#d946ef',          // Magenta
          deportes: '#eab308',      // Yellow
        }
      }
    },
  },
  plugins: [],
};
