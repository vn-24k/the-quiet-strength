import { useEffect, useState, type FC } from "react";
import { motion, useSpring } from "framer-motion";

export const CustomCursor: FC = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [isPointer, setIsPointer] = useState(false);

  const cursorX = useSpring(0, { damping: 25, stiffness: 350 });
  const cursorY = useSpring(0, { damping: 25, stiffness: 350 });
  const dotX = useSpring(0, { damping: 45, stiffness: 600 });
  const dotY = useSpring(0, { damping: 45, stiffness: 600 });

  useEffect(() => {
    // Apenas ativa o cursor customizado em dispositivos com mouse
    if (window.matchMedia("(pointer: coarse)").matches) {
      return;
    }

    const moveCursor = (e: MouseEvent) => {
      cursorX.set(e.clientX - 16);
      cursorY.set(e.clientY - 16);
      dotX.set(e.clientX - 3);
      dotY.set(e.clientY - 3);
      setIsVisible(true);

      const target = e.target as HTMLElement | null;
      if (
        target?.tagName === "BUTTON" ||
        target?.tagName === "A" ||
        target?.closest("button") ||
        target?.closest("a") ||
        target?.getAttribute("role") === "button"
      ) {
        setIsPointer(true);
      } else {
        setIsPointer(false);
      }
    };

    const handleMouseLeave = () => setIsVisible(false);
    const handleMouseEnter = () => setIsVisible(true);

    window.addEventListener("mousemove", moveCursor);
    document.addEventListener("mouseleave", handleMouseLeave);
    document.addEventListener("mouseenter", handleMouseEnter);

    return () => {
      window.removeEventListener("mousemove", moveCursor);
      document.removeEventListener("mouseleave", handleMouseLeave);
      document.removeEventListener("mouseenter", handleMouseEnter);
    };
  }, [cursorX, cursorY, dotX, dotY]);

  if (!isVisible) return null;

  return (
    <>
      <motion.div
        className="pointer-events-none fixed top-0 left-0 z-[9999] rounded-full border border-crimson-700/60 transition-transform duration-100 ease-out hidden md:block"
        style={{
          x: cursorX,
          y: cursorY,
          width: isPointer ? 42 : 32,
          height: isPointer ? 42 : 32,
          backgroundColor: isPointer ? "rgba(139, 14, 14, 0.08)" : "transparent",
        }}
      />
      <motion.div
        className="pointer-events-none fixed top-0 left-0 z-[9999] w-1.5 h-1.5 rounded-full bg-crimson-700 hidden md:block"
        style={{
          x: dotX,
          y: dotY,
        }}
      />
    </>
  );
};
