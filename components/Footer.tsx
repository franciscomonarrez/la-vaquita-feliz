// File: components/Footer.tsx
export default function Footer() {
    return (
      <footer className="bg-background text-foreground">
        <div className="container mx-auto text-center p-4">
          © {new Date().getFullYear()} La Vaquita Feliz. Todos los derechos
          reservados.
        </div>
      </footer>
    )
  }
  