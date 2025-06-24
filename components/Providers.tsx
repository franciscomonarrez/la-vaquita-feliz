'use client'

import { ReactNode } from 'react'
import { CartProvider } from '../context/CartContext'
import Header from './Header'
import Footer from './Footer'
import CartSidebar from './CartSidebar'

export default function Providers({ children }: { children: ReactNode }) {
  return (
    <CartProvider>
      <Header />
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row lg:space-x-8">
          <main className="flex-1 w-full lg:w-auto">
            {children}
          </main>
          <aside className="w-full lg:w-80 mt-6 lg:mt-0">
            <CartSidebar />
          </aside>
        </div>
      </div>
      <Footer />
    </CartProvider>
  )
}