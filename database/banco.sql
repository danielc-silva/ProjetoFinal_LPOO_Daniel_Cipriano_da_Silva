CREATE DATABASE lpoo_projeto_daniel_cipriano_da_silva;

-- tabela para armazenar as pessoas
CREATE TABLE tb_pessoas (
    cpf VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,

    tipo_pessoa CHAR(1) NOT NULL CHECK (tipo_pessoa IN ('Proprietario', 'Veterinario')),
    
    -- usados quando proprietario
    inscricao_estadual VARCHAR(20),
    nome_fazenda VARCHAR(100),
    
    -- usado quando vet
    crmv VARCHAR(20) UNIQUE
);


-- tabela para armazenar os animais
CREATE TABLE tb_animais (
    brinco VARCHAR(20) PRIMARY KEY,
    raca VARCHAR(50) NOT NULL,
    data_nascimento DATE NOT NULL,
    
    tipo_animal VARCHAR(20) NOT NULL CHECK (tipo_animal IN ('Macho', 'Femea')),
    
    -- utilizado caso macho
    is_castrado BOOLEAN,
    
    -- utilizado caso femea
    estado_reprodutivo VARCHAR(20) CHECK (estado_reprodutivo IN ('Vazia', 'Inseminada', 'Prenha'))
);

-- para armazenar os manejos
CREATE TABLE tb_manejos (
    id_manejo SERIAL PRIMARY KEY,
    brinco_animal VARCHAR(20) NOT NULL,
    cpf_responsavel VARCHAR(14) NOT NULL,
    
    data_evento DATE NOT NULL,
    tipo_evento VARCHAR(20) NOT NULL CHECK (tipo_evento IN ('Inseminação', 'Diagnóstico', 'Parto', 'Aborto')),
    
    -- usar pra quando o vet fazer um toq
    resultado_diagnostico VARCHAR(10) CHECK (resultado_diagnostico IN ('Positivo', 'Negativo')),
    
    -- observações do manej
    observacao TEXT,

    FOREIGN KEY (brinco_animal) REFERENCES animais(brinco) ON DELETE CASCADE,
    FOREIGN KEY (cpf_responsavel) REFERENCES pessoas(cpf) ON DELETE RESTRICT
);


