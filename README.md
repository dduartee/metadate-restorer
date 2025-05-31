# Restaurador de Datas (Ferramenta de Restauração de Data de Arquivos)

Este script Python identifica e restaura as datas de criação e modificação de arquivos de mídia baseado nos padrões de data/hora encontrados em seus nomes.

> [Read this documentation in English](README.md)

## Uso

```bash
python script.py <pasta> [opções]
```

Onde `script.py` é o nome do arquivo desta ferramenta (o padrão é `date_restorer.py`)

### Opções

- `-s`, `--dry-run`: Executa em modo de simulação (não altera os arquivos)
- `-v`, `--verbose`: Mostra informações detalhadas durante o processamento
- `-e`, `--ext`: Lista de extensões de arquivo para processar (ex: jpg png mp4)
- `--log`: Define o nível de detalhes do log (DEBUG, INFO, WARNING, ERROR)
- `--ignore-text`: Ignora arquivos de texto comuns (.txt, .md, .py, etc.)

### Exemplos

```bash
# Processar todos os arquivos na pasta 'fotos' e suas subpastas
python script.py ./fotos

# Simular o processamento sem alterar arquivos
python script.py ./fotos --dry-run

# Processar apenas arquivos JPG e PNG com log detalhado
python script.py ./fotos --ext jpg png --verbose

# Executar com log de depuração
python script.py ./fotos --log DEBUG

# Ignorar arquivos de texto e processar apenas arquivos de mídia
python script.py ./fotos --ignore-text
```

Onde `script.py` é o nome deste script, independente de como você o renomeie.

## Adicionando Novos Padrões de Nome de Arquivo

Para adicionar suporte para padrões adicionais de nomes de arquivo:

1. Abra o script e encontre a função `extract_date()`
2. Siga o modelo fornecido no docstring da função
3. Adicione seu novo padrão com uma regex que captura componentes de data/hora
4. Use try/except para lidar com possíveis erros de análise
5. Retorne uma tupla com (objeto_datetime, string_explicacao)

Exemplo de modelo para adicionar um novo padrão:

```python
# Padrão X: DESCRIÇÃO_DO_PADRÃO (ex., Camera_YYYYMMDD.jpg)
m = re.search(r'SEU_PADRÃO_REGEX_AQUI', filename)
if m:
    try:
        # Extrair componentes de data dos grupos regex
        # Converter para objeto datetime
        dt = datetime.strptime(string_data, 'string_formato')
        return dt, f"string de explicação com {valores_capturados}"
    except ValueError:
        pass
```

## Padrões de Arquivos Reconhecidos

O script identifica vários formatos comuns de nomes de arquivos:

- Câmeras digitais: `20181128_110755.jpg`, `IMG_20180507_192217158.jpg`
- WhatsApp: `WhatsApp Image 2018-11-27 at 18.41.02.png`, `IMG-20181225-WA0014.jpg`
- Screenshots: `Screenshot_20200101-151016_Calendar.jpg`
- Timestamps Unix: `FB_IMG_1545742864733.jpg`
- VideoCapture: `VideoCapture_20240513-155722.jpg`
- Timestamp-UUID: `1628085150288-52bceeb9-f9d1-45ec-bcef-c8e594921.jpg`
- PicsArt: `Picsart_22-09-05_08-32-31-010.jpg`
- CamScanner: `CamScanner 10-30-2022 17.02.jpg`, `CamScanner 10-30-2022 17.02_1.jpg`
- E vários outros padrões comuns de smartphones e câmeras

## Requisitos

Python 3.6 ou superior.

## Arquivos de Exemplo

O diretório `examples/` contém arquivos de exemplo de imagem e vídeo com diferentes padrões de nomeação que você pode usar para testar o script. Execute o script neste diretório para ver como ele identifica e processa vários formatos de data:

```bash
python date_restorer.py --dry-run ./examples
```

## Testes

O projeto inclui um conjunto completo de testes automatizados para validar o funcionamento do script com diferentes padrões de nomes de arquivo. Os testes estão no arquivo `test_date_restorer.py`.

### Executando os Testes

```bash
# Executar todos os testes (manuais e unitários)
python test_date_restorer.py

# Executar apenas os testes manuais com saída formatada
python test_date_restorer.py --manual

# Executar apenas os testes unitários
python test_date_restorer.py --unittest
```

### Tipos de Testes

1. **Testes Manuais**: Exibem uma saída formatada de todos os padrões de arquivo suportados e não suportados, facilitando a visualização rápida do que está funcionando.
2. **Testes Unitários**: Verificam sistematicamente cada padrão de reconhecimento e caso de falha, garantindo que o script funcione conforme esperado.

Os testes cobrem:
- Todos os 9 padrões de nome de arquivo suportados
- Validação de timestamps válidos e inválidos
- Limites temporais (desde a era Unix até a data atual)
- Casos que não devem ser reconhecidos (como IDs de mídias sociais)
- Normalização de dígitos unicode

### Adicionando Novos Testes

Se você adicionar suporte para novos padrões de nome de arquivo, é recomendado também adicionar testes correspondentes no arquivo `test_date_restorer.py`. Siga o modelo de teste existente para adicionar novos casos de teste.

## Licença

MIT License
