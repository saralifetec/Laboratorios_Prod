from . import db
from datetime import datetime
from sqlalchemy import DateTime, Double, Numeric, text
from sqlalchemy.dialects.mysql import TINYINT

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    funcao_id = db.Column(db.Integer, db.ForeignKey('funcoes.id'), nullable=False)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=False)

    funcao = db.relationship('Funcao', backref='users')
    laboratorio = db.relationship('Laboratorio', backref='users')

    def __repr__(self):
        return f"User('{self.username}')"

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    teste_id = db.Column(db.Integer, db.ForeignKey('testes.id'), nullable=False)
    concluido = db.Column(db.DateTime, nullable=True)

    teste = db.relationship('Testes', backref='report', uselist=False)

    def __repr__(self):
        return f"Report(id={self.id}, teste_id={self.teste_id}, concluido={self.concluido})"   

class Componente(db.Model):
    __tablename__ = 'componentes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    componente = db.Column(db.String(100), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return f"Componente(id={self.id}, componente='{self.componente}', obsoleto={self.obsoleto})"

class ConfHorasAuto(db.Model):
    __tablename__ = 'confhorasauto'
    id = db.Column(db.Integer, primary_key=True)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    horasdia = db.Column(db.Float)
    horasgerais = db.Column(db.Integer)
    auto = db.Column(db.Boolean, default=False)
    tipo = db.Column(db.String(50))
    pepnet = db.Column(db.String(50))
    limitar = db.Column(TINYINT(1), nullable=False, default=0, server_default=text('0'))
    # Relações
    laboratorios = db.relationship('ConfHorasAutoLab', backref='confhorasauto', cascade='all, delete-orphan')
    codigosg = db.relationship('ConfHorasAutoCodg', backref='confhorasauto', cascade='all, delete-orphan')

class ConfHorasAutoLab(db.Model):
    __tablename__ = 'confhorasauto_labs'
    id = db.Column(db.Integer, primary_key=True)
    confhorasauto_id = db.Column(db.Integer, db.ForeignKey('confhorasauto.id'), nullable=False)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'), nullable=False)

class ConfHorasAutoCodg(db.Model):
    __tablename__ = 'confhorasauto_codg'
    id = db.Column(db.Integer, primary_key=True)
    confhorasauto_id = db.Column(db.Integer, db.ForeignKey('confhorasauto.id'), nullable=False)
    codigog_id = db.Column(db.Integer, db.ForeignKey('codigosg.id'), nullable=False)

class Referencia(db.Model):
    __tablename__ = 'referencias'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    referencia = db.Column(db.String(50), nullable=False)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=True)
    componente_id = db.Column(db.Integer, db.ForeignKey('componentes.id'), nullable=True)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'), nullable=True)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('solicitantes.id'), nullable=True)
    stockminimo = db.Column(db.Integer, default=0)
    obs = db.Column(db.Text, nullable=True)
    estado = db.Column(db.String(10), nullable=True)
    plme = db.Column(db.Boolean, default=False)
    obsoleto = db.Column(db.Boolean, default=False)
    descricao = db.Column(db.String(100), nullable=True)

    componente = db.relationship('Componente', backref='referencias', lazy=True)
    laboratorio = db.relationship('Laboratorio', backref='referencias', lazy=True)
    solicitante = db.relationship('Solicitante', backref='referencias', lazy=True)
    projeto=db.relationship('Projeto', backref='referencias', lazy=True)

    def __repr__(self):
        return f"Referencia(id={self.id}, referencia='{self.referencia}')"

    
