/** Apilix design tokens - same look as the concept site (dark violet, Inter Tight + JetBrains Mono). */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter Tight"', 'system-ui', 'sans-serif'],
        serif: ['"Instrument Serif"', 'Georgia', 'serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      colors: {
        ink: { 950: '#08080e', 900: '#0f0d1a', 800: '#16132a', 700: '#211c3b' },
        lilac: { DEFAULT: '#c8b4ff', 600: '#8f6cf0' },
        mint: '#93f9d2',
        cat: { ai: '#c8b4ff', ui: '#ff7ab6', backend: '#93f9d2', devops: '#ffd36b' },
      },
      boxShadow: { glow: '0 0 40px -14px rgba(200,180,255,.55)' },
    },
  },
  plugins: [],
};
