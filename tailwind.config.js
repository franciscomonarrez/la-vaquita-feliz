/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      './app/**/*.{js,ts,jsx,tsx}',
      './components/**/*.{js,ts,jsx,tsx}',
    ],
    theme: {
      extend: {
        fontFamily: {
          header: ['Montserrat', 'sans-serif'],
          body: ['Source Sans Pro', 'sans-serif'],
        },
        colors: {
          primary:   '#E77622', // Warm orange
          secondary: '#5C2F1A', // Deep brown
          accent:    '#D99F3A', // Mustard yellow
          background:'#FEF5EC', // Light cream
          muted:     '#F1E8DF', // Soft panel tone
        },
      },
    },
    plugins: [],
  }