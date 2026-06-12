-- Criação do banco de dados, descomente a linha abaixo se for rodar tudo do zero.
-- CREATE DATABASE lpoo_projeto_daniel_cipriano_da_silva;


CREATE TABLE tb_pessoas (
    cpf VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,

    tipo_pessoa VARCHAR(20) NOT NULL CHECK (tipo_pessoa IN ('Proprietario', 'Veterinario')),
    
    inscricao_estadual VARCHAR(20),
    nome_fazenda VARCHAR(100),
    
    crmv VARCHAR(20) UNIQUE
);


CREATE TABLE tb_animais (
    brinco INTEGER PRIMARY KEY,
    raca VARCHAR(50) NOT NULL,
    data_nascimento DATE NOT NULL,
    
    tipo_animal VARCHAR(20) NOT NULL CHECK (tipo_animal IN ('Macho', 'Femea')),
    
    is_castrado BOOLEAN,
    
    estado_reprodutivo VARCHAR(20) CHECK (estado_reprodutivo IN ('Vazia', 'Inseminada', 'Prenha'))
);


CREATE TABLE tb_manejos (
    id_manejo SERIAL PRIMARY KEY,
    brinco_animal INTEGER NOT NULL,
    cpf_responsavel VARCHAR(14) NOT NULL,
    
    data_evento DATE NOT NULL,
    tipo_evento VARCHAR(20) NOT NULL CHECK (tipo_evento IN ('Inseminação', 'Diagnóstico', 'Parto', 'Aborto')),
    
    resultado_diagnostico VARCHAR(10) CHECK (resultado_diagnostico IN ('Positivo', 'Negativo')),
    
    observacao TEXT,

    FOREIGN KEY (brinco_animal) REFERENCES tb_animais(brinco) ON DELETE CASCADE,
    FOREIGN KEY (cpf_responsavel) REFERENCES tb_pessoas(cpf) ON DELETE RESTRICT
);