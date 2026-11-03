import { useState } from "react";
import { HeroPoster } from "./components/HeroPoster";
import { VisualArchiveSeries } from "./components/VisualArchiveSeries";
import { PhilosophicalManifesto } from "./components/PhilosophicalManifesto";
import { Footer } from "./components/Footer";
import { AudioAmbience } from "./components/AudioAmbience";
import { CustomCursor } from "./components/CustomCursor";

export function App() {
  const [viewMode, setViewMode] = useState<"full" | "poster-only">("full");

  return (
    <div className="min-h-screen bg-[#f3efe6] text-ink-900 font-sans selection:bg-crimson-700 selection:text-white">
      {/* Cursor Tátil */}
      <CustomCursor />

      {/* Áudio Ambiente Meditativo Procedural */}
      <AudioAmbience />

      {/* Barra de Navegação Flutuante Minimalista */}
      <nav className="sticky top-0 z-40 w-full bg-[#f3efe6]/90 backdrop-blur-md border-b border-ink-900/10 transition-all">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
          
          {/* Logo Minimalista */}
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 bg-crimson-700" />
            <span className="font-serif font-black text-sm tracking-widest text-ink-900">
              SHADOW
            </span>
            <span className="hidden sm:inline font-mono text-[10px] text-ink-500 tracking-widest uppercase">
              // ARCHIVE NO. 01
            </span>
          </div>

          {/* Links e Alternador de Visão */}
          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-6 font-mono text-xs uppercase tracking-wider text-ink-600">
              <a href="#poster" className="hover:text-crimson-700 transition-colors">Obra Principal</a>
              <a href="#series" className="hover:text-crimson-700 transition-colors">Human Instincts</a>
              <a href="#manifesto" className="hover:text-crimson-700 transition-colors">Manifesto</a>
            </div>

            <div className="flex items-center gap-1.5 p-1 bg-ink-900/5 rounded-full border border-ink-900/10">
              <button
                onClick={() => setViewMode("full")}
                className={`px-3 py-1 rounded-full text-[11px] font-mono tracking-wider uppercase transition-all ${
                  viewMode === "full"
                    ? "bg-ink-900 text-[#f5f2eb] font-semibold shadow-sm"
                    : "text-ink-600 hover:text-ink-900"
                }`}
              >
                Experiência
              </button>
              <button
                onClick={() => setViewMode("poster-only")}
                className={`px-3 py-1 rounded-full text-[11px] font-mono tracking-wider uppercase transition-all ${
                  viewMode === "poster-only"
                    ? "bg-crimson-700 text-white font-semibold shadow-sm"
                    : "text-ink-600 hover:text-ink-900"
                }`}
              >
                Poster 1:1
              </button>
            </div>
          </div>

        </div>
      </nav>

      {/* Conteúdo Principal */}
      <main id="poster">
        <HeroPoster />

        {viewMode === "full" && (
          <>
            <div id="series">
              <VisualArchiveSeries />
            </div>

            <div id="manifesto">
              <PhilosophicalManifesto />
            </div>
          </>
        )}
      </main>

      {/* Rodapé */}
      <Footer />
    </div>
  );
}

export default App;
