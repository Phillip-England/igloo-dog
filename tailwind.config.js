/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.py"],
  theme: {
    extend: {
      colors: {
        "white": '#ffffff',
        "lightgray": "#eeeeee",
        "gray": "#cccccc",
        "darkgray": "#666666",
        "black": "#333333",
        "cfared": "#e60e33",
      }
    },
  },
  plugins: [],
}