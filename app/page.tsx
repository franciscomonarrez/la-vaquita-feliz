import Link from 'next/link'
import Image from 'next/image'

export default function HomePage() {
  return (
    <>
      {/* Hero Section */}
      <section className="bg-primary text-white py-20 font-header">
        <div className="container mx-auto flex flex-col-reverse md:flex-row items-center px-4">
          <div className="md:w-1/2 mt-8 md:mt-0">
            <Image
              src="/images/hero-machaca.jpg"
              alt="Machaca artesanal"
              width={600}
              height={400}
              className="rounded-lg shadow-lg"
            />
          </div>
          <div className="md:w-1/2 md:pl-12 text-center md:text-left">
            <h1 className="text-5xl mb-4 leading-tight">
              Bienvenidos a <span className="text-accent">La Vaquita Feliz</span>
            </h1>
            <p className="text-lg mb-6 font-body">
              Descubre nuestra machaca y carne seca artesanal, elaborada con pasión en Sinaloa.
            </p>
            <div className="space-x-4">
              <Link href="/productos" className="px-6 py-3 bg-secondary hover:bg-secondary/90 text-white font-semibold rounded-md transition">
                Ver Productos
              </Link>
              <Link href="/recetas" className="px-6 py-3 bg-accent hover:bg-accent/90 text-foreground font-semibold rounded-md transition">
                Ver Recetas
              </Link>
            </div>
          </div>
        </div>
      </section>
      {/* Featured Products & Call to Action omitted for brevity */}
    </>
  )
}