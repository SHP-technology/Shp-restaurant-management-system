import { motion } from 'framer-motion'
import type { ReactNode } from 'react'

const pageVariants = {
  initial: {
    opacity: 0,
    x: 40,
    scale: 0.985,
  },
  animate: {
    opacity: 1,
    x: 0,
    scale: 1,
    transition: {
      duration: 0.35,
      ease: [0.16, 1, 0.3, 1] as const,
    },
  },
  exit: {
    opacity: 0,
    x: -40,
    scale: 0.985,
    transition: {
      duration: 0.25,
      ease: [0.7, 0, 0.84, 0] as const,
    },
  },
}

export function PageTransition({ children }: { children: ReactNode }) {
  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      className="min-h-screen w-full overflow-x-hidden"
    >
      {children}
    </motion.div>
  )
}
