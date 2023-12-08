# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AcessoPessoa(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.DateTimeField(blank=True, null=True)
    ip = models.CharField(max_length=45, blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    post = models.TextField(blank=True, null=True)
    texto_get = models.TextField(blank=True, null=True)
    request = models.TextField(blank=True, null=True)
    nivel_permissao = models.IntegerField(blank=True, null=True)
    cookie = models.TextField(blank=True, null=True)
    pessoas = models.ForeignKey('Pessoas', models.DO_NOTHING)
    ehlogin = models.CharField(db_column='ehLogin', max_length=45, blank=True, null=True)  # Field name made lowercase.
    caminho_arquivo = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'acesso_pessoa'


class Alertas(models.Model):
    id = models.BigAutoField(primary_key=True)
    descricao = models.CharField(max_length=1000)
    pessoas_id_cadastro = models.ForeignKey('Pessoas', models.DO_NOTHING, db_column='pessoas_id_cadastro')
    pessoas_id_destino = models.ForeignKey('Pessoas', models.DO_NOTHING, db_column='pessoas_id_destino', related_name='alertas_pessoas_id_destino_set')
    visualizado = models.CharField(max_length=1, blank=True, null=True)
    data_alerta = models.DateTimeField(blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    concluido = models.CharField(max_length=50, blank=True, null=True)
    dt_concluido = models.DateTimeField(blank=True, null=True)
    dt_prazo = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'alertas'


class Arquivos(models.Model):
    id = models.BigAutoField(primary_key=True)
    nm_arq = models.CharField(max_length=100, blank=True, null=True)
    dt_arq = models.DateTimeField(blank=True, null=True)
    tp_arq = models.CharField(max_length=45, blank=True, null=True)
    contratos = models.ForeignKey('Contratos', models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    dt_envio_banco = models.DateTimeField(blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    dt_processamento = models.DateTimeField(blank=True, null=True)
    origem = models.CharField(max_length=45, blank=True, null=True)
    pessoas_id_envio = models.ForeignKey('Pessoas', models.DO_NOTHING, db_column='pessoas_id_envio', blank=True, null=True)
    boletos_avulso = models.ForeignKey('BoletosAvulso', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'arquivos'



class BoletosAvulso(models.Model):
    id = models.BigAutoField(primary_key=True)
    dt_boleto = models.DateField()
    pessoas = models.ForeignKey('Pessoas', models.DO_NOTHING)
    pessoas_id_inclusao = models.ForeignKey('Pessoas', models.DO_NOTHING, db_column='pessoas_id_inclusao', related_name='boletosavulso_pessoas_id_inclusao_set')
    contratos = models.ForeignKey('Contratos', models.DO_NOTHING, blank=True, null=True)
    descricao = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'boletos_avulso'


class ContratoLote(models.Model):
    id = models.BigAutoField(primary_key=True)
    contratos = models.ForeignKey('Contratos', models.DO_NOTHING)
    lote = models.ForeignKey('Lotes', models.DO_NOTHING)
    vl_lote = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'contrato_lote'


class ContratoParcelas(models.Model):
    id = models.BigAutoField(primary_key=True)
    contratos = models.ForeignKey('Contratos', models.DO_NOTHING, blank=True, null=True)
    nu_parcela = models.IntegerField(blank=True, null=True)
    dt_vencimento = models.DateField(blank=True, null=True)
    dt_pagto = models.DateField(blank=True, null=True)
    vl_parcela = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vl_correcao_monetaria = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vl_juros = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vl_pagto = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vl_juros_pagto = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vl_honorarios = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vl_taxa = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vl_multa = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vl_corrigido = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    liquidada_no_cadastro = models.CharField(max_length=45, blank=True, null=True)
    simulada = models.CharField(max_length=45, blank=True, null=True)
    dt_vencimento_original = models.DateField(blank=True, null=True)
    arquivos_id_remessa = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='arquivos_id_remessa', blank=True, null=True)
    nu_linha_remessa = models.IntegerField(blank=True, null=True)
    arquivos_id_retorno = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='arquivos_id_retorno', related_name='contratoparcelas_arquivos_id_retorno_set', blank=True, null=True)
    nu_linha_retorno = models.CharField(max_length=45, blank=True, null=True)
    dt_credito = models.DateField(blank=True, null=True)
    dt_processo_pagto = models.DateTimeField(blank=True, null=True)
    teds = models.ForeignKey('Teds', models.DO_NOTHING, blank=True, null=True)
    tratar_ted = models.IntegerField(blank=True, null=True)
    pessoas_id_atualizacao = models.ForeignKey('Pessoas', models.DO_NOTHING, db_column='pessoas_id_atualizacao', blank=True, null=True)
    fl_negativada = models.CharField(max_length=45, blank=True, null=True)
    motivo_zerado = models.CharField(max_length=150, blank=True, null=True)
    observacao_zerado = models.CharField(max_length=2000, blank=True, null=True)
    fl_acao_judicial = models.CharField(max_length=45, blank=True, null=True)
    boletos_avulso = models.ForeignKey(BoletosAvulso, models.DO_NOTHING, blank=True, null=True)
    dt_atualizacao_monetaria = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'contrato_parcelas'


class Contratos(models.Model):
    descricao = models.CharField(max_length=500, blank=True, null=True)
    dt_contrato = models.DateField(blank=True, null=True)
    vl_contrato = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vendedor = models.ForeignKey('Pessoas', models.DO_NOTHING, blank=True, null=True)
    comprador = models.ForeignKey('Pessoas', models.DO_NOTHING, related_name='contratos_comprador_set', blank=True, null=True)
    nu_parcelas = models.IntegerField(blank=True, null=True)
    vl_entrada = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    eventos = models.ForeignKey('Eventos', models.DO_NOTHING)
    tp_contrato = models.CharField(max_length=50, blank=True, null=True)
    pessoas_id_inclusao = models.ForeignKey('Pessoas', models.DO_NOTHING, db_column='pessoas_id_inclusao', related_name='contratos_pessoas_id_inclusao_set')
    dt_inclusao = models.DateTimeField(blank=True, null=True)
    honor_adimp = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    honor_inadimp = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    parcela_primeiro_pagto = models.IntegerField(blank=True, null=True)
    juros = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    contratos_id_pai = models.ForeignKey('self', models.DO_NOTHING, db_column='contratos_id_pai', blank=True, null=True)
    dt_primeira_parcela = models.DateField(blank=True, null=True)
    instrucao = models.TextField(blank=True, null=True)
    termo_percentual_contrato = models.CharField(max_length=100, blank=True, null=True)
    termo_descricao_lote = models.TextField(blank=True, null=True)
    termo_descricao_pagto = models.TextField(blank=True, null=True)
    termo_local_data = models.CharField(max_length=500, blank=True, null=True)
    termo_nomes_lote = models.CharField(max_length=500, blank=True, null=True)
    tp_contrato_boleto = models.CharField(max_length=50, blank=True, null=True)
    gerar_boleto = models.CharField(max_length=45, blank=True, null=True)
    desconto_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fl_parcelas_zerado = models.CharField(max_length=45, blank=True, null=True)
    dt_parcelas_zerado = models.DateTimeField(blank=True, null=True)
    motivo_zerado = models.CharField(max_length=150, blank=True, null=True)
    observacao_zerado = models.CharField(max_length=2000, blank=True, null=True)
    dt_acao_judicial = models.DateTimeField(blank=True, null=True)
    suspenso = models.CharField(max_length=1, blank=True, null=True)
    dt_suspensao = models.DateField(blank=True, null=True)
    dt_retorno_suspensao = models.DateField(blank=True, null=True)
    repasse = models.CharField(max_length=1, blank=True, null=True)
    status_antes_acordo = models.CharField(max_length=45, blank=True, null=True)
    fiador = models.TextField(blank=True, null=True)
    animal = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'contratos'


class DadosArquivoRetorno(models.Model):
    id = models.BigAutoField(primary_key=True)
    nosso_numero = models.CharField(max_length=45, blank=True, null=True)
    id_ocorrencia = models.CharField(max_length=45, blank=True, null=True)
    descricao = models.CharField(max_length=1000, blank=True, null=True)
    dt_banco = models.DateField(blank=True, null=True)
    dt_vencimento = models.DateField(blank=True, null=True)
    vl_boleto = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    vl_pago = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    vl_juros = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    dt_credito = models.DateField(blank=True, null=True)
    motivo_ocorrencia = models.CharField(max_length=45, blank=True, null=True)
    arquivos = models.ForeignKey(Arquivos, models.DO_NOTHING)
    nu_linha = models.IntegerField(blank=True, null=True)
    fl_processado = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dados_arquivo_retorno'


class Documentos(models.Model):
    id = models.BigAutoField(primary_key=True)
    descricao = models.CharField(max_length=500)
    file = models.CharField(max_length=100)
    contratos = models.ForeignKey(Contratos, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'documentos'


class Eventos(models.Model):
    nome = models.CharField(max_length=500, db_collation='utf8mb3_general_ci', blank=True, null=True)
    leiloeiro = models.ForeignKey('Pessoas', models.DO_NOTHING)
    dt_evento = models.DateField()
    tipo = models.CharField(max_length=200, db_collation='utf8mb3_general_ci', db_comment='(virtual, presencial, online)')

    class Meta:
        managed = True
        db_table = 'eventos'


class Haras(models.Model):
    nome = models.CharField(max_length=500)
    contato = models.CharField(max_length=500, blank=True, null=True)
    telefone = models.CharField(max_length=50, blank=True, null=True)
    proprietario = models.ForeignKey('Pessoas', models.DO_NOTHING, blank=True, null=True)
    proprietario_nome = models.CharField(max_length=500, blank=True, null=True)
    proprietario_doc = models.CharField(max_length=500, blank=True, null=True)
    rua = models.CharField(max_length=500, blank=True, null=True)
    numero = models.CharField(max_length=50, blank=True, null=True)
    complemento = models.CharField(max_length=1000, blank=True, null=True)
    bairro = models.CharField(max_length=200, blank=True, null=True)
    cidade = models.CharField(max_length=200, blank=True, null=True)
    estado = models.CharField(max_length=200, blank=True, null=True)
    cep = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'haras'


class IndiceCgj(models.Model):
    id = models.BigAutoField(primary_key=True)
    dt_indice = models.DateField()
    vl_indice = models.DecimalField(max_digits=12, decimal_places=6)

    class Meta:
        managed = True
        db_table = 'indice_cgj'


class LancamentosTed(models.Model):
    id = models.BigAutoField(primary_key=True)
    teds = models.ForeignKey('Teds', models.DO_NOTHING)
    valor = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tipo = models.CharField(max_length=200, blank=True, null=True)
    obs = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'lancamentos_ted'


class Lotes(models.Model):
    nome = models.CharField(max_length=500)
    num_registro = models.CharField(max_length=100, blank=True, null=True)
    dt_nascimento = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=500)

    class Meta:
        managed = True
        db_table = 'lotes'


class Modulo(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=45)
    nome = models.CharField(unique=True, max_length=100)
    descricao = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'modulo'


class Ocorrencias(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=500, blank=True, null=True)
    mensagem = models.TextField(blank=True, null=True)
    pessoas = models.ForeignKey('Pessoas', models.DO_NOTHING)
    contratos = models.ForeignKey(Contratos, models.DO_NOTHING)
    data_ocorrencia = models.DateTimeField(blank=True, null=True)
    contratos_id_original = models.IntegerField(blank=True, null=True)
    ligacao_feita = models.CharField(max_length=1, blank=True, null=True)
    promessa_pagamento = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ocorrencias'


class Perfil(models.Model):
    id = models.BigAutoField(primary_key=True)
    descricao = models.CharField(unique=True, max_length=45)
    dt_atualizacao = models.DateTimeField()
    fixo = models.CharField(max_length=1)

    class Meta:
        managed = True
        db_table = 'perfil'


class PerfilModulo(models.Model):
    id = models.BigAutoField(primary_key=True)
    perfil = models.ForeignKey(Perfil, models.DO_NOTHING)
    modulo = models.ForeignKey(Modulo, models.DO_NOTHING)
    visualizar = models.CharField(max_length=45, blank=True, null=True)
    adicionar = models.CharField(max_length=45, blank=True, null=True)
    editar = models.CharField(max_length=45, blank=True, null=True)
    conceder = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'perfil_modulo'


class Pessoas(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    dt_nascimento = models.DateField(blank=True, null=True)
    cpf_cnpj = models.CharField(max_length=45, blank=True, null=True)
    rg = models.CharField(max_length=45, blank=True, null=True)
    foto = models.CharField(max_length=500, blank=True, null=True)
    email = models.CharField(unique=True, max_length=200)
    password = models.CharField(max_length=200, blank=True, null=True)
    saltdb = models.CharField(max_length=100, blank=True, null=True)
    dt_ativo = models.DateTimeField(blank=True, null=True)
    apelido = models.CharField(max_length=45, blank=True, null=True)
    dt_inclusao = models.DateTimeField(blank=True, null=True)
    rua = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=45, blank=True, null=True)
    complemento = models.CharField(max_length=200, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    cep = models.CharField(max_length=45, blank=True, null=True)
    celular = models.CharField(max_length=45, blank=True, null=True)
    site = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    sobre = models.CharField(max_length=1000, blank=True, null=True)
    status = models.ForeignKey('Status', models.DO_NOTHING)
    eh_leiloeiro = models.CharField(max_length=45)
    eh_vendedor = models.CharField(max_length=45)
    eh_comprador = models.CharField(max_length=45)
    eh_user = models.CharField(max_length=45)
    telefone = models.CharField(max_length=45, blank=True, null=True)
    contato = models.CharField(max_length=200, blank=True, null=True)
    eh_admin = models.CharField(max_length=200)
    perfil = models.ForeignKey(Perfil, models.DO_NOTHING, blank=True, null=True)
    honor_adimp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    honor_inadimp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    nacionalidade = models.CharField(max_length=200, blank=True, null=True)
    supervisor = models.CharField(max_length=1, blank=True, null=True)
    operador = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pessoas'


class Protocolos(models.Model):
    id = models.BigAutoField(primary_key=True)
    protocolo = models.CharField(max_length=12)
    dt_registro = models.DateTimeField()
    cad_pessoa = models.BigIntegerField(blank=True, null=True)
    vendedor = models.CharField(max_length=100, blank=True, null=True)
    vendedor_id = models.BigIntegerField(blank=True, null=True)
    comprador = models.CharField(max_length=100, blank=True, null=True)
    comprador_id = models.BigIntegerField(blank=True, null=True)
    evento = models.CharField(max_length=500, blank=True, null=True)
    evento_id = models.BigIntegerField(blank=True, null=True)
    produto = models.CharField(max_length=100, blank=True, null=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    dt_parcela = models.DateField()
    nr_parcela = models.IntegerField()
    prazo = models.DateField()
    status = models.CharField(max_length=45, blank=True, null=True)
    setor = models.CharField(max_length=45, blank=True, null=True)
    setor_trans = models.DateTimeField(blank=True, null=True)
    trans_pessoa = models.BigIntegerField(blank=True, null=True)
    finalizado = models.DateTimeField(blank=True, null=True)
    finalizado_pessoa = models.BigIntegerField(blank=True, null=True)
    finalizado_motivo = models.CharField(max_length=500, blank=True, null=True)
    contrato_id = models.BigIntegerField(unique=True, blank=True, null=True)
    enable = models.IntegerField(blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    dt_contrato = models.DateField(blank=True, null=True)
    dt_digitalizado = models.DateField(blank=True, null=True)
    ct_verifica = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'protocolos'


class ProtocolosEventos(models.Model):
    id = models.BigAutoField(primary_key=True)  # The composite primary key (id, protocolos_id) found, that is not supported. The first column is selected.
    setor = models.CharField(max_length=45)
    ocorrencia = models.TextField(blank=True, null=True)
    data = models.DateTimeField()
    pessoas_id = models.BigIntegerField()
    protocolos = models.ForeignKey(Protocolos, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'protocolos_eventos'
        unique_together = (('id', 'protocolos'),)


class ProtocolosServicos(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=100)
    enviado = models.DateField(blank=True, null=True)
    recebido = models.DateField(blank=True, null=True)
    digitalizado = models.DateField(blank=True, null=True)
    fisico = models.DateField(blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    dt_registro = models.DateTimeField()
    dt_atualizacao = models.DateTimeField(blank=True, null=True)
    pessoa_id = models.PositiveBigIntegerField(blank=True, null=True)
    enable = models.PositiveIntegerField()

    class Meta:
        managed = True
        db_table = 'protocolos_servicos'


class ProtocolosSetor(models.Model):
    id = models.BigAutoField(primary_key=True)  # The composite primary key (id, protocolos_id) found, that is not supported. The first column is selected.
    setor = models.CharField(max_length=45)
    data = models.DateTimeField()
    pessoas_id = models.BigIntegerField()
    protocolos = models.ForeignKey(Protocolos, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'protocolos_setor'
        unique_together = (('id', 'protocolos'),)


class RodizioClientes(models.Model):
    pessoas_id = models.IntegerField(blank=True, null=True)
    tp_contrato = models.CharField(max_length=45, blank=True, null=True)
    vendedor_id = models.IntegerField(blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    id_rodizio = models.IntegerField(blank=True, null=True)
    ativo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rodizio_clientes'


class SendMail(models.Model):
    id = models.BigAutoField(primary_key=True)
    assunto = models.CharField(max_length=1000, blank=True, null=True)
    mensagem = models.TextField(blank=True, null=True)
    email_dest = models.CharField(max_length=200, blank=True, null=True)
    nome_dest = models.CharField(max_length=200, blank=True, null=True)
    email_reply = models.CharField(max_length=200, blank=True, null=True)
    nome_reply = models.CharField(max_length=200, blank=True, null=True)
    prioridade = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'send_mail'


class SendMailDestinatarios(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=200)
    enviado = models.IntegerField()
    send_mail = models.ForeignKey(SendMail, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'send_mail_destinatarios'


class Status(models.Model):
    descricao = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = True
        db_table = 'status'


class Teds(models.Model):
    id = models.BigAutoField(primary_key=True)
    pessoas_id_vendedor = models.ForeignKey(Pessoas, models.DO_NOTHING, db_column='pessoas_id_vendedor')
    pessoas_id_inclusao = models.ForeignKey(Pessoas, models.DO_NOTHING, db_column='pessoas_id_inclusao', related_name='teds_pessoas_id_inclusao_set')
    dt_inclusao = models.DateTimeField(blank=True, null=True)
    dt_ted = models.DateField(blank=True, null=True)
    vl_ted = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status_ted = models.IntegerField(blank=True, null=True)
    banco = models.IntegerField(blank=True, null=True)
    agencia = models.IntegerField(blank=True, null=True)
    dv_agencia = models.CharField(max_length=45, blank=True, null=True)
    conta = models.IntegerField(blank=True, null=True)
    dv_conta = models.CharField(max_length=45, blank=True, null=True)
    arquivos_id_remessa = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='arquivos_id_remessa', blank=True, null=True)
    nu_linha_remessa = models.IntegerField(blank=True, null=True)
    arquivos_id_retorno_previa = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='arquivos_id_retorno_previa', related_name='teds_arquivos_id_retorno_previa_set', blank=True, null=True)
    nu_linha_retorno_previa = models.IntegerField(blank=True, null=True)
    arquivos_id_retorno_processamento = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='arquivos_id_retorno_processamento', related_name='teds_arquivos_id_retorno_processamento_set', blank=True, null=True)
    nu_linha_retorno_processamento = models.IntegerField(blank=True, null=True)
    arquivos_id_retorno_consolidado = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='arquivos_id_retorno_consolidado', related_name='teds_arquivos_id_retorno_consolidado_set', blank=True, null=True)
    nu_linha_retorno_consolidado = models.IntegerField(blank=True, null=True)
    del_domc_bancario = models.IntegerField(blank=True, null=True)
    log_zerar = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'teds'
