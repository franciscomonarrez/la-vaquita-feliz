'use client'

import { useCart } from '../context/CartContext'
import Link from 'next/link'

export default function CartSidebar() {
  const { items, removeItem, clearCart } = useCart()

  return (
    <aside className="w-80 border-l border-secondary p-4 bg-muted font-body">
      <h2 className="text-xl font-semibold mb-4 text-foreground">Tu Carrito</h2>

      {items.length === 0 ? (
        <p className="text-foreground">El carrito está vacío</p>
      ) : (
        <ul className="space-y-2">
          {items.map((item) => (
            <li
              key={item.id}
              className="flex justify-between items-center text-foreground"
            >
              <div>
                <p className="font-semibold">{item.name}</p>
                <p className="text-sm text-accent">Qty: {item.quantity}</p>
              </div>
              <button
                onClick={() => removeItem(item.id)}
                className="text-secondary font-bold"
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      )}

      {items.length > 0 && (
        <>
          <Link
            href="/carrito"
            className="block mb-2 text-center bg-primary text-white py-2 rounded-md font-semibold hover:bg-primary/90 transition"
          >
            Ver Carrito
          </Link>
          <button
            onClick={clearCart}
            className="w-full text-center text-secondary font-semibold hover:underline transition"
          >
            Limpiar Carrito
          </button>
        </>
      )}
    </aside>
  )
}