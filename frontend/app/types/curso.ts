export interface Curso {
  id: number;
  nome: string;
  descricao: string;
  preco: string;
  total_vendas: number;
  media_avaliacoes: string;
  criado_por?: number;
  criado_por_nome?: string;
  criacao?: string;
}