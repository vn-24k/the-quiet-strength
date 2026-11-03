/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        washi: {
          50: "#FAF8F5",
          100: "#F5F2EB",
          200: "#EFECE4",
          300: "#E5E0D5",
          400: "#D6CFC0",
          500: "#C4BAA6"
        },
        ink: {
          900: "#0A0A0A",
          800: "#141414",
          700: "#222120",
          600: "#383634",
          500: "#5A5752",
          400: "#7F7B74",
          300: "#A8A39B"
        },
        crimson: {
          500: "#C41E1E",
          600: "#A01414",
          700: "#8B0E0E",
          800: "#6B0A0A",
          900: "#4D0606"
        },
        vermilion: "#E6392F",
        goldLeaf: "#C5A059"
      },
      fontFamily: {
        serif: ['"Cinzel"', '"Playfair Display"', '"Didot"', 'Georgia', 'serif'],
        sans: ['"Plus Jakarta Sans"', '"Inter"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"Space Mono"', 'monospace'],
        kanji: ['"Noto Serif JP"', '"Yu Mincho"', 'serif']
      },
      backgroundImage: {
        'paper-grain': "radial-gradient(#b0a898 0.75px, transparent 0.75px)",
      },
      animation: {
        'pulse-subtle': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float-slow': 'float 7s ease-in-out infinite',
        'ink-fade': 'inkFade 1.2s ease-out forwards',
        'shimmer': 'shimmer 2.8s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-6px)' },
        },
        inkFade: {
          '0%': { opacity: '0', filter: 'blur(4px)' },
          '100%': { opacity: '1', filter: 'blur(0)' }
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' }
        }
      }
    },
  },
  plugins: [],
}
