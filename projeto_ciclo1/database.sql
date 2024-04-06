CREATE TABLE Usuarios (
	id SERIAL PRIMARY KEY UNIQUE,
	nome VARCHAR(255),
	email VARCHAR(255) UNIQUE,
	cpf VARCHAR(11) UNIQUE,
	senha VARCHAR,
	nivel_acesso INTEGER
);

CREATE TABLE Documentos (
	id SERIAL PRIMARY KEY UNIQUE,
	tipo VARCHAR(255),
	data_cadastro TIMESTAMP,
	id_usuario_cadastrou INTEGER REFERENCES Usuarios(id),
	imagem VARCHAR,
	tags VARCHAR[],
	data_ultima_modificacao TIMESTAMP,
	usuario_ultima_modificacao INTEGER REFERENCES Usuarios(id),
	conteudo TEXT
);

CREATE TABLE log_usuarios (
	id SERIAL PRIMARY KEY UNIQUE,
	id_usuario_modificador INTEGER REFERENCES Usuarios(id),
	id_usuario_modificado INTEGER REFERENCES Usuarios(id),
  horario TIMESTAMP,
	mensagem_log TEXT
);

CREATE TABLE log_documentos (
	id SERIAL PRIMARY KEY UNIQUE,
	id_usuario_modificador INTEGER REFERENCES Usuarios(id),
	id_documento_modificado INTEGER REFERENCES Documentos(id),
  horario TIMESTAMP,
	mensagem_log INTEGER
);

CREATE TABLE log_sistema (
	id SERIAL PRIMARY KEY UNIQUE,
	type_error VARCHAR,
  horario TIMESTAMP,
	mensagem_log TEXT
);