import { useState, useEffect, useRef, type FC } from "react";
import { Volume2, VolumeX } from "lucide-react";

export const AudioAmbience: FC = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioCtxRef = useRef<AudioContext | null>(null);
  const masterGainRef = useRef<GainNode | null>(null);
  const oscillatorsRef = useRef<OscillatorNode[]>([]);

  const startAmbience = () => {
    try {
      const AudioContextClass = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      const ctx = new AudioContextClass();
      audioCtxRef.current = ctx;

      const masterGain = ctx.createGain();
      masterGain.gain.setValueAtTime(0.001, ctx.currentTime);
      masterGain.gain.exponentialRampToValueAtTime(0.08, ctx.currentTime + 3);
      masterGain.connect(ctx.destination);
      masterGainRef.current = masterGain;

      // Frequências harmônicas meditativas (Acorde Zen em Lá Menor / Pentatônica Oriental)
      const freqs = [108, 162, 216, 324];
      const oscs: OscillatorNode[] = [];

      freqs.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const oscGain = ctx.createGain();

        osc.type = idx % 2 === 0 ? "sine" : "triangle";
        osc.frequency.setValueAtTime(freq, ctx.currentTime);

        // LFO sutil para movimento orgânico de vento
        const lfo = ctx.createOscillator();
        const lfoGain = ctx.createGain();
        lfo.frequency.setValueAtTime(0.15 + idx * 0.05, ctx.currentTime);
        lfoGain.gain.setValueAtTime(2.5, ctx.currentTime);
        lfo.connect(osc.frequency);
        lfo.start();

        oscGain.gain.setValueAtTime(0.25 / (idx + 1), ctx.currentTime);
        osc.connect(oscGain);
        oscGain.connect(masterGain);
        osc.start();
        oscs.push(osc);
      });

      oscillatorsRef.current = oscs;
      setIsPlaying(true);
    } catch (e) {
      console.warn("Web Audio não iniciado:", e);
    }
  };

  const stopAmbience = () => {
    if (masterGainRef.current && audioCtxRef.current) {
      const ctx = audioCtxRef.current;
      masterGainRef.current.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 1.2);
      setTimeout(() => {
        audioCtxRef.current?.close();
        audioCtxRef.current = null;
        setIsPlaying(false);
      }, 1200);
    } else {
      setIsPlaying(false);
    }
  };

  const toggleAudio = () => {
    if (isPlaying) {
      stopAmbience();
    } else {
      startAmbience();
      playChime();
    }
  };

  // Sino cerimonial ao interagir
  const playChime = () => {
    try {
      const AudioContextClass = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      const ctx = audioCtxRef.current || new AudioContextClass();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(864, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(432, ctx.currentTime + 1.8);

      gain.gain.setValueAtTime(0.12, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 2.2);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 2.2);
    } catch {
      // Ignorar falha em navegadores restritivos
    }
  };

  useEffect(() => {
    return () => {
      audioCtxRef.current?.close();
    };
  }, []);

  return (
    <div className="fixed bottom-6 right-6 z-50 flex items-center gap-2">
      <button
        onClick={toggleAudio}
        aria-label="Alternar paisagem sonora ambiente"
        className="group flex items-center gap-2.5 px-3.5 py-2 rounded-full washi-card text-xs font-mono tracking-wider uppercase text-ink-800 hover:text-crimson-700 shadow-sm hover:shadow transition-all duration-300"
      >
        <div className="relative flex items-center justify-center w-5 h-5">
          {isPlaying ? (
            <>
              <Volume2 className="w-4 h-4 text-crimson-700 animate-pulse" />
              <span className="absolute -top-1 -right-1 w-1.5 h-1.5 rounded-full bg-crimson-600 animate-ping" />
            </>
          ) : (
            <VolumeX className="w-4 h-4 text-ink-500 group-hover:text-ink-800" />
          )}
        </div>
        <span className="hidden sm:inline font-medium">
          {isPlaying ? "Áudio Atmosférico: Ativo" : "Ativar Som Zen"}
        </span>
      </button>
    </div>
  );
};
