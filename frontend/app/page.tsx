export default function Home() {
  return (
    <main className="min-h-screen bg-zinc-950 text-white">
      {/* HERO */}
      <section className="max-w-6xl mx-auto px-6 py-24">
        <div className="space-y-6">
          <span className="bg-zinc-800 text-zinc-300 px-4 py-2 rounded-full text-sm">
            Software Sales API
          </span>

          <h1 className="text-5xl font-bold leading-tight max-w-3xl">
            Plataforma moderna de vendas de cursos com Django REST API
          </h1>

          <p className="text-zinc-400 text-lg max-w-2xl">
            Projeto full stack com autenticação JWT, compras,
            avaliações e dashboard administrativo.
          </p>

          <div className="flex gap-4 pt-4">
            <a
              href="https://main-api-django-tu0m.onrender.com/swagger/"
              className="bg-white text-black px-6 py-3 rounded-xl font-medium hover:opacity-90"
            >
              Swagger
            </a>

            <a
              href="/dashboard"
              className="border border-zinc-700 px-6 py-3 rounded-xl hover:bg-zinc-900"
            >
              Dashboard
            </a>
          </div>
        </div>
      </section>

      {/* CARDS */}
      <section className="max-w-6xl mx-auto px-6 grid md:grid-cols-3 gap-6 pb-20">
        <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-2xl">
          <h2 className="text-xl font-semibold mb-3">
            JWT Authentication
          </h2>

          <p className="text-zinc-400">
            Sistema seguro utilizando access token e refresh token.
          </p>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-2xl">
          <h2 className="text-xl font-semibold mb-3">
            Cursos
          </h2>

          <p className="text-zinc-400">
            CRUD completo de cursos com avaliações e vendas.
          </p>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-2xl">
          <h2 className="text-xl font-semibold mb-3">
            Dashboard
          </h2>

          <p className="text-zinc-400">
            Interface moderna consumindo API REST em tempo real.
          </p>
        </div>
      </section>
    </main>
  );
}