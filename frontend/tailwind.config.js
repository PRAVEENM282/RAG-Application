/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'accent-primary': '#3b82f6',
                'bg-secondary': '#1e293b',
            }
        },
    },
    plugins: [],
}
