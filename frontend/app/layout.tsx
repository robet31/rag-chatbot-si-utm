import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Akademik SI UTM - RAG Chatbot',
  description: 'RAG Chatbot untuk informasi akademik Sistem Informasi Universitas Trunojoyo Madura',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id">
      <body>{children}</body>
    </html>
  )
}
