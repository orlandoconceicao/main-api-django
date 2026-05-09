"use client";

import { useEffect, useState } from "react";
import { getCursos } from "../services/api";

interface Curso {
  id: number;
  nome: string;
  descricao: string;
  preco: string;
  total_vendas: number;
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

  return (
    <main className="min-h-screen bg-zinc-950 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-10">
          Dashboard
        </h1>

        <div className="grid md:grid-cols-3 gap-6">
          {cursos.map((curso) => (
            <div
              key={curso.id}
              className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6"
            >
              <h2 className="text-2xl font-semibold mb-3">
                {curso.nome}
              </h2>

              <p className="text-zinc-400 mb-4">
                {curso.descricao}
              </p>

              <div className="space-y-2">
                <p>
                  💰 R$ {curso.preco}
                </p>

                <p>
                  📈 {curso.total_vendas} vendas
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}