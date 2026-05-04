import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import ThemeProvider from '@/components/ThemeProvider'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Course Companion — Agentic AI Course',
  description: 'Learn Agentic AI development with 10 structured chapters and quizzes.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} bg-gray-50 dark:bg-slate-950 text-gray-900 dark:text-slate-100 min-h-screen transition-colors duration-300`}>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
