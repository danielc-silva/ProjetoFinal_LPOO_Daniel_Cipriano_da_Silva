-- tabela para armazenar as pessoas
CREATE TABLE pessoas (
    cpf VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,

    tipo_pessoa CHAR(1) NOT NULL CHECK (tipo_pessoa IN ('P', 'V')),
    
    -- usados quando proprietario
    inscricao_estadual VARCHAR(20),
    nome_fazenda VARCHAR(100),
    
    -- usado quando vet
    crmv VARCHAR(20) UNIQUE
);

-- tabela para armazenar os animais
CREATE TABLE animais (
    brinco VARCHAR(20) PRIMARY KEY,
    raca VARCHAR(50) NOT NULL,
    sexo CHAR(1) NOT NULL CHECK (sexo IN ('M', 'F')),
    
    -- utilizado caso macho
    is_castrado BOOLEAN,
    
    -- utilizado caso femea
    estado_reprodutivo VARCHAR(20) CHECK (estado_reprodutivo IN ('Vazia', 'Inseminada', 'Prenha')),
    data_ultima_inseminacao DATE
);