class MovimentoStock(db.Model):
    __tablename__ = 'movimentostock'
    id = db.Column(db.Integer, primary_key=True)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'), nullable=True)
    referencia_id = db.Column(db.Integer, db.ForeignKey('referencias.id'), nullable=False)
    localizacao_id = db.Column(db.Integer, db.ForeignKey('localizacao.id'), nullable=True)
    quantidade = db.Column(db.Float, nullable=False)
    obs = db.Column(db.Text, nullable=True)
    movimento = db.Column(db.String(1), nullable=False)
    exportado = db.Column(db.DateTime, nullable=True)

    ensaio = db.relationship('Ensaio', backref=db.backref('saidas_stock', lazy=True))
    referencia = db.relationship('Referencia', foreign_keys=[referencia_id], backref=db.backref('saidas_stock', lazy=True))
    localizacao = db.relationship('Localizacao', foreign_keys=[localizacao_id], backref=db.backref('entradas_stock', lazy=True))

    def __repr__(self):
        return f"SaidaStock(id={self.id}, ensaio_id={self.ensaio_id}, referencia_id={self.referencia_id}, quantidade={self.quantidade})"

class Tipopeca(db.Model):
    __tablename__ = 'tipopeca'
    id = db.Column(db.Integer, primary_key=True)
    tipopeca = db.Column(db.String(20), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Tipopeca('{self.tipopeca}', '{self.obsoleto}')"

class Componentesae(db.Model):
    __tablename__ = 'componentes_ae'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(2), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Componentesae('{self.codigo}', '{self.nome}', '{self.obsoleto}')"

class Tipovolumeae(db.Model):
    __tablename__ = 'tipovolumeae'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Tipovolumeae('{self.nome}', '{self.obsoleto}')"
    
class Codificacaoae(db.Model):
    __tablename__ = 'codificacaoae'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Codificacaoae('{self.nome}', '{self.obsoleto}')"
    
class Fase(db.Model):
    __tablename__ = 'fases'
    id = db.Column(db.Integer, primary_key=True)
    fase = db.Column(db.String(100), nullable=False)
    sucatearmod = db.Column(db.Integer, nullable=True)
    sucateartrims = db.Column(db.Integer, nullable=True)
    obsoleto = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Fase('{self.fase}', '{self.obsoleto}')"

class ReferenciaAE(db.Model):
    __tablename__ = 'referenciasae'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    referencia = db.Column(db.String(120), nullable=False, unique=True)
    tipo = db.Column(db.String(20), nullable=False, default='projeto')

    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'), nullable=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=True)
    codificacaoae_id = db.Column(db.Integer, db.ForeignKey('codificacaoae.id'), nullable=True)
    tipopeca_id = db.Column(db.Integer, db.ForeignKey('tipopeca.id'), nullable=True)
    componente_id = db.Column(db.Integer, db.ForeignKey('componentes_ae.id'), nullable=False)

    estado_codigo = db.Column(db.String(10), nullable=False, default='00')
    localizacao_atual_id = db.Column(db.Integer, db.ForeignKey('localizacao_ae.id'), nullable=False)

    solicitante_id = db.Column(db.Integer, db.ForeignKey('solicitantes.id'), nullable=True)
    tipovolumeae_id = db.Column(db.Integer, db.ForeignKey('tipovolumeae.id'), nullable=True)

    peso = db.Column(db.Numeric(10, 2), nullable=True)
    dimensoes = db.Column(db.String(100), nullable=True)
    data_limite_armazenamento = db.Column(db.Date, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    obsoleto = db.Column(db.Boolean, nullable=False, default=False)

    laboratorio = db.relationship('Laboratorio', backref='referencias_ae')
    projeto = db.relationship('Projeto', backref='referencias_ae')
    codificacaoae = db.relationship('Codificacaoae', backref='referencias_ae')
    tipopeca = db.relationship('Tipopeca', backref='referencias_ae')
    componenteae = db.relationship('Componentesae', backref='referencias_ae')
    localizacao_atual = db.relationship('Localizacao_ae', backref='referencias_ae')
    solicitante = db.relationship('Solicitante', backref='referencias_ae')
    tipovolumeae = db.relationship('Tipovolumeae', backref='referencias_ae')

class MovimentoAE(db.Model):
    __tablename__ = 'movimentosae'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    referenciaae_id = db.Column(db.Integer, db.ForeignKey('referenciasae.id'), nullable=False)
    localizacao_origem_id = db.Column(db.Integer, db.ForeignKey('localizacao_ae.id'), nullable=False)
    localizacao_destino_id = db.Column(db.Integer, db.ForeignKey('localizacao_ae.id'), nullable=True)
    data_planeada = db.Column(db.DateTime, nullable=True)
    data_confirmacao = db.Column(db.DateTime, nullable=True)
    emailenviado = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.Enum('planeado', 'confirmado', 'cancelado'), nullable=False, default='planeado')
    criado_por = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    confirmado_por = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    pep = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    referenciaae = db.relationship('ReferenciaAE', backref='movimentos')
    localizacao_origem = db.relationship('Localizacao_ae', foreign_keys=[localizacao_origem_id])
    localizacao_destino = db.relationship('Localizacao_ae', foreign_keys=[localizacao_destino_id])
    criado_por_user = db.relationship('User', foreign_keys=[criado_por])
    confirmado_por_user = db.relationship('User', foreign_keys=[confirmado_por])

class Funcao(db.Model):
    __tablename__ = 'funcoes'
    id = db.Column(db.Integer, primary_key=True)
    funcao = db.Column(db.String(20), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Funcao('{self.funcao}', '{self.obsoleto}')"
    
class Normas(db.Model):
    __tablename__ = 'normas'
    id = db.Column(db.Integer, primary_key=True)
    norma = db.Column(db.String(20), nullable=False)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=False)

    laboratorio = db.relationship('Laboratorio', backref='normas')

    def __repr__(self):
        return f"Norma('{self.norma}', '{self.obsoleto}')"

class Normasdocumentos(db.Model):
    __tablename__ = 'normasdocumentos'
    id = db.Column(db.Integer, primary_key=True)
    norma_id = db.Column(db.Integer, db.ForeignKey('normas.id'), nullable=False)
    documento = db.Column(db.String(255), nullable=False) 

    norma = db.relationship('Normas', backref='normasdocumentos')

    def __repr__(self):
        return f"Normasdocumentos(id={self.id}, norma_id={self.norma_id}, documento={self.documento})"

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Cliente('{self.cliente}', '{self.obsoleto}')"


class Projeto(db.Model):
    __tablename__ = 'projetos'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(20), nullable=False)
    tipopeca_id = db.Column(db.Integer, db.ForeignKey('tipopeca.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=False)  
    torque = db.Column(db.String(50), nullable=True)
    testfixture = db.Column(db.String(100), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('codigo', 'descricao', 'tipopeca_id', 'cliente_id', name='uq_projeto_campos'),
    )
  
    tipopeca = db.relationship('Tipopeca', backref='projetos')
    cliente = db.relationship('Cliente', backref='projetos')

    def __repr__(self):
        return f"Projeto('{self.codigo}', '{self.descricao}', '{self.obsoleto}')"

    
class Solicitante(db.Model):
    __tablename__ = 'solicitantes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=True)
    obsoleto = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Solicitante('{self.nome}', '{self.email}', '{self.obsoleto}')"
    
class Codigosg(db.Model):
    __tablename__ = 'codigosg'
    id = db.Column(db.Integer, primary_key=True)
    codigog = db.Column(db.String(50), nullable=False, unique=True)
    descricao = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=True)
    obsoleto = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Codigog('{self.codigog}', '{self.descricao}', '{self.ano}', '{self.obsoleto}')"
    
class DadosGerais(db.Model):
    __tablename__ = 'dadosgerais'
    id = db.Column(db.Integer, primary_key=True)
    custohorapessoa = db.Column(Numeric(10, 2, asdecimal=False), nullable=True)

    def __repr__(self):
        return f"DadosGerais('{self.custohorapessoa}')"

class Tipotestes(db.Model):
    __tablename__ = 'tipotestes'
    id = db.Column(db.Integer, primary_key=True)
    teste = db.Column(db.String(50), nullable=False, unique=True)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'), nullable=False)
    criarpasta = db.Column(db.Boolean, nullable=False)
    mediveis = db.Column(db.Boolean, nullable=True)
    obsoleto = db.Column(db.Boolean, nullable=False)

    laboratorio = db.relationship('Laboratorio', backref='tipotestes')

    def __repr__(self):
        return f"Tipoteste('{self.teste}', '{self.laboratorio_id}', '{self.obsoleto}')"

class PedidoHorasExtra(db.Model):
    __tablename__ = 'pedidos_horas_extra'
    id = db.Column(db.Integer, primary_key=True)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teste_id = db.Column(db.Integer, db.ForeignKey('testes.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horas = db.Column(Numeric(10, 2, asdecimal=False), nullable=False)
    justificacao = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='Pendente')
    data_pedido = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    tecnico = db.relationship('User', backref='pedidos_horas_extra')
    teste = db.relationship('Testes', backref='pedidos_horas_extra')


class Templatenormas(db.Model):
    __tablename__ = 'templatenormas'
    id = db.Column(db.Integer, primary_key=True)
    norma_id = db.Column(db.Integer, db.ForeignKey('normas.id'), nullable=False)
    teste_id = db.Column(db.Integer, db.ForeignKey('tipotestes.id'), nullable=False)
    ordem = db.Column(db.Integer, nullable=True)
    duracao = db.Column(db.Float, nullable=True)
    duracaomontagem = db.Column(db.Float, nullable=True)
    tempopp = db.Column(db.Float, nullable=True)
    tempomp = db.Column(db.Float, nullable=True)
    obsoleto = db.Column(db.Boolean, nullable=False, default=False)

    # Relacionamentos
    norma = db.relationship('Normas', backref='templatenormas')
    teste = db.relationship('Tipotestes', backref='templatenormas')

    def __repr__(self):
        return f"Templatenormas(norma_id={self.norma_id}, teste_id={self.teste_id}, ordem={self.ordem})"

class Motivosfalhaensaios(db.Model):
    __tablename__ = 'motivosfalhaensaios'
    id = db.Column(db.Integer, primary_key=True)
    motivo = db.Column(db.String(50), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Motivosfalhaensaios('{self.motivo}', '{self.obsoleto}')"
    
class Motivosatraso(db.Model):
    __tablename__ = 'motivosatraso'
    id = db.Column(db.Integer, primary_key=True)
    motivo = db.Column(db.String(50), nullable=False)
    obsoleto = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Motivosatraso('{self.motivo}', '{self.obsoleto}')"

class Maquina(db.Model):
    __tablename__ = 'maquinas'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    codsaphoras = db.Column(db.Integer, nullable=True)
    codsappecas = db.Column(db.Integer, nullable=True)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'), nullable=True)
    custo = db.Column(db.Float, nullable=True)
    obsoleto = db.Column(db.Boolean, nullable=False, default=False)

    laboratorio = db.relationship('Laboratorio', backref='maquinas')

    def __repr__(self):
        return f"Maquina('{self.codigo}', '{self.nome}')"


class Horas(db.Model):
    __tablename__ = 'horas'
    id = db.Column(db.Integer, primary_key=True)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horas = db.Column(Numeric(10, 2, asdecimal=False), nullable=False)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'), nullable=True)
    codigog_id = db.Column(db.Integer, db.ForeignKey('codigosg.id'), nullable=True)
    teste_id = db.Column(db.Integer, db.ForeignKey('testes.id'), nullable=True)
    obs = db.Column(db.String(100), nullable=True)
    extra = db.Column(db.Boolean, nullable=False, default=False)
    auto = db.Column(db.Boolean, nullable=True, default=False)
    tipo = db.Column(db.String(3), nullable=True)
    manual = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    exportado = db.Column(db.Date, nullable=True)
    execucao_id = db.Column(db.Integer, db.ForeignKey('horas_auto_execucoes.id'), nullable=True)


    # Relacionamentos
    tecnico = db.relationship('User', backref='horas')
    ensaio = db.relationship('Ensaio', backref='horas', foreign_keys=[ensaio_id])
    codigog = db.relationship('Codigosg', backref='horas', foreign_keys=[codigog_id])
    teste = db.relationship('Testes', backref='horas', foreign_keys=[teste_id])
    execucao = db.relationship('HorasAutoExecucao', backref='horas')

    def __repr__(self):
        return f"Horas(id={self.id}, tecnico_id={self.tecnico_id}, data={self.data}, horas={self.horas})"

class Ensaio(db.Model):
    __tablename__ = 'ensaios'
    id = db.Column(db.Integer, primary_key=True)
    ensaio = db.Column(db.String(20), nullable=False, unique=True)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'), nullable=False)
    norma_id = db.Column(db.Integer, db.ForeignKey('normas.id'), nullable=True)
    npecasrecebidas = db.Column(db.Integer, nullable=True)
    destinopecas = db.Column(db.String(50), nullable=True)
    destinodevol = db.Column(db.String(200), nullable=True)
    moradadevol = db.Column(db.String(400), nullable=True)
    pep = db.Column(db.String(50), nullable=True)
    network = db.Column(db.String(20), nullable=True)
    partnzf = db.Column(db.Text, nullable=True)
    partncliente = db.Column(db.Text, nullable=True)
    corecustomer = db.Column(db.String(50), nullable=False, default='Customer', server_default=text("'Customer'"))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=True)
    tipopeca_id = db.Column(db.Integer, db.ForeignKey('tipopeca.id'), nullable=True)
    fase_id = db.Column(db.Integer, db.ForeignKey('fases.id'), nullable=True)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('solicitantes.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    prefixo = db.Column(db.String(5), nullable=True)
    primeirapeca = db.Column(db.Integer, nullable=True)
    obs = db.Column(db.Text, nullable=True)
    datapedido = db.Column(db.Date, nullable=False)  
    datasolicitada = db.Column(db.Date, nullable=True)  
    dataentregapecas = db.Column(db.Date, nullable=True)  
    dataacordada = db.Column(db.Date, nullable=True)  
    atrasado = db.Column(db.Integer, default=0)
    motivoatraso_id = db.Column(db.Integer, db.ForeignKey('motivosatraso.id'), nullable=True)
    anulado = db.Column(db.Boolean, nullable=False, default=False)
    motivoanulacao = db.Column(db.Text, nullable=True)
    concluido = db.Column(db.Date, nullable=True)  

    # Relacionamentos
    laboratorio = db.relationship('Laboratorio', backref='ensaios')
    norma = db.relationship('Normas', backref='ensaios')
    cliente = db.relationship('Cliente', backref='ensaios')
    projeto = db.relationship('Projeto', backref='ensaios')
    tipopeca = db.relationship('Tipopeca', backref='ensaios')
    fase = db.relationship('Fase', backref='ensaios')
    solicitante = db.relationship('Solicitante', backref='ensaios')
    user = db.relationship('User', backref='ensaios')
    motivoatraso = db.relationship('Motivosatraso', backref='ensaios')
   
    def __repr__(self):
        return f"Ensaio('{self.ensaio}', lab={self.laboratorio_id}, anulado={self.anulado})"


class Testes(db.Model):
    __tablename__ = 'testes'
    id = db.Column(db.Integer, primary_key=True)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'), nullable=False) 
    teste_id = db.Column(db.Integer, db.ForeignKey('tipotestes.id'), nullable=False)
    ordem = db.Column(db.Integer, nullable=True)
    qtd = db.Column(db.Integer, nullable=True)
    prefixo = db.Column(db.String(5), nullable=True)
    primeirapeca = db.Column(db.Integer, nullable=True)
    datainicio = db.Column(db.DateTime, nullable=True)
    duracao = db.Column(db.Float, nullable=True)
    datafim = db.Column(db.DateTime, nullable=True)
    horasmaqexp = db.Column(db.DateTime, nullable=True)
    maquina_id = db.Column(db.Integer, db.ForeignKey('maquinas.id'), nullable=True)
    obs = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    fator = db.Column(db.Integer, nullable=False, default=1)
    bemprimeira = db.Column(db.Integer, nullable=True)
    motivofalhaensaio_id = db.Column(db.Integer, db.ForeignKey('motivosfalhaensaios.id'), nullable=False)
    horasesgotadas = db.Column(db.Integer, default=0)
    esgotadomanualmente = db.Column(db.Integer, nullable=False, default=0)

    # Relacionamentos
    ensaio = db.relationship('Ensaio', backref='testes')  
    teste = db.relationship('Tipotestes', backref='testes')
    maquina = db.relationship('Maquina', backref='testes')
    user = db.relationship('User', backref='testes_realizados')

    def __repr__(self):
        return f"Testes(ensaio_id={self.ensaio_id}, teste_id={self.teste_id}, ordem={self.ordem})"  

    def to_dict(self):
        def iso(dt):
            if not dt:
                return None
            if hasattr(dt, "isoformat"):
                return dt.isoformat()
            return str(dt)
        return {
            'id': self.id,
            'ensaio_id': self.ensaio_id,
            'teste_id': self.teste_id,
            'ordem': self.ordem,
            'qtd': self.qtd,
            'prefixo': self.prefixo,
            'primeirapeca': self.primeirapeca,
            'datainicio': iso(self.datainicio),
            'duracao': self.duracao,
            'datafim': iso(self.datafim),
            'horasmaqexp': iso(self.horasmaqexp),
            'maquina_id': self.maquina_id,
            'obs': self.obs,
            'user_id': self.user_id,
            'fator': self.fator,
            'bemprimeira': self.bemprimeira,
            'motivofalhaensaio_id': self.motivofalhaensaio_id,
            'teste_nome': self.teste.teste if self.teste else None,
            'maquina_nome': self.maquina.nome if self.maquina else None,
            'user_nome': self.user.full_name if self.user else None
        }

class Laboratorio(db.Model):
    __tablename__ = 'laboratorios'
    id = db.Column(db.Integer, primary_key=True)
    laboratorio = db.Column(db.String(50), nullable=False)
    elmact = db.Column(db.Integer, nullable=True) 
    act = db.Column(db.Integer, nullable=True)  
    pastatestes = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    obsoleto = db.Column(db.Boolean, nullable=False, default=False)  #

    def __repr__(self):
        return f"Laboratorio('{self.laboratorio}', '{self.obsoleto}')"

class ConfEmailAuto(db.Model):
    __tablename__ = 'confemailauto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    evento = db.Column(db.String(50), nullable=False)
    assunto = db.Column(db.Text, nullable=False)
    texto = db.Column(db.Text, nullable=False)
    laboratorio_id = db.Column(db.Integer, nullable=False)  
    to_email = db.Column(db.Text, nullable=False)
    cc_email = db.Column(db.Text, nullable=True)  
    obsoleto = db.Column(db.Boolean, nullable=False, default=False)

    laboratorios = db.relationship(
        'ConfEmailAutoLab',
        backref='confemailauto',
        cascade='all, delete-orphan'
    )

class ConfEmailAutoLab(db.Model):
    __tablename__ = 'confemailauto_labs'
    id = db.Column(db.Integer, primary_key=True)
    confemailauto_id = db.Column(db.Integer, db.ForeignKey('confemailauto.id'), nullable=False)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'), nullable=False)

class Aviso(db.Model):
    __tablename__ = 'avisos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    aviso = db.Column(db.Text, nullable=False)
    descartar = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship('User', backref='avisos')

    def __repr__(self):
        return f"Aviso(id={self.id}, user_id={self.user_id}, descartar={self.descartar})"
    

class Localizacao(db.Model):
    __tablename__ = 'localizacao'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    morada = db.Column(db.String(50), nullable=True)
    morada2 = db.Column(db.String(50), nullable=True)
    interno = db.Column(db.Boolean, nullable=False, server_default=text('1'))
    contactonome = db.Column(db.String(50), nullable=True)
    contactoemail = db.Column(db.String(50), nullable=True)
    contactotlf = db.Column(db.String(20), nullable=True)
    obsoleto = db.Column(db.Boolean, nullable=False, server_default=text('0'))

    def __repr__(self):
        return (f"Localizacao(id={self.id}, nome={self.nome}, interno={self.interno}, "
                f"obsoleto={self.obsoleto})")

class Localizacao_ae(db.Model):
    __tablename__ = 'localizacao_ae'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    morada = db.Column(db.String(50), nullable=True)
    morada2 = db.Column(db.String(50), nullable=True)
    interno = db.Column(db.Boolean, nullable=False, server_default=text('1'))
    contactonome = db.Column(db.String(50), nullable=True)
    contactoemail = db.Column(db.String(50), nullable=True)
    contactotlf = db.Column(db.String(20), nullable=True)
    obsoleto = db.Column(db.Boolean, nullable=False, server_default=text('0'))

    def __repr__(self):
        return (f"Localizacao_ae(id={self.id}, nome={self.nome}, interno={self.interno}, "
                f"obsoleto={self.obsoleto})")
    
class ConfValidacaoManual(db.Model):
    __tablename__ = 'confvalidacaomanual'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    regex = db.Column(db.Text, nullable=False)
    chave_i18n = db.Column(db.String(100), nullable=True)
    obsoleto = db.Column(db.SmallInteger, nullable=False, default=0)

class UserCalendar(db.Model):
    __tablename__ = 'user_calendar'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)

    tipo = db.Column(db.String(20), nullable=False)
    # valores:
    # normal, ferias, falta, parcial, trabalhou

    horas = db.Column(db.Float, nullable=True)

    descricao = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    # impedir duplicados
    __table_args__ = (
        db.UniqueConstraint('user_id', 'data', name='unique_user_day'),
    )

class Feriado(db.Model):
    __tablename__ = 'feriados'

    id = db.Column(db.Integer, primary_key=True)

    data = db.Column(db.Date, nullable=False, unique=True)
    descricao = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class ConsultaLayout(db.Model):
    __tablename__ = 'consultas_layout'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Ex.: 'ensaios', 'horas', 'testes', ...
    tabela_principal = db.Column(db.String(50), nullable=False)

    # JSON serializado com joins, campos, agregacoes, filtros, calculados, ordenacao
    definicao_json = db.Column(db.Text, nullable=False)

    # private | all | role_tecnicos | role_coordenadores | selected_users
    visibilidade = db.Column(db.String(30), nullable=False, default='private')

    obsoleto = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    owner = db.relationship('User', backref='consultas_layout')

    def __repr__(self):
        return f"ConsultaLayout(id={self.id}, nome='{self.nome}', owner_id={self.owner_id})"


class ConsultaLayoutUser(db.Model):
    __tablename__ = 'consultas_layout_users'

    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas_layout.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    consulta = db.relationship(
        'ConsultaLayout',
        backref=db.backref('utilizadores_especificos', cascade='all, delete-orphan')
    )
    user = db.relationship('User', backref='consultas_layout_permitidas')

    __table_args__ = (
        db.UniqueConstraint('consulta_id', 'user_id', name='uq_consulta_layout_user'),
    )

    def __repr__(self):
        return f"ConsultaLayoutUser(consulta_id={self.consulta_id}, user_id={self.user_id})"
    
class HorasAuto(db.Model):
    __tablename__ = 'horas_auto'

    id = db.Column(db.Integer, primary_key=True)

    ativo = db.Column(db.Boolean, default=False)

    frequencia = db.Column(db.String(20), default="semanal")
    repeticao = db.Column(db.Integer)  # dia da semana (2=segunda...)

    dia_inicio = db.Column(db.Date)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

class HorasAutoExecucao(db.Model):
    __tablename__ = 'horas_auto_execucoes'

    id = db.Column(db.Integer, primary_key=True)
    data_execucao = db.Column(db.Date, nullable=False)
    data_inicio = db.Column(db.Date, nullable=True)
    data_fim = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='horasautoexecucoes')

class ConfGeral(db.Model):
    __tablename__ = 'conf_geral'

    id = db.Column(db.Integer, primary_key=True)
    pais = db.Column(db.String(50), nullable=False)
    localizacao = db.Column(db.String(50), nullable=False)

    @staticmethod
    def get_conf_geral():
        return ConfGeral.query.first()

