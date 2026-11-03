import { useState, type FC } from "react";
import { Sparkles, CheckCircle2, Download } from "lucide-react";

export const PhilosophicalManifesto: FC = () => {
  const [downloaded, setDownloaded] = useState(false);

  const handleDownload = () => {
    setDownloaded(true);
    setTimeout(() => setDownloaded(false), 3000);
  };

  return (
    <section className="relative w-full max-w-6xl mx-auto px-4 sm:px-6 py-20 border-t border-ink-900/10">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        
        {/* Lado Esquerdo: Tipografia Monumental do Manifesto */}
        <div className="lg:col-span-7 space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-crimson-700/10 border border-crimson-700/30 rounded-full text-crimson-800 font-mono text-[11px] tracking-widest uppercase">
            <Sparkles className="w-3.5 h-3.5" />
            <span>MANIFESTO // O PODER DO SILÊNCIO</span>
          </div>

          <h2 className="font-serif font-black text-3xl sm:text-5xl md:text-6xl text-ink-900 leading-[1.05] tracking-tight">
            A verdadeira força não precisa levantar a voz para dominar o espaço.
          </h2>

          <p className="font-sans text-sm sm:text-base text-ink-700 leading-relaxed max-w-xl">
            Em uma era de ruído perpétuo, a serenidade tornou-se o ato máximo de insubordinação. 
            <strong> The Quiet Strength</strong> é um estudo visual e filosófico sobre quem caminha firme 
            através das tempestades com elegância inabalável.
          </p>

          <div className="pt-4 flex flex-wrap items-center gap-4">
            <button
              onClick={handleDownload}
              className="shimmer-button text-white px-7 py-3.5 rounded-sm font-mono text-xs font-bold tracking-[0.2em] uppercase shadow-lg hover:shadow-crimson-900/30 flex items-center gap-3 transition-transform active:scale-95"
            >
              {downloaded ? (
                <>
                  <CheckCircle2 className="w-4 h-4 text-white" />
                  <span>Poster Baixado // Alta Resolução</span>
                </>
              ) : (
                <>
                  <Download className="w-4 h-4 text-white" />
                  <span>Baixar Obra em Alta Resolução (300 DPI)</span>
                </>
              )}
            </button>

            <a
              href="#poster"
              className="px-6 py-3.5 bg-transparent border border-ink-900/20 text-ink-900 font-mono text-xs font-semibold tracking-widest uppercase hover:bg-ink-900 hover:text-[#f5f2eb] transition-all"
            >
              Ver Detalhes do Acervo
            </a>
          </div>

          <div className="pt-4 flex items-center gap-6 text-[11px] font-mono text-ink-500">
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-crimson-700" />
              Edição Oficial Series 01
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-ink-900" />
              Kyoto Archive Protocol
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-crimson-700" />
              Fidelidade Visual 1:1
            </span>
          </div>
        </div>

        {/* Lado Direito: Certificado / Ficha Técnica Editorial */}
        <div className="lg:col-span-5 bg-ink-900 text-[#f5f2eb] p-6 sm:p-8 rounded-sm border border-ink-800 shadow-2xl relative">
          <div className="absolute top-0 right-0 transform translate-x-2 -translate-y-2">
            <div className="hanko-seal w-12 h-12 rounded-sm flex items-center justify-center shadow-lg">
              <span className="font-kanji text-xl font-bold text-white">道</span>
            </div>
          </div>

          <div className="space-y-4">
            <p className="font-mono text-xs text-crimson-500 tracking-[0.25em] uppercase font-bold">
              CERTIFICADO DE AUTENTICIDADE
            </p>

            <div className="border-t border-b border-ink-800 py-4 space-y-3 font-mono text-xs">
              <div className="flex justify-between">
                <span className="text-ink-400">TÍTULO:</span>
                <span className="text-[#f5f2eb] font-semibold">THE QUIET STRENGTH</span>
              </div>
              <div className="flex justify-between">
                <span className="text-ink-400">SÉRIE:</span>
                <span className="text-[#f5f2eb]">01 — HUMAN INSTINCTS</span>
              </div>
              <div className="flex justify-between">
                <span className="text-ink-400">PERSONAGEM:</span>
                <span className="text-crimson-400 font-semibold">花樣年華 (CONTEMPORARY SAMURAI)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-ink-400">LOCALIZAÇÃO:</span>
                <span className="text-[#f5f2eb]">KYOTO, JAPAN // 2026</span>
              </div>
              <div className="flex justify-between">
                <span className="text-ink-400">PALETA:</span>
                <span className="text-crimson-400">WASHI OFF-WHITE & CRIMSON #8B0E0E</span>
              </div>
            </div>

            <p className="font-serif italic text-xs text-ink-300 leading-relaxed">
              "A quietude de espírito é a raiz de onde toda grandeza genuína floresce."
            </p>

            <div className="pt-2 flex items-center justify-between text-[10px] font-mono text-ink-500">
              <span>SHA-256 VERIFIED</span>
              <span className="text-crimson-500 font-bold">LIMITED ARCHIVE RUN</span>
            </div>
          </div>
        </div>

      </div>
    </section>
  );
};
