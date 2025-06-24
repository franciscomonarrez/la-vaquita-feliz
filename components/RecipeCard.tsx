'use client'

import Image from 'next/image'
import type { Recipe } from '../data/recipes'

export default function RecipeCard({ recipe }: { recipe: Recipe }) {
  return (
    <div className="border rounded-lg overflow-hidden font-body hover:shadow-lg transition">
      <Image
        src={recipe.imageUrl}
        alt={recipe.title}
        width={400}
        height={250}
        className="object-cover"
      />
      <div className="p-4">
        <h2 className="text-2xl font-bold mb-2 font-header">{recipe.title}</h2>
        <p className="text-foreground mb-4">{recipe.description}</p>
        <ul className="list-disc list-inside mb-4">
          {recipe.ingredients.map((ing, i) => (
            <li key={i}>{ing}</li>
          ))}
        </ul>
        <ol className="list-decimal list-inside">
          {recipe.steps.map((step, i) => (
            <li key={i} className="mb-2">{step}</li>
          ))}
        </ol>
      </div>
    </div>
  )
}