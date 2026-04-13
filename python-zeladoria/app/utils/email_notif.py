"""
Sprint 18 — Notificações por E-mail
Envia e-mail ao cidadão quando o status do chamado muda.
Requer: EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD no .env
Em desenvolvimento (sem variáveis configuradas): loga o e-mail sem enviar.
"""
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

logger = logging.getLogger("zelo.email")

# Configuração via variáveis de ambiente
# Aceita SMTP_* (padrão .env) e EMAIL_* (legado) — prioridade: SMTP_*
EMAIL_HOST     = os.environ.get("SMTP_HOST") or os.environ.get("EMAIL_HOST", "")
EMAIL_PORT     = int(os.environ.get("SMTP_PORT") or os.environ.get("EMAIL_PORT", "587"))
EMAIL_USER     = os.environ.get("SMTP_USER") or os.environ.get("EMAIL_USER", "")
EMAIL_PASSWORD = os.environ.get("SMTP_PASSWORD") or os.environ.get("EMAIL_PASSWORD", "")
EMAIL_FROM     = os.environ.get("EMAIL_FROM", EMAIL_USER or "noreply@belem.pa.gov.br")
EMAIL_FROM_NAME = os.environ.get("EMAIL_FROM_NAME", "Zelô — Zeladoria Urbana de Belém")

_CONFIGURADO = bool(EMAIL_HOST and EMAIL_USER and EMAIL_PASSWORD)


# ── Templates de e-mail ──────────────────────────────────────────────────────

_STATUS_LABELS = {
    "aberto":        "🔵 Aberto",
    "em_andamento":  "🟡 Em Andamento",
    "resolvido":     "✅ Resolvido",
    "cancelado":     "🔴 Cancelado",
}

