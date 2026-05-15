from software_sales.courses.models import Curso


def listar_cursos():
    return Curso.objects.select_related(
        "criado_por"
    ).prefetch_related(
        "avaliacoes",
        "compras",
    )


def listar_curso_por_id(curso_id):
    return Curso.objects.select_related(
        "criado_por"
    ).filter(id=curso_id).first()