from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def enviar_email_boas_vindas(email):
    send_mail(
        subject='Bem-vindo!',
        message='Seu cadastro foi realizado com sucesso.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Email enviado"


@shared_task
def enviar_email_compra(email, curso):
    send_mail(
        subject='Compra realizada',
        message=f'Sua compra do curso {curso} foi confirmada.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Compra confirmada"


@shared_task
def processar_reembolso(email, curso):
    send_mail(
        subject='Solicitação de reembolso',
        message=f'O reembolso do curso {curso} foi solicitado.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Reembolso solicitado"


@shared_task
def enviar_email_recuperacao_senha(email):
    send_mail(
        subject='Recuperação de senha',
        message='Clique no link para redefinir sua senha.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Recuperação enviada"


@shared_task
def enviar_email_verificacao(email):
    send_mail(
        subject='Verificação de e-mail',
        message='Confirme seu cadastro através do link enviado.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Verificação enviada"


@shared_task
def enviar_email_compra_recusada(email, curso):
    send_mail(
        subject='Compra recusada',
        message=f'O pagamento do curso {curso} foi recusado.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Compra recusada"


@shared_task
def enviar_email_certificado(email, curso):
    send_mail(
        subject='Certificado liberado',
        message=f'Seu certificado do curso {curso} já está disponível.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Certificado enviado"


@shared_task
def enviar_email_nota_fiscal(email, curso):
    send_mail(
        subject='Nota fiscal disponível',
        message=f'A nota fiscal da compra do curso {curso} está disponível.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Nota fiscal enviada"


@shared_task
def enviar_email_reembolso_aprovado(email, curso):
    send_mail(
        subject='Reembolso aprovado',
        message=f'O reembolso do curso {curso} foi aprovado.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Reembolso aprovado"


@shared_task
def enviar_email_reembolso_recusado(email, curso):
    send_mail(
        subject='Reembolso recusado',
        message=f'O reembolso do curso {curso} foi recusado.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Reembolso recusado"


@shared_task
def enviar_relatorio_diario(email):
    send_mail(
        subject='Relatório diário',
        message='Resumo diário de vendas e movimentações do sistema.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Relatório enviado"