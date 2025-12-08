/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}", "./content/**/*.md"],
  theme: {
    fontFamily: {
      sans: ['Lato', 'sans-serif'],
      serif: ['Playfair Display', 'serif'],
    },
    extend: {
      colors: {
        primary: '#064e3b', // emerald-900: Deep Herbal Green
        secondary: '#f5f5f4', // stone-100: Warm Background
        accent: '#d97706', // amber-600: Gold/Energy
        'accent-light': '#fcd34d', // amber-300
        text: '#1e293b', // slate-800: Soft Black
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ]
}

