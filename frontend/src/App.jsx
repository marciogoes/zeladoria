import React, { useState, useEffect } from 'react';
import { Search, Filter, Clock, AlertCircle, CheckCircle, XCircle, ChevronDown, Star, Calendar, DollarSign, FileText, X, Edit, Save } from 'lucide-react';

// Usa a variável de ambiente em produção, cai para localhost em dev
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001';

// Componente Principal
export default function CatalogoServicos() {
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('catalogo');
  const [servicos, setServicos] = useState([]);
  const [chamados, setChamados] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // Estados de Filtros
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategoria, setFilterCategoria] = useState('');
  const [filterPrioridade, setFilterPrioridade] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [onlyGratuitos, setOnlyGratuitos] = useState(false);
  const [onlyOnline, setOnlyOnline] = useState(false);
  
  // Estados de Modais
  const [selectedServico, setSelectedServico] = useState(null);
  const [reclassifyModal, setReclassifyModal] = useState(false);
  const [selectedChamado, setSelectedChamado] = useState(null);
  
  // Dashboard Stats
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    // Simular autenticação
    const mockUser = {
      id: 1,
      nome: 'João Silva',
      tipo: 'secretaria',
      secretaria_id: 1,
      secretaria: { sigla: 'SEURB', nome: 'Secretaria de Urbanismo' }
    };
    setUser(mockUser);
    loadData(mockUser);
  }, []);

  const loadData = async (currentUser) => {
    setLoading(true);
    try {
      // Carregar serviços da secretaria
      const servRes = await fetch(`${API_BASE}/api/servicos?secretaria_id=${currentUser.secretaria_id}`);
      if (servRes.ok) {
        const data = await servRes.json();
        setServicos(data.servicos || []);
      }

      // Carregar chamados
      const chamadosRes = await fetch(`${API_BASE}/api/chamados`);
      if (chamadosRes.ok) {
        const data = await chamadosRes.json();
        setChamados(data.chamados || []);
      }

      // Carregar dashboard
      const dashRes = await fetch(`${API_BASE}/api/servicos/dashboard?secretaria_id=${currentUser.secretaria_id}`);
      if (dashRes.ok) {
        const data = await dashRes.json();
        setDashboardData(data);
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  // Filtrar serviços
  const filteredServicos = servicos.filter(s => {
    if (searchTerm && !s.nome.toLowerCase().includes(searchTerm.toLowerCase()) && 
        !s.codigo.toLowerCase().includes(searchTerm.toLowerCase())) return false;
    if (filterCategoria && s.categoria !== filterCategoria) return false;
    if (filterPrioridade && s.prioridade !== filterPrioridade) return false;
    if (filterStatus && s.status !== filterStatus) return false;
    if (onlyGratuitos && s.custo > 0) return false;
    if (onlyOnline && !s.atendimento_online) return false;
    return true;
  });

  // Calcular SLA do chamado
  const calcularSLA = (chamado) => {
    if (!chamado.prazo_sla) return { status: 'sem-prazo', label: 'Sem prazo', color: 'gray' };
    
    const prazo = new Date(chamado.prazo_sla);
    const agora = new Date();
    const diff = prazo - agora;
    const horas = diff / (1000 * 60 * 60);
    
    if (horas < 0) return { status: 'vencido', label: 'Vencido', color: 'red', horas: Math.abs(horas) };
    if (horas < 24) return { status: 'critico', label: 'Crítico', color: 'orange', horas };
    return { status: 'normal', label: 'No prazo', color: 'green', horas };
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold">🏛️ Zeladoria Belém</h1>
              {user && (
                <p className="text-sm opacity-90">
                  {user.secretaria.sigla} - {user.nome}
                </p>
              )}
            </div>
            <button className="px-4 py-2 bg-white/20 rounded-lg hover:bg-white/30 transition">
              Sair
            </button>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex space-x-1">
            {['catalogo', 'chamados', 'dashboard'].map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-3 font-medium transition ${
                  activeTab === tab
                    ? 'border-b-2 border-blue-600 text-blue-600'
                    : 'text-gray-600 hover:text-blue-600'
                }`}
              >
                {tab === 'catalogo' && '📋 Catálogo de Serviços'}
                {tab === 'chamados' && '📞 Chamados'}
                {tab === 'dashboard' && '📊 Dashboard'}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {activeTab === 'catalogo' && (
          <CatalogoTab
            servicos={filteredServicos}
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
            filterCategoria={filterCategoria}
            setFilterCategoria={setFilterCategoria}
            filterPrioridade={filterPrioridade}
            setFilterPrioridade={setFilterPrioridade}
            filterStatus={filterStatus}
            setFilterStatus={setFilterStatus}
            onlyGratuitos={onlyGratuitos}
            setOnlyGratuitos={setOnlyGratuitos}
            onlyOnline={onlyOnline}
            setOnlyOnline={setOnlyOnline}
            onSelectServico={setSelectedServico}
            loading={loading}
          />
        )}

        {activeTab === 'chamados' && (
          <ChamadosTab
            chamados={chamados}
            onReclassify={(chamado) => {
              setSelectedChamado(chamado);
              setReclassifyModal(true);
            }}
            calcularSLA={calcularSLA}
          />
        )}

        {activeTab === 'dashboard' && (
          <DashboardTab data={dashboardData} />
        )}
      </main>

      {/* Modal Detalhes do Serviço */}
      {selectedServico && (
        <ServicoModal
          servico={selectedServico}
          onClose={() => setSelectedServico(null)}
        />
      )}

      {/* Modal Reclassificar Chamado */}
      {reclassifyModal && selectedChamado && (
        <ReclassifyModal
          chamado={selectedChamado}
          servicos={servicos}
          onClose={() => {
            setReclassifyModal(false);
            setSelectedChamado(null);
          }}
          onSave={(novoServico) => {
            console.log('Reclassificando para:', novoServico);
            setReclassifyModal(false);
            setSelectedChamado(null);
          }}
        />
      )}
    </div>
  );
}

// Tab Catálogo
function CatalogoTab({ 
  servicos, 
  searchTerm, 
  setSearchTerm,
  filterCategoria,
  setFilterCategoria,
  filterPrioridade,
  setFilterPrioridade,
  filterStatus,
  setFilterStatus,
  onlyGratuitos,
  setOnlyGratuitos,
  onlyOnline,
  setOnlyOnline,
  onSelectServico,
  loading
}) {
  const categorias = [...new Set(servicos.map(s => s.categoria))];
  
  return (
    <div className="space-y-6">
      {/* Filtros */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Filter size={20} />
          Filtros
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="relative">
            <Search className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Buscar serviço..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>
          
          <select
            value={filterCategoria}
            onChange={(e) => setFilterCategoria(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
          >
            <option value="">Todas as categorias</option>
            {categorias.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
          
          <select
            value={filterPrioridade}
            onChange={(e) => setFilterPrioridade(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
          >
            <option value="">Todas as prioridades</option>
            <option value="emergencial">🚨 Emergencial</option>
            <option value="alta">🔴 Alta</option>
            <option value="media">🟡 Média</option>
            <option value="baixa">🟢 Baixa</option>
            <option value="agendavel">📅 Agendável</option>
          </select>
        </div>
        
        <div className="flex flex-wrap gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={onlyGratuitos}
              onChange={(e) => setOnlyGratuitos(e.target.checked)}
              className="w-4 h-4 text-blue-600"
            />
            <span className="text-sm">Apenas gratuitos</span>
          </label>
          
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={onlyOnline}
              onChange={(e) => setOnlyOnline(e.target.checked)}
              className="w-4 h-4 text-blue-600"
            />
            <span className="text-sm">Atendimento online</span>
          </label>
        </div>
      </div>

      {/* Lista de Serviços */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold mb-4">
          Serviços ({servicos.length})
        </h2>
        
        {loading ? (
          <div className="text-center py-8 text-gray-500">Carregando...</div>
        ) : servicos.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            Nenhum serviço encontrado
          </div>
        ) : (
          <div className="space-y-3">
            {servicos.map(servico => (
              <ServicoCard
                key={servico.id}
                servico={servico}
                onClick={() => onSelectServico(servico)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// Card de Serviço
function ServicoCard({ servico, onClick }) {
  const getPrioridadeColor = (prioridade) => {
    const colors = {
      emergencial: 'bg-red-100 text-red-800',
      alta: 'bg-orange-100 text-orange-800',
      media: 'bg-yellow-100 text-yellow-800',
      baixa: 'bg-green-100 text-green-800',
      agendavel: 'bg-blue-100 text-blue-800'
    };
    return colors[prioridade] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div
      onClick={onClick}
      className="border rounded-lg p-4 hover:shadow-md transition cursor-pointer"
    >
      <div className="flex justify-between items-start mb-2">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-mono text-gray-500">{servico.codigo}</span>
            <span className={`text-xs px-2 py-1 rounded-full ${getPrioridadeColor(servico.prioridade)}`}>
              {servico.prioridade}
            </span>
          </div>
          <h3 className="font-semibold text-lg">{servico.nome}</h3>
          <p className="text-sm text-gray-600 mt-1">{servico.descricao}</p>
        </div>
      </div>
      
      <div className="flex flex-wrap gap-4 text-sm text-gray-600 mt-3">
        <div className="flex items-center gap-1">
          <Clock size={16} />
          <span>SLA: {servico.sla_horas}h</span>
        </div>
        <div className="flex items-center gap-1">
          <DollarSign size={16} />
          <span>{servico.custo === 0 ? 'Gratuito' : `R$ ${servico.custo.toFixed(2)}`}</span>
        </div>
        <div className="flex items-center gap-1">
          <FileText size={16} />
          <span>{servico.categoria}</span>
        </div>
        {servico.avaliacao_media > 0 && (
          <div className="flex items-center gap-1">
            <Star size={16} className="fill-yellow-400 text-yellow-400" />
            <span>{servico.avaliacao_media.toFixed(1)}</span>
          </div>
        )}
      </div>
    </div>
  );
}

// Tab Chamados
function ChamadosTab({ chamados, onReclassify, calcularSLA }) {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold mb-4">
          Chamados com SLA ({chamados.length})
        </h2>
        
        {chamados.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            Nenhum chamado encontrado
          </div>
        ) : (
          <div className="space-y-3">
            {chamados.map(chamado => {
              const sla = calcularSLA(chamado);
              return (
                <ChamadoCard
                  key={chamado.id}
                  chamado={chamado}
                  sla={sla}
                  onReclassify={() => onReclassify(chamado)}
                />
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

// Card de Chamado
function ChamadoCard({ chamado, sla, onReclassify }) {
  const getStatusColor = (status) => {
    const colors = {
      aberto: 'bg-blue-100 text-blue-800',
      em_andamento: 'bg-yellow-100 text-yellow-800',
      resolvido: 'bg-green-100 text-green-800',
      cancelado: 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getSLAIcon = (status) => {
    if (status === 'vencido') return <XCircle className="text-red-500" />;
    if (status === 'critico') return <AlertCircle className="text-orange-500" />;
    return <CheckCircle className="text-green-500" />;
  };

  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition">
      <div className="flex justify-between items-start mb-2">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-mono text-gray-500">{chamado.protocolo}</span>
            <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(chamado.status)}`}>
              {chamado.status.replace('_', ' ')}
            </span>
          </div>
          <h3 className="font-semibold text-lg">{chamado.titulo}</h3>
          <p className="text-sm text-gray-600 mt-1">{chamado.descricao}</p>
        </div>
        <button
          onClick={onReclassify}
          className="ml-4 px-3 py-1.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm flex items-center gap-1"
        >
          <Edit size={14} />
          Reclassificar
        </button>
      </div>
      
      <div className="flex items-center gap-2 mt-3 p-3 bg-gray-50 rounded-lg">
        {getSLAIcon(sla.status)}
        <div className="flex-1">
          <div className="text-sm font-medium">SLA: {sla.label}</div>
          {sla.horas && (
            <div className="text-xs text-gray-600">
              {sla.status === 'vencido'
                ? `Vencido há ${sla.horas.toFixed(0)}h`
                : `${sla.horas.toFixed(0)}h restantes`}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Tab Dashboard
function DashboardTab({ data }) {
  if (!data) {
    return (
      <div className="text-center py-8 text-gray-500">
        Carregando dashboard...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard title="Total de Serviços" value={data.total_servicos} icon="📋" color="blue" />
        <KPICard title="Serviços Ativos" value={data.servicos_ativos} icon="✅" color="green" />
        <KPICard title="Categorias" value={data.total_categorias} icon="📁" color="purple" />
        <KPICard title="Taxa SLA" value={`${data.taxa_cumprimento_sla_geral.toFixed(0)}%`} icon="⏱️" color="orange" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="font-semibold mb-4">Distribuição por Prioridade</h3>
          <div className="space-y-2">
            {Object.entries(data.por_prioridade).map(([prioridade, total]) => (
              <div key={prioridade} className="flex items-center gap-2">
                <div className="w-24 text-sm capitalize">{prioridade}</div>
                <div className="flex-1 bg-gray-200 rounded-full h-6">
                  <div
                    className="bg-blue-600 h-6 rounded-full flex items-center justify-end pr-2 text-xs text-white font-medium"
                    style={{ width: `${(total / data.total_servicos * 100)}%` }}
                  >
                    {total}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="font-semibold mb-4">Categorias Mais Solicitadas</h3>
          <div className="space-y-3">
            {data.categorias_mais_solicitadas.slice(0, 5).map((item, idx) => (
              <div key={idx} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                <span className="text-sm">{item.categoria}</span>
                <span className="font-semibold text-blue-600">{item.total}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function KPICard({ title, value, icon, color }) {
  const colorClasses = {
    blue: 'border-blue-500 text-blue-600',
    green: 'border-green-500 text-green-600',
    purple: 'border-purple-500 text-purple-600',
    orange: 'border-orange-500 text-orange-600'
  };

  return (
    <div className={`bg-white rounded-lg shadow-sm p-6 border-l-4 ${colorClasses[color]}`}>
      <div className="text-3xl mb-2">{icon}</div>
      <div className="text-sm text-gray-600 mb-1">{title}</div>
      <div className="text-2xl font-bold">{value}</div>
    </div>
  );
}

function ServicoModal({ servico, onClose }) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center">
          <h2 className="text-xl font-bold">{servico.nome}</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-lg transition">
            <X size={20} />
          </button>
        </div>
        <div className="p-6 space-y-4">
          <div><label className="text-sm font-semibold text-gray-600">Código</label><p className="font-mono">{servico.codigo}</p></div>
          <div><label className="text-sm font-semibold text-gray-600">Descrição</label><p>{servico.descricao}</p></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="text-sm font-semibold text-gray-600">Categoria</label><p>{servico.categoria}</p></div>
            <div><label className="text-sm font-semibold text-gray-600">Prioridade</label><p className="capitalize">{servico.prioridade}</p></div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="text-sm font-semibold text-gray-600">SLA</label><p>{servico.sla_horas}h</p></div>
            <div><label className="text-sm font-semibold text-gray-600">Custo</label><p>{servico.custo === 0 ? 'Gratuito' : `R$ ${servico.custo.toFixed(2)}`}</p></div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ReclassifyModal({ chamado, servicos, onClose, onSave }) {
  const [selectedServico, setSelectedServico] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredServicos = servicos.filter(s =>
    s.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.codigo.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center">
          <h2 className="text-xl font-bold">Reclassificar Chamado</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-lg transition"><X size={20} /></button>
        </div>
        <div className="p-6 space-y-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="text-sm text-gray-600">Chamado atual</div>
            <div className="font-semibold">{chamado.protocolo}</div>
            <div className="text-sm mt-1">{chamado.titulo}</div>
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-600 mb-2">Buscar novo serviço</label>
            <div className="relative">
              <Search className="absolute left-3 top-3 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Digite o nome ou código do serviço..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
          </div>
          <div className="max-h-96 overflow-y-auto space-y-2">
            {filteredServicos.map(servico => (
              <div
                key={servico.id}
                onClick={() => setSelectedServico(servico)}
                className={`border rounded-lg p-3 cursor-pointer transition ${selectedServico?.id === servico.id ? 'border-blue-500 bg-blue-50' : 'hover:border-blue-300'}`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <div className="text-xs font-mono text-gray-500">{servico.codigo}</div>
                    <div className="font-semibold">{servico.nome}</div>
                    <div className="text-sm text-gray-600 mt-1">SLA: {servico.sla_horas}h | {servico.categoria}</div>
                  </div>
                  {selectedServico?.id === servico.id && <CheckCircle className="text-blue-600" />}
                </div>
              </div>
            ))}
          </div>
          <div className="flex gap-3 pt-4 border-t">
            <button onClick={onClose} className="flex-1 px-4 py-2 border rounded-lg hover:bg-gray-50 transition">Cancelar</button>
            <button
              onClick={() => selectedServico && onSave(selectedServico)}
              disabled={!selectedServico}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <Save size={16} />
              Salvar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
