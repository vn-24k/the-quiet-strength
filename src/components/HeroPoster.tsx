import { useState, type FC } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Download, Sparkles, Eye, CheckCircle2 } from "lucide-react";

interface HeroPosterProps {
  onInteract?: () => void;
}

export const HeroPoster: FC<HeroPosterProps> = ({ onInteract }) => {
  const [showOriginal, setShowOriginal] = useState(false);
  const [downloadSuccess, setDownloadSuccess] = useState(false);

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = "/obra-final-1para1.jpg";
    link.download = "THE-QUIET-STRENGTH-1PARA1-OBRA-FINAL.jpg";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setDownloadSuccess(true);
    setTimeout(() => setDownloadSuccess(false), 2500);
    if (onInteract) onInteract();
  };

  return (
    <section className="relative w-full max-w-5xl mx-auto px-2 sm:px-4 py-6 md:py-10 select-none">
      
      {/* Controles de Fidelidade e Ferramentas de Inspeção */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4 px-2">
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono tracking-wider bg-crimson-800 text-white font-semibold shadow">
            <Sparkles className="w-3.5 h-3.5" />
            PARIDADE 1:1 CONCLUÍDA
          </span>
          <span className="hidden sm:inline-block font-mono text-[11px] text-ink-600 uppercase">
            // FACE-SWAP EDITORIAL ALINHADO
          </span>
        </div>

        <div className="flex items-center gap-2">
          {/* Botão de Alternar Referência Original vs Obra Final */}
          <button
            onClick={() => setShowOriginal(!showOriginal)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full font-mono text-xs tracking-wider uppercase transition-all shadow-sm border ${
              showOriginal
                ? "bg-amber-600 text-white border-amber-700"
                : "bg-white/80 hover:bg-white text-ink-900 border-ink-900/15"
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            {showOriginal ? "Ver Sua Obra (Com Seu Rosto)" : "Comparar c/ Original"}
          </button>

          {/* Botão de Download em Alta Resolução */}
          <button
            onClick={handleDownload}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-ink-900 hover:bg-ink-800 text-[#f5f2eb] font-mono text-xs tracking-wider uppercase transition-all shadow-sm"
          >
            {downloadSuccess ? (
              <>
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                Baixado!
              </>
            ) : (
              <>
                <Download className="w-3.5 h-3.5" />
                Baixar Pôster
              </>
            )}
          </button>
        </div>
      </div>

      {/* =========================================================================
          POSTER PRINCIPAL 1:1 - MOLDURA EDITORIAL DE MUSEU
          ========================================================================= */}
      <div className="relative bg-[#efece4] border border-[#d2cbba] shadow-2xl p-2 sm:p-4 md:p-6 overflow-hidden">
        
        {/* Textura de Fundo Papel Washi Clássico */}
        <div 
          className="absolute inset-0 pointer-events-none opacity-20" 
          style={{
            backgroundImage: "radial-gradient(#9e9686 0.75px, transparent 0.75px)",
            backgroundSize: "24px 24px"
          }}
        />

        {/* Linha vertical de dobra sutil de papel antigo no centro */}
        <div className="absolute top-0 bottom-0 left-1/2 w-px bg-black/5 pointer-events-none" />

        {/* Container Central com Transição Animada Suave */}
        <div className="relative w-full max-w-3xl mx-auto flex flex-col items-center justify-center">
          <AnimatePresence mode="wait">
            {showOriginal ? (
              <motion.div
                key="original"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="relative w-full overflow-hidden border border-amber-600/40 shadow-xl"
              >
                <div className="absolute top-3 left-3 z-30 px-2.5 py-1 bg-amber-600 text-white font-mono text-[10px] tracking-widest uppercase font-bold shadow">
                  REFERÊNCIA ORIGINAL SORTEADA
                </div>
                <img
                  src="/referencia-sorteada.jpg"
                  alt="Referência Original Sorteada - The Quiet Strength"
                  className="w-full h-auto object-contain block"
                />
              </motion.div>
            ) : (
              <motion.div
                key="sua-obra"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="relative w-full overflow-hidden border border-ink-900/20 shadow-2xl"
              >
                <div className="absolute top-3 left-3 z-30 px-2.5 py-1 bg-crimson-800 text-white font-mono text-[10px] tracking-widest uppercase font-bold shadow flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  OBRA FINAL 1:1 • SEU ROSTO
                </div>
                <img
                  src="/obra-final-1para1.jpg"
                  alt="Obra Final com Rosto do Usuário - The Quiet Strength"
                  className="w-full h-auto object-contain block"
                />
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Metadados Editoriais Inferiores */}
        <div className="mt-4 pt-3 border-t border-ink-900/10 flex flex-wrap items-center justify-between gap-2 font-mono text-[10px] text-ink-600">
          <div>
            ARQUIVO: <span className="font-bold text-ink-900">THE QUIET STRENGTH / SHADOW ARCHIVE NO. 01</span>
          </div>
          <div>
            TATUAGEM NO PESCOÇO: <span className="font-bold text-crimson-800">花樣年華</span>
          </div>
          <div>
            LOCALIDADE: <span className="font-bold text-ink-900">KYOTO, JP</span> • 2026
          </div>
        </div>

      </div>
    </section>
  );
};
