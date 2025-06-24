import './globals.css'
import Providers from '../components/Providers'

export const metadata = {
  title: 'La Vaquita Feliz',
  description: 'Machaca y carne seca artesanal – tienda en línea',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className="min-h-screen flex flex-col bg-background text-foreground font-body">
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}