_TEMPLATE_STATUS = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 20px; }}
    .card {{ background: #fff; border-radius: 12px; max-width: 520px; margin: 0 auto; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,.08); }}
    .header {{ background: linear-gradient(135deg, #0099aa, #2563eb); padding: 28px 32px; }}
    .header h1 {{ color: #fff; margin: 0; font-size: 1.3rem; letter-spacing: -.02em; }}
    .header p {{ color: rgba(255,255,255,.8); margin: 4px 0 0; font-size: .88rem; }}
    .body {{ padding: 28px 32px; }}
    .status-badge {{ display: inline-block; padding: 5px 14px; border-radius: 20px;
                     background: {badge_bg}; color: {badge_color}; font-weight: 600; font-size: .85rem; }}
    .info-row {{ display: flex; justify-content: space-between; padding: 10px 0;
                 border-bottom: 1px solid #f0f4f8; font-size: .88rem; }}
    .info-row span:first-child {{ color: #94a3b8; }}
    .info-row strong {{ color: #0f172a; }}
    .btn {{ display: inline-block; margin-top: 20px; padding: 12px 24px; background: #0099aa;
            color: #fff !important; text-decoration: none; border-radius: 8px;
            font-weight: 700; font-size: .9rem; }}
    .footer {{ background: #f8fafc; padding: 16px 32px; font-size: .78rem; color: #94a3b8; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1>🏛️ Zelô — Zeladoria Urbana de Belém</h1>
      <p>Atualização do seu chamado</p>
    </div>
    <div class="body">
      <p style="color:#475569;margin-top:0;">Olá, <strong>{nome}</strong>!</p>
      <p style="color:#475569;">Seu chamado <strong>{protocolo}</strong> teve uma atualização de status:</p>

      <div style="background:#f8fafc;border-radius:10px;padding:16px;margin:16px 0;">
        <div style="font-size:.78rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;">Novo Status</div>
        <span class="status-badge">{status_label}</span>
      </div>

      <div class="info-row">
        <span>Chamado</span>
        <strong>{titulo}</strong>
      </div>
      <div class="info-row">
        <span>Protocolo</span>
        <strong>{protocolo}</strong>
      </div>
      <div class="info-row">
        <span>Categoria</span>
        <strong>{categoria}</strong>
      </div>
      {observacao_html}

      <a href="{app_url}" class="btn">Ver meu chamado ›</a>
    </div>
    <div class="footer">
      Prefeitura Municipal de Belém · Zeladoria Urbana<br>
      Este é um e-mail automático, não responda a esta mensagem.
    </div>
  </div>
</body>
</html>
"""

_TEMPLATE_CRIACAO = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 20px; }}
    .card {{ background: #fff; border-radius: 12px; max-width: 520px; margin: 0 auto; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,.08); }}
    .header {{ background: linear-gradient(135deg, #059669, #0099aa); padding: 28px 32px; }}
    .header h1 {{ color: #fff; margin: 0; font-size: 1.3rem; }}
    .header p {{ color: rgba(255,255,255,.8); margin: 4px 0 0; font-size: .88rem; }}
    .body {{ padding: 28px 32px; }}
    .protocolo {{ font-family: monospace; font-size: 1.4rem; font-weight: 700;
                  color: #0099aa; background: #f0f4f8; padding: 10px 16px;
                  border-radius: 8px; display: inline-block; margin: 12px 0; letter-spacing: .05em; }}
    .info-row {{ display: flex; justify-content: space-between; padding: 10px 0;
                 border-bottom: 1px solid #f0f4f8; font-size: .88rem; }}
    .info-row span:first-child {{ color: #94a3b8; }}
    .info-row strong {{ color: #0f172a; }}
    .btn {{ display: inline-block; margin-top: 20px; padding: 12px 24px; background: #0099aa;
            color: #fff !important; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: .9rem; }}
    .footer {{ background: #f8fafc; padding: 16px 32px; font-size: .78rem; color: #94a3b8; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1>✅ Chamado Registrado com Sucesso!</h1>
      <p>Zelô — Zeladoria Urbana de Belém</p>
    </div>
    <div class="body">
      <p style="color:#475569;margin-top:0;">Olá, <strong>{nome}</strong>!</p>
      <p style="color:#475569;">Seu chamado foi registrado. Guarde seu protocolo:</p>
      <div class="protocolo">{protocolo}</div>

      <div class="info-row">
        <span>Título</span>
        <strong>{titulo}</strong>
      </div>
      <div class="info-row">
        <span>Categoria</span>
        <strong>{categoria}</strong>
      </div>
      <div class="info-row">
        <span>Bairro</span>
        <strong>{bairro}</strong>
      </div>
      <div class="info-row">
        <span>Prioridade</span>
        <strong>{prioridade}</strong>
      </div>
      <div class="info-row">
        <span>Prazo SLA</span>
        <strong>{sla}</strong>
      </div>

      <p style="color:#475569;font-size:.88rem;">
        Acompanhe o andamento pelo app. Você receberá um e-mail a cada atualização de status.
      </p>
      <a href="{app_url}" class="btn">Acompanhar chamado ›</a>
    </div>
    <div class="footer">
      Prefeitura Municipal de Belém · Zeladoria Urbana<br>
      Este é um e-mail automático, não responda a esta mensagem.
    </div>
  </div>
</body>
</html>
"""


# ── Funções de envio ─────────────────────────────────────────────────────────

def _enviar(para: str, assunto: str, html: str, texto: str = "") -> bool:
    """Envia e-mail via SMTP. Retorna True se enviado, False se apenas logado."""
    if not _CONFIGURADO:
        logger.info(
            f"[EMAIL SIMULADO] Para: {para} | Assunto: {assunto}\n"
            f"  (Defina EMAIL_HOST, EMAIL_USER e EMAIL_PASSWORD para enviar de verdade)"
        )
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = assunto
    msg["From"]    = f"{EMAIL_FROM_NAME} <{EMAIL_FROM}>"
    msg["To"]      = para

    if texto:
        msg.attach(MIMEText(texto, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, [para], msg.as_string())
        logger.info(f"✅ E-mail enviado: {para} | {assunto}")
        return True
    except Exception as e:
        logger.error(f"❌ Falha ao enviar e-mail para {para}: {e}")
        return False


def notificar_criacao(chamado) -> bool:
    """
    Envia e-mail de confirmação ao cidadão quando um chamado é criado.
    """
    try:
        usuario = chamado.usuario
        if not usuario or not usuario.email:
            return False

        cat  = chamado.categoria.nome if chamado.categoria else "—"
        bairro = chamado.bairro.nome if chamado.bairro else "—"
        sla_h = chamado.categoria.sla_horas if chamado.categoria and chamado.categoria.sla_horas else 72
        sla_str = f"{sla_h}h" if sla_h < 24 else f"{sla_h // 24} dia(s)"
        app_url = os.environ.get("APP_URL", "https://zeladoria-backend-production.up.railway.app/app")

        html = _TEMPLATE_CRIACAO.format(
            nome=usuario.nome,
            protocolo=chamado.protocolo,
            titulo=chamado.titulo,
            categoria=cat,
            bairro=bairro,
            prioridade=chamado.prioridade.capitalize(),
            sla=sla_str,
            app_url=app_url,
        )
        assunto = f"✅ Chamado {chamado.protocolo} registrado — Zelô Belém"
        return _enviar(usuario.email, assunto, html)

    except Exception as e:
        logger.error(f"Erro em notificar_criacao: {e}")
        return False


def notificar_mudanca_status(chamado, status_anterior: str, observacao: str = "") -> bool:
    """
    Envia e-mail ao cidadão quando o status do chamado muda.
    Não envia se o usuário não tiver e-mail ou se o status não mudou.
    """
    try:
        usuario = chamado.usuario
        if not usuario or not usuario.email:
            return False
        if status_anterior == chamado.status:
            return False

        _BADGE = {
            "aberto":        ("#dbeafe", "#1d4ed8"),
            "em_andamento":  ("#fef3c7", "#92400e"),
            "resolvido":     ("#d1fae5", "#065f46"),
            "cancelado":     ("#fee2e2", "#991b1b"),
        }
        badge_bg, badge_color = _BADGE.get(chamado.status, ("#f1f5f9", "#475569"))
        status_label = _STATUS_LABELS.get(chamado.status, chamado.status)
        cat = chamado.categoria.nome if chamado.categoria else "—"
        app_url = os.environ.get("APP_URL", "https://zeladoria-backend-production.up.railway.app/app")

        obs_html = ""
        if observacao:
            obs_html = f'<div class="info-row"><span>Observação</span><strong>{observacao[:200]}</strong></div>'

        html = _TEMPLATE_STATUS.format(
            nome=usuario.nome,
            protocolo=chamado.protocolo,
            titulo=chamado.titulo,
            categoria=cat,
            status_label=status_label,
            badge_bg=badge_bg,
            badge_color=badge_color,
            observacao_html=obs_html,
            app_url=app_url,
        )
        assunto = f"[{status_label}] Chamado {chamado.protocolo} — Zelô Belém"
        return _enviar(usuario.email, assunto, html)

    except Exception as e:
        logger.error(f"Erro em notificar_mudanca_status: {e}")
        return False
