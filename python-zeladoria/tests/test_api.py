"""
Testes de API Pública e Engajamento
Sprint 14 — Suite de Testes
"""
import pytest


class TestAPIPublica:
    """Testa endpoints públicos — sem autenticação."""

    def test_estatisticas_publicas(self, client):
        resp = client.get("/api/publico/estatisticas")
        assert resp.status_code == 200
        data = resp.json()
        assert "total_chamados" in data
        assert "taxa_resolucao" in data
        assert "top_bairros" in data

    def test_chamados_publicos(self, client):
        resp = client.get("/api/publico/chamados")
        assert resp.status_code == 200
        data = resp.json()
        assert "total" in data
        assert "dados" in data
        assert isinstance(data["dados"], list)

    def test_chamados_publicos_sem_dados_pessoais(self, client):
        """Garante que dados pessoais não são expostos."""
        resp = client.get("/api/publico/chamados")
        assert resp.status_code == 200
        for c in resp.json()["dados"]:
            assert "usuario_id" not in c
            assert "email" not in c
            assert "cpf" not in c
            assert "telefone" not in c

    def test_categorias_publicas(self, client):
        resp = client.get("/api/categorias/")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_bairros_publicos(self, client):
        resp = client.get("/api/bairros/")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


class TestEngajamento:
    """Testa votação e gamificação."""

    def test_perfil_gamificacao(self, client, token_cidadao):
        resp = client.get("/api/engajamento/meu-perfil", headers=token_cidadao)
        assert resp.status_code == 200
        data = resp.json()
        assert "pontos" in data
        assert "nivel" in data
        assert "conquistas" in data

    def test_ranking_cidadaos(self, client):
        resp = client.get("/api/engajamento/ranking")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_ranking_bairros(self, client):
        resp = client.get("/api/engajamento/ranking-bairros")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


class TestHealth:
    """Testa endpoints de saúde."""

    def test_health_basic(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_root(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["version"] == "3.0.0"

    def test_docs_acessiveis(self, client):
        resp = client.get("/docs")
        assert resp.status_code == 200


class TestIA:
    """Testa endpoints de IA."""

    def test_triar_chamado(self, client, token_cidadao):
        resp = client.post(
            "/api/ia/triar",
            headers=token_cidadao,
            json={"titulo": "Buraco na rua", "descricao": "Há um buraco grande no asfalto"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "categoria_sugerida" in data
        assert "prioridade_sugerida" in data
        assert "confianca" in data
        assert 0 <= data["confianca"] <= 1

    def test_triar_categoriza_corretamente(self, client, token_cidadao):
        """Testa que 'buraco' classifica como Buraco na via."""
        resp = client.post(
            "/api/ia/triar",
            headers=token_cidadao,
            json={"titulo": "Enorme buraco no asfalto", "descricao": "Cratera na pavimentação"},
        )
        assert resp.status_code == 200
        assert "Buraco" in resp.json()["categoria_sugerida"]

    def test_triar_dengue(self, client, token_cidadao):
        """Testa que 'dengue' classifica corretamente."""
        resp = client.post(
            "/api/ia/triar",
            headers=token_cidadao,
            json={"titulo": "Foco de dengue", "descricao": "Água parada com mosquito aedes"},
        )
        assert resp.status_code == 200
        assert resp.json()["prioridade_sugerida"] == "critica"

    def test_painel_publico(self, client):
        resp = client.get("/api/ia/painel-publico")
        assert resp.status_code == 200
        data = resp.json()
        assert "hoje" in data
        assert "semana" in data
        assert "mes" in data
