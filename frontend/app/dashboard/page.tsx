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
  criado_por_nome?: string;
  criacao?: string;
}

export default function DashboardPage() {
  const [cursos, setCursos] = useState<Curso[]>([]);
  const [loading, setLoading] = useState(true);

  // CARREGAR CURSOS
  useEffect(() => {
    async function loadCursos() {
      try {
        const data = await getCursos();

        // CORREÇÃO PRINCIPAL (API paginada Django)
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

  // LINKS (UDemy + Google Images)
  function getCourseLinks(nome: string) {
    const query = encodeURIComponent(nome);

    return {
      udemy: `https://www.udemy.com/courses/search/?q=${query}`,
      googleImage: `https://www.google.com/search?tbm=isch&q=${query}`,
    };
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
          {cursos.map((curso) => {
            const links = getCourseLinks(curso.nome);

            return (
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
                {/* IMAGEM AUTOMÁTICA */}
                <div className="h-52 overflow-hidden">
                  <img
                    src={`https://source.unsplash.com/600x400/?${encodeURIComponent(
                      curso.nome
                    )}`}
                    alt={curso.nome}
                    className="w-full h-full object-cover"
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
                      Ativo
                    </span>
                  </div>

                  {/* BOTÕES */}
                  <div className="flex gap-3 pt-2">
                    <a
                      href={links.udemy}
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

                    <a
                      href={links.googleImage}
                      target="_blank"
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
                      📷
                    </a>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* VAZIO */}
        {cursos.length === 0 && (
          <div className="text-center py-24">
            <h2 className="text-3xl font-bold mb-4">
              Nenhum curso encontrado
            </h2>

            <p className="text-zinc-400">
              Verifique se existem cursos cadastrados na API.
            </p>
          </div>
        )}
      </section>
    </main>
  );
}
console.log("API URL:", process.env.NEXT_PUBLIC_API_URL);