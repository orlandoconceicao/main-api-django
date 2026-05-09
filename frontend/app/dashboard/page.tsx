"use client";

import { useEffect, useState } from "react";
import { getCursos } from "../services/api";

interface Curso {
  id: number;
  nome: string;
  descricao: string;
  preco: string;
  total_vendas: number;
  media_avaliacoes: string;
}

export default function DashboardPage() {
  const [cursos, setCursos] = useState<Curso[]>([]);
  const [loading, setLoading] = useState(true);

  // CARREGAR CURSOS
  useEffect(() => {
    async function loadCursos() {
      try {
        const data = await getCursos();

        const cursosFormatados = Array.isArray(data)
          ? data
          : data?.results || [];

        setCursos(cursosFormatados);
      } catch (error) {
        console.error("Erro ao carregar cursos:", error);
      } finally {
        setLoading(false);
      }
    }

    loadCursos();
  }, []);

  // CAPA FIXA (FUNCIONA EM PRODUÇÃO)
  function getCourseImage(nome: string) {
    const images: Record<string, string> = {
      "Engenharia de software":
        "https://images.unsplash.com/photo-1518770660439-4636190af475",

      "Analise e desenvolvimento de sistemas":
        "https://images.unsplash.com/photo-1555066931-4365d14bab8c",

      "Cibersegurança":
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b",
    };

    return (
      images[nome] ||
      "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5"
    );
  }

  // LOADING
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-zinc-950 text-white">
        <p className="text-xl animate-pulse">Carregando cursos...</p>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-white">
      {/* HEADER */}
      <section className="border-b border-zinc-800">
        <div className="max-w-7xl mx-auto px-6 py-10">
          <h1 className="text-5xl font-bold mb-4">
            Dashboard de Cursos
          </h1>

          <p className="text-zinc-400 text-lg max-w-2xl">
            Plataforma moderna de vendas de cursos integrada com Django REST Framework.
          </p>
        </div>
      </section>

      {/* CURSOS */}
      <section className="max-w-7xl mx-auto px-6 py-14">
        <div className="grid md:grid-cols-3 gap-8">
          {cursos.map((curso) => (
            <div
              key={curso.id}
              className="
                bg-zinc-900
                border border-zinc-800
                rounded-3xl
                overflow-hidden
                hover:border-zinc-600
                transition
                hover:scale-[1.02]
              "
            >
              {/* 🖼️ CAPA */}
              <div className="h-52 overflow-hidden">
                <img
                  src={getCourseImage(curso.nome)}
                  alt={curso.nome}
                  className="w-full h-full object-cover"
                  loading="lazy"
                />
              </div>

              {/* CONTEÚDO */}
              <div className="p-6 space-y-5">
                <div>
                  <h2 className="text-2xl font-bold mb-2">
                    {curso.nome}
                  </h2>

                  <p className="text-zinc-400 text-sm line-clamp-3">
                    {curso.descricao}
                  </p>
                </div>

                {/* MÉTRICAS */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-zinc-800 rounded-2xl p-4">
                    <p className="text-zinc-400 text-sm">Preço</p>
                    <h3 className="text-xl font-bold">
                      R$ {curso.preco}
                    </h3>
                  </div>

                  <div className="bg-zinc-800 rounded-2xl p-4">
                    <p className="text-zinc-400 text-sm">Nota</p>
                    <h3 className="text-xl font-bold">
                      ⭐ {curso.media_avaliacoes}
                    </h3>
                  </div>
                </div>

                {/* VENDAS */}
                <div className="flex justify-between text-sm text-zinc-400">
                  <span>{curso.total_vendas} vendas</span>

                  <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-xs">
                    Disponível
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* SEM CURSOS */}
        {cursos.length === 0 && (
          <div className="text-center py-24">
            <h2 className="text-3xl font-bold mb-4">
              Nenhum curso encontrado
            </h2>

            <p className="text-zinc-400">
              Verifique a API ou cadastre cursos no Django admin.
            </p>
          </div>
        )}
      </section>
    </main>
  );
}