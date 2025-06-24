
import { products } from '../../data/products'
import ProductCard from '../../components/ProductCard'

export default function ProductosPage() {
  return (
    <>
      <h1 className="text-3xl font-bold mb-6">Productos</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </>
  )
}
