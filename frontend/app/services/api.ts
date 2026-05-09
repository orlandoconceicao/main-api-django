const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getCursos() {
  const res = await fetch(`${API_URL}/api/cursos/`);

  if (!res.ok) {
    throw new Error("Erro ao buscar cursos");
  }

  return res.json();
}