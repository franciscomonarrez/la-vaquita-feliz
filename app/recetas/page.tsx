
import { recipes } from '../../data/recipes'
import RecipeCard from '../../components/RecipeCard'

export default function RecetasPage() {
  return (
    <>
      <h1 className="text-3xl font-bold mb-6">Recetas</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {recipes.map((rec) => (
          <RecipeCard key={rec.id} recipe={rec} />
        ))}
      </div>
    </>
  )
}