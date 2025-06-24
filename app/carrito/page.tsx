
'use client'

import { useCart } from '../../context/CartContext'
import Link from 'next/link'

export default function CarritoPage() {
  const { items, removeItem, clearCart } = useCart()
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0)

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Tu Carrito</h1>
      {items.length === 0 ? (
        <p>
          Tu carrito está vacío.{' '}
          <Link href="/productos" className="text-red-600">
            Ver productos
          </Link>
        </p>
      ) : (
        <>
          <ul className="space-y-4 mb-6">
            {items.map((item) => (
              <li key={item.id} className="flex justify-between items-center">
                <span>{item.name} x {item.quantity}</span>
                <span>${item.price * item.quantity}</span>
                <button
                  onClick={() => removeItem(item.id)}
                  className="text-red-600"
                >
                  Eliminar
                </button>
              </li>
            ))}
          </ul>
          <div className="text-right font-bold mb-6">Total: ${total}</div>
          <button className="bg-red-600 text-white px-4 py-2 rounded">
            Checkout
          </button>
          <button onClick={clearCart} className="ml-4 text-red-600">
            Limpiar Carrito
          </button>
        </>
      )}
    </div>
  )
}
