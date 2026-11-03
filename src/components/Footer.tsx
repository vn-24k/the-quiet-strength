import { type FC } from "react";

export const Footer: FC = () => {
  return (
    <footer className="w-full bg-[#ebe7de] border-t border-ink-900/15 py-12 px-4 sm:px-6">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
        
        {/* Identidade */}
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 bg-crimson-700" />
          <div>
            <p className="font-serif font-bold text-sm tracking-widest text-ink-900">SHADOW / VISUAL ARCHIVE</p>
            <p className="font-mono text-[9px] text-ink-500 tracking-[0.2em] uppercase">SERIES 01 // KYOTO 2026</p>
          </div>
        </div>

        {/* Kanji Central */}
        <div className="font-kanji text-sm font-semibold tracking-[0.4em] text-ink-600">
          静けさの中の強さ · 花樣年華
        </div>

        {/* Metadados & Direitos */}
        <div className="text-right font-mono text-[10px] text-ink-500 space-y-0.5">
          <p>© 2026 SHADOW ARCHIVE. TODOS OS DIREITOS RESERVADOS.</p>
          <p className="text-crimson-800 font-medium">DESIGN EDITORIAL DE ALTA FIDELIDADE 1:1</p>
        </div>

      </div>
    </footer>
  );
};
