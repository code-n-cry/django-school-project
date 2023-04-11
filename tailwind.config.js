/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./node_modules/tw-elements/dist/js/**/*.js",
  ],
  theme: {
    extend: {},
    container: {
      padding: {
        DEFAULT: '1rem',
        sm: '2rem',
        lg: '4rem',
        xl: '8rem',
        '2xl': '6rem',
      },
    },
  },
  darkMode: "class",
  plugins: [require("tw-elements/dist/plugin")],
};
