"""
Testes de Autenticação
Sprint 14 — Suite de Testes
"""
import pytest


class TestAuth:
    """Testa endpoints de autenticação."""

    def test_login_admin_valido(self, client, token_admin):
        """Login com credenciais válidas retorna token."""
        resp = client.post("/api/auth/login", json={
            "email": "admin@test.com",
            "senha": "senha123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["usuario"]["tipo"] == "admin"

    def test_login_senha_errada(self, client):
        """Login com senha errada retorna 401."""
        resp = client.post("/api/auth/login", json={
            "email": "admin@test.com",
            "senha": "senha_errada",
        })
        assert resp.status_code == 401

    def test_login_email_inexistente(self, client):
        """Login com email não cadastrado retorna 401."""
        resp = client.post("/api/auth/login", json={
            "email": "naoexiste@test.com",
            "senha": "senha123",
        })
        assert resp.status_code == 401

    def test_me_com_token(self, client, token_admin):
        """Rota /me retorna dados do usuário autenticado."""
        resp = client.get("/api/auth/me", headers=token_admin)
        assert resp.status_code == 200
        assert resp.json()["email"] == "admin@test.com"

    def test_me_sem_token(self, client):
        """Rota /me sem token retorna 401."""
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401

    def test_registro_novo_usuario(self, client):
        """Registro de novo usuário retorna token."""
        resp = client.post("/api/auth/register", json={
            "nome": "Novo Cidadão",
            "email": "novo@test.com",
            "senha": "senha123",
            "tipo": "cidadao",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "access_token" in data

    def test_registro_email_duplicado(self, client):
        """Registro com email existente retorna 400."""
        client.post("/api/auth/register", json={
            "nome": "Duplo",
            "email": "duplo@test.com",
            "senha": "senha123",
            "tipo": "cidadao",
        })
        resp = client.post("/api/auth/register", json={
            "nome": "Duplo 2",
            "email": "duplo@test.com",
            "senha": "senha123",
            "tipo": "cidadao",
        })
        assert resp.status_code == 400
