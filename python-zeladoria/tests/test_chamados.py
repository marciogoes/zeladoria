"""
Testes de Chamados
Sprint 14 — Suite de Testes
"""
import pytest


@pytest.fixture
def categoria_e_bairro(client, token_admin):
    """Cria categoria e bairro para usar nos testes de chamado."""
    from tests.conftest import TestingSessionLocal
    from app.models.categoria import Categoria
    from app.models.bairro import Bairro

    db = TestingSessionLocal()
    cat = db.query(Categoria).first()
    if not cat:
        cat = Categoria(nome="Buraco na via", sla_horas=48, cor="#ff0000", icone="road")
        db.add(cat)
        db.commit()
        db.refresh(cat)

    bairro = db.query(Bairro).first()
    if not bairro:
        bairro = Bairro(nome="Nazaré", regiao="Centro")
        db.add(bairro)
        db.commit()
        db.refresh(bairro)

    db.close()
    return cat.id, bairro.id


class TestChamados:
    """Testa CRUD de chamados."""

    def test_listar_chamados_autenticado(self, client, token_cidadao):
        resp = client.get("/api/chamados/", headers=token_cidadao)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_listar_chamados_sem_token(self, client):
        resp = client.get("/api/chamados/")
        assert resp.status_code == 401

    def test_criar_chamado_cidadao(self, client, token_cidadao, categoria_e_bairro):
        cat_id, bairro_id = categoria_e_bairro
        resp = client.post(
            "/api/chamados/",
            headers=token_cidadao,
            data={
                "titulo": "Buraco enorme na rua",
                "descricao": "Buraco de 1 metro na rua principal, risco aos veículos",
                "endereco": "Rua Teste, 123",
                "categoria_id": cat_id,
                "bairro_id": bairro_id,
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert "protocolo" in data
        assert data["protocolo"].startswith("BEL")
        assert data["status"] == "aberto"
        assert data["prioridade"] == "media"

    def test_criar_chamado_titulo_vazio(self, client, token_cidadao, categoria_e_bairro):
        cat_id, _ = categoria_e_bairro
        resp = client.post(
            "/api/chamados/",
            headers=token_cidadao,
            data={
                "titulo": "",
                "descricao": "Sem título",
                "endereco": "Rua X",
                "categoria_id": cat_id,
            },
        )
        assert resp.status_code == 422

    def test_obter_chamado_existente(self, client, token_cidadao, categoria_e_bairro):
        cat_id, _ = categoria_e_bairro
        # Cria
        criar = client.post(
            "/api/chamados/",
            headers=token_cidadao,
            data={
                "titulo": "Teste obter",
                "descricao": "Teste",
                "endereco": "Rua Y",
                "categoria_id": cat_id,
            },
        )
        assert criar.status_code == 201
        chamado_id = criar.json()["id"]

        # Busca
        resp = client.get(f"/api/chamados/{chamado_id}", headers=token_cidadao)
        assert resp.status_code == 200
        assert resp.json()["id"] == chamado_id

    def test_obter_chamado_inexistente(self, client, token_cidadao):
        resp = client.get("/api/chamados/999999", headers=token_cidadao)
        assert resp.status_code == 404

    def test_atualizar_status_gestor(self, client, token_admin, token_cidadao, categoria_e_bairro):
        cat_id, _ = categoria_e_bairro
        criar = client.post(
            "/api/chamados/",
            headers=token_cidadao,
            data={
                "titulo": "Para resolver",
                "descricao": "Será resolvido",
                "endereco": "Rua Z",
                "categoria_id": cat_id,
            },
        )
        chamado_id = criar.json()["id"]

        # Admin atualiza status
        resp = client.patch(
            f"/api/chamados/{chamado_id}/status",
            headers=token_admin,
            json={"status": "em_andamento"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "em_andamento"

    def test_cidadao_nao_pode_atualizar_status(self, client, token_cidadao, categoria_e_bairro):
        cat_id, _ = categoria_e_bairro
        criar = client.post(
            "/api/chamados/",
            headers=token_cidadao,
            data={
                "titulo": "Proibido cidadão mudar status",
                "descricao": "Teste",
                "endereco": "Rua W",
                "categoria_id": cat_id,
            },
        )
        chamado_id = criar.json()["id"]
        resp = client.patch(
            f"/api/chamados/{chamado_id}/status",
            headers=token_cidadao,
            json={"status": "resolvido"},
        )
        assert resp.status_code == 403

    def test_filtro_por_status(self, client, token_admin):
        resp = client.get("/api/chamados/?status=aberto", headers=token_admin)
        assert resp.status_code == 200
        chamados = resp.json()
        assert all(c["status"] == "aberto" for c in chamados)
