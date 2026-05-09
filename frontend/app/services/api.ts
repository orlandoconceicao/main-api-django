const API_URL = "https://main-api-django-tu0m.onrender.com/api";

export async function getCursos() {
  const response = await fetch(`${API_URL}/cursos/`);

  if (!response.ok) {
    throw new Error("Erro ao buscar cursos");
  }

  return response.json();
}