'use client'

import Image from 'next/image'
import { ShoppingCart } from 'lucide-react'
import { useCart } from '../context/CartContext'
import type { Product } from '../data/products'

export default function ProductCard({ product }: { product: Product }) {
  const { addItem } = useCart()
  return (
    <div className="border rounded-lg p-6 flex flex-col font-body hover:shadow-lg transition">
      <Image
        src={product.imageUrl}
        alt={product.name}
        width={300}
        height={200}
        className="object-cover rounded-md mb-4"
      />
      <h2 className="text-xl font-semibold mb-2 font-header">{product.name}</h2>
      <p className="text-foreground mb-4 flex-1">{product.description}</p>
      <div className="flex items-center justify-between">
        <span className="text-lg font-bold text-primary">${product.price}</span>
        <button
          onClick={() => addItem(product)}
          className="bg-primary text-white px-3 py-1 rounded-md flex items-center hover:bg-primary/90 transition"
        >
          <ShoppingCart size={16} className="mr-1" /> Añadir
        </button>
      </div>
    </div>
  )
}