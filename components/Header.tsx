// File: components/Header.tsx
import Link from 'next/link'

export default function Header() {
  return (
    <header className="bg-primary text-white">
      <div className="container mx-auto flex items-center justify-between p-4">
        <Link href="/">
          <span className="text-2xl font-bold">La Vaquita Feliz</span>
        </Link>
        <nav className="space-x-6">
          <Link href="/productos" className="hover:underline">
            Productos
          </Link>
          <Link href="/recetas" className="hover:underline">
            Recetas
          </Link>
          <Link href="/nosotros" className="hover:underline">
            Nosotros
          </Link>
        </nav>
        <Link href="/carrito">
          <button className="relative">
            🛒
          </button>
        </Link>
      </div>
    </header>
  )
}
