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

  useEffect(() => {
    async function loadCursos() {
      try {
        const data = await getCursos();
        setCursos(data.results || []);
      } catch (error) {
        console.error(error);
      }
    }

    loadCursos();
  }, []);

  function getUdemyLink(nome: string) {
    const links: Record<string, string> = {
      "Engenharia de software":
        "https://www.udemy.com/topic/software-engineering/",

      "Analise e desenvolvimento de sistemas":
        "https://www.udemy.com/topic/software-development/",

      "Cibersegurança":
        "https://www.udemy.com/topic/cyber-security/",
    };

    return links[nome] || "https://www.udemy.com/";
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
            Plataforma moderna de vendas de cursos integrada
            com Django REST Framework.
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
                hover:border-zinc-700
                transition
              "
            >
              {/* IMAGEM */}
              <div className="h-52 overflow-hidden">
                <img
                  src={`https://picsum.photos/600/400?random=${curso.id}`}
                  alt={curso.nome}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* CONTEÚDO */}
              <div className="p-6 space-y-5">
                <div>
                  <h2 className="text-2xl font-bold mb-3">
                    {curso.nome}
                  </h2>

                  <p className="text-zinc-400 line-clamp-4">
                    {curso.descricao}
                  </p>
                </div>

                {/* MÉTRICAS */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-zinc-800 rounded-2xl p-4">
                    <p className="text-zinc-400 text-sm mb-1">
                      Preço
                    </p>

                    <h3 className="text-2xl font-bold">
                      R$ {curso.preco}
                    </h3>
                  </div>

                  <div className="bg-zinc-800 rounded-2xl p-4">
                    <p className="text-zinc-400 text-sm mb-1">
                      Avaliação
                    </p>

                    <h3 className="text-2xl font-bold">
                      ⭐ {curso.media_avaliacoes}
                    </h3>
                  </div>
                </div>

                {/* VENDAS */}
                <div className="flex items-center justify-between">
                  <p className="text-zinc-400">
                    {curso.total_vendas} vendas
                  </p>

                  <span className="bg-green-500/20 text-green-400 text-sm px-3 py-1 rounded-full">
                    Disponível
                  </span>
                </div>

                {/* BOTÕES */}
                <div className="flex gap-3 pt-2">
                  <a
                    href={getUdemyLink(curso.nome)}
                    target="_blank"
                    className="
                      flex-1
                      bg-white
                      text-black
                      text-center
                      py-3
                      rounded-2xl
                      font-semibold
                      hover:opacity-90
                      transition
                    "
                  >
                    Ver na Udemy
                  </a>

                  <button
                    className="
                      px-5
                      py-3
                      border
                      border-zinc-700
                      rounded-2xl
                      hover:bg-zinc-800
                      transition
                    "
                  >
                    API
                  </button>
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
              Cadastre cursos no Django Admin.
            </p>
          </div>
        )}
      </section>
    </main>
  );
}