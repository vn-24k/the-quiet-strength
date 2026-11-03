import { useState, type FC } from "react";
import { motion } from "framer-motion";
import { Shield, Eye, Flame, Anchor, Wind, ArrowUpRight } from "lucide-react";

interface Pillar {
  id: string;
  kanji: string;
  name: string;
  romanji: string;
  description: string;
  quote: string;
  icon: React.ElementType;
  meta: string;
}

const pillars: Pillar[] = [
  {
    id: "01",
    kanji: "規律",
    name: "Discipline",
    romanji: "Kiritsu",
    description: "A repetição ritualística no escuro, antes que a luz do sol toque a lâmina.",
    quote: "A disciplina não é uma prisão; é a forja onde a vontade se torna inquebrável.",
    icon: Shield,
    meta: "KATANA // PURE STEEL"
  },
  {
    id: "02",
    kanji: "集中",
    name: "Focus",
    romanji: "Shūchū",
    description: "Eliminar todo ruído externo até que reste apenas o movimento exato e intencional.",
    quote: "Onde o olhar descansa com clareza, a dúvida simplesmente deixa de existir.",
    icon: Eye,
    meta: "CLARITY // UNWAVERING"
  },
  {
    id: "03",
    kanji: "忍耐",
    name: "Patience",
    romanji: "Nintai",
    description: "Esperar sem pressa, como a pedra do riacho polida pelo fluxo perpétuo da água.",
    quote: "A árvore mais sólida é aquela que suportou invernos inteiros em silêncio absoluto.",
    icon: Anchor,
    meta: "TIMELESS // TEMPERED"
  },
  {
    id: "04",
    kanji: "回復力",
    name: "Resilience",
    romanji: "Kaifukuryoku",
    description: "A quietude diante da tempestade. Carregar cicatrizes não como vergonha, mas como ouro.",
    quote: "Kintsugi interior: reconstruído com paciência, mais valioso após a ruptura.",
    icon: Flame,
    meta: "KINTSUGI // GOLD SEAL"
  },
  {
    id: "05",
    kanji: "自由",
    name: "Freedom",
    romanji: "Jiyū",
    description: "O desapego completo do medo de perder. Caminhar livre pelas montanhas sem amarras.",
    quote: "Livre não é quem faz o que quer, mas quem não é escravo de suas próprias fraquezas.",
    icon: Wind,
    meta: "WIND // INFINITE VOID"
  }
];

export const VisualArchiveSeries: FC = () => {
  const [selectedPillar, setSelectedPillar] = useState<string>("04");

  return (
    <section className="relative w-full max-w-6xl mx-auto px-4 sm:px-6 py-16 border-t border-ink-900/10">
      
      {/* Título da Seção */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
        <div>
          <div className="flex items-center gap-2 font-mono text-xs text-crimson-800 tracking-[0.25em] uppercase mb-2">
            <span className="w-2 h-2 bg-crimson-700" />
            <span>SERIES 01 // DEEP EXPLORATION</span>
          </div>
          <h2 className="font-serif font-black text-3xl sm:text-5xl text-ink-900 tracking-tight">
            HUMAN INSTINCTS
          </h2>
          <p className="font-mono text-xs sm:text-sm text-ink-600 tracking-wider mt-2">
            Os cinco preceitos fundamentais da resiliência silenciosa.
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs text-ink-500">
          <span>CATALOG NO. 01—05</span>
          <span className="w-12 h-px bg-ink-900/20" />
          <span className="text-crimson-800 font-semibold">KYOTO PROTOCOL</span>
        </div>
      </div>

      {/* Grid de 5 Pilares em Cartões Interativos */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        {pillars.map((pillar) => {
          const isSelected = selectedPillar === pillar.id;
          const Icon = pillar.icon;

          return (
            <motion.div
              key={pillar.id}
              onClick={() => setSelectedPillar(pillar.id)}
              whileHover={{ y: -4 }}
              transition={{ duration: 0.2 }}
              className={`relative cursor-pointer p-5 rounded-sm transition-all duration-300 border ${
                isSelected
                  ? "bg-ink-900 text-[#f5f2eb] border-crimson-700 shadow-xl"
                  : "bg-[#faf8f5] text-ink-900 border-ink-900/15 hover:border-crimson-700/60"
              }`}
            >
              {/* Header do Card */}
              <div className="flex items-start justify-between mb-6">
                <span className={`font-mono text-xs tracking-widest ${isSelected ? "text-crimson-500 font-bold" : "text-ink-400"}`}>
                  [{pillar.id}]
                </span>
                <span className={`font-kanji text-xl font-bold ${isSelected ? "text-crimson-500" : "text-ink-700"}`}>
                  {pillar.kanji}
                </span>
              </div>

              <div className="space-y-2">
                <h3 className="font-serif font-bold text-xl tracking-wide">
                  {pillar.name}
                </h3>
                <p className={`font-mono text-[10px] tracking-wider uppercase ${isSelected ? "text-ink-400" : "text-ink-500"}`}>
                  {pillar.romanji}
                </p>
                <p className={`text-xs leading-relaxed pt-2 ${isSelected ? "text-[#e5dfd3]" : "text-ink-600"}`}>
                  {pillar.description}
                </p>
              </div>

              <div className="mt-8 pt-4 border-t border-current/10 flex items-center justify-between">
                <Icon className={`w-4 h-4 ${isSelected ? "text-crimson-500" : "text-ink-500"}`} />
                <ArrowUpRight className={`w-3.5 h-3.5 transition-transform ${isSelected ? "rotate-45 text-crimson-500" : "text-ink-400"}`} />
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Caixa de Citação do Pilar Ativo */}
      <div className="mt-8 p-6 bg-ink-900 text-[#f5f2eb] rounded-sm border-l-4 border-crimson-700 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-lg">
        <div className="space-y-1">
          <p className="font-mono text-[10px] tracking-[0.2em] text-crimson-500 uppercase">
            PRINCÍPIO SELECIONADO // {pillars.find(p => p.id === selectedPillar)?.name.toUpperCase()}
          </p>
          <p className="font-serif italic text-base sm:text-lg text-[#faf8f5]">
            "{pillars.find(p => p.id === selectedPillar)?.quote}"
          </p>
        </div>
        <div className="shrink-0 font-mono text-[10px] text-ink-400 tracking-widest uppercase">
          {pillars.find(p => p.id === selectedPillar)?.meta}
        </div>
      </div>

    </section>
  );
};
