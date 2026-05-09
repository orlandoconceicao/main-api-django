const API_URL =
  process.env.NEXT_PUBLIC_API_URL;

export async function getCursos() {
  const response = await fetch(
    `${API_URL}/api/cursos/`
  );

  return response.json();
}