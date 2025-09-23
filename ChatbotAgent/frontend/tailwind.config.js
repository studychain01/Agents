/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  safelist: [
    'bg-blue-500',
    'bg-gray-200', 
    'text-white',
    'text-gray-900',
    'rounded-2xl',
    'rounded-br-md',
    'rounded-bl-md',
    'px-3',
    'py-2',
    'ml-12',
    'mr-12'
  ]
}
