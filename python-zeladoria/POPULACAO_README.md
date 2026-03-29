# 🎯 GUIA DE POPULAÇÃO DO BANCO DE DADOS

## 📋 O que este script faz?

Este script popula o banco de dados com dados realistas para apresentação:

### 📊 Dados que serão criados:

✅ **8 Usuários de Demonstração:**
- 5 Cidadãos
- 3 Equipes (SEURB, SESAN, SEMMA)

✅ **50 Chamados Variados:**
- Diferentes status (Aberto, Em Andamento, Resolvido, Cancelado)
- Diferentes prioridades (Baixa, Média, Alta, Crítica)
- Datas distribuídas nos últimos 90 dias
- Localizações reais em Belém/PA
- Histórico completo de mudanças

✅ **Comentários Realistas:**
- 60% dos chamados têm comentários
- 1 a 5 comentários por chamado
- Tipos variados (Atualização, Observação, Resolução)
- Alguns visíveis e outros internos

✅ **Avaliações:**
- 70% dos chamados resolvidos têm avaliação
- Notas de 1 a 5 estrelas (distribuição realista)
- 80% com comentários dos cidadãos

---

## 🚀 COMO EXECUTAR

### Opção 1: Arquivo .bat (Mais Fácil)
```bash
# Clique duas vezes no arquivo:
popular_banco.bat
```

### Opção 2: Python direto
```bash
python popular_banco.py
```

---

## ⚙️ PRÉ-REQUISITOS

1. ✅ Banco de dados já criado (tabelas existentes)
2. ✅ Seeds básicos executados (categorias, bairros, secretarias)
3. ✅ Servidor backend rodando ou configurado

---

## 📧 USUÁRIOS PARA LOGIN

Após executar o script, você poderá fazer login com:

### 👤 Cidadãos:
- **Email:** maria.silva@email.com
- **Senha:** demo123

- **Email:** joao.pereira@email.com  
- **Senha:** demo123

### 👷 Equipes:
- **Email:** pedro.santos@seurb.belem.pa.gov.br
- **Senha:** demo123

- **Email:** juliana.costa@sesan.belem.pa.gov.br
- **Senha:** demo123

### 📊 Gestores:
Use os usuários padrão criados no seed:
- **Email:** gestor@zeladoria.com
- **Senha:** gestor123

---

## 📈 ESTATÍSTICAS ESPERADAS

Após a execução, você terá:
- **~50 chamados** distribuídos por status
- **~120 comentários** em vários chamados
- **~15 avaliações** com notas variadas
- **Dados dos últimos 90 dias** para análise temporal

---

## 🎨 IDEAL PARA APRESENTAÇÃO

Este script cria dados perfeitos para demonstrar:
- ✅ Dashboard com gráficos preenchidos
- ✅ Lista de chamados variada
- ✅ Sistema de comentários ativo
- ✅ Avaliações e feedback
- ✅ Histórico de mudanças
- ✅ Múltiplos tipos de usuário

---

## ⚠️ IMPORTANTE

- ❗ Não execute em produção (apenas em desenvolvimento)
- ❗ Os dados são fictícios mas realistas
- ❗ Pode ser executado múltiplas vezes (não duplica usuários)
- ❗ Para limpar: recriar o banco de dados

---

## 🆘 PROBLEMAS?

Se encontrar erros:
1. Verifique se o banco está criado
2. Confirme que os seeds foram executados
3. Verifique a conexão com o banco
4. Veja os logs de erro no console

---

## 📞 CONTATO

Qualquer dúvida, consulte a documentação principal do projeto!

**Boa apresentação! 🚀**
