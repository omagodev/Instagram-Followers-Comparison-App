# Instagram Followers Comparison App

Este aplicativo web, desenvolvido em Flask, permite comparar dois snapshots dos seguidores do Instagram, fornecidos em arquivos JSON. O app identifica quais usuários deixaram de seguir e quais começaram a seguir, diferenciando entre um unfollow real e uma conta que foi excluída (verificada pelo título da página).

## Funcionalidades

- **Carregamento e Mesclagem de Dados:**  
  Lê e combina arquivos JSON que contêm dados dos seguidores. Arquivos que compartilham o mesmo nome base (por exemplo, `meuarquivo_1.json`, `meuarquivo_2.json`) são mesclados automaticamente.

- **Comparação de Snapshots:**  
  Identifica:

  - Usuários que deixaram de seguir: presentes no snapshot antigo, mas ausentes no novo.
  - Novos seguidores: presentes no snapshot novo, mas ausentes no antigo.

- **Verificação de Perfil:**  
  Para cada usuário que deixou de seguir, o app realiza uma requisição HTTP e extrai o `<title>` da página do Instagram. Se o título contiver "Página não encontrada", o perfil é marcado como **excluído**; caso contrário, como **unfollow**.

- **Interface com Estilização:**  
  Utiliza Bootstrap para uma interface responsiva e limpa. Os status são destacados com badges (por exemplo, **Excluído** e **Unfollow**) e há contadores para o número de unfollows e novos follows.

## Requisitos

- Python 3.x
- Flask
- pandas
- requests

## Instalação

1. **Clone o Repositório:**

   ```bash
   git clone git@github.com:omagodev/Instagram-Followers-Comparison-App.git
   cd nome-do-repositorio
   ```

2. **Crie e Ative um Ambiente Virtual:**

   - No Linux/macOS:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - No Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Crie o Arquivo `requirements.txt`:**

   Crie um arquivo chamado `requirements.txt` com o seguinte conteúdo:

   ```
   Flask
   pandas
   requests
   ```

4. **Instale as Dependências:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Baixe os Dados do Instagram:**

   Acesse o seguinte link para solicitar o download dos seus dados de seguidores no Instagram:

   👉 [https://accountscenter.instagram.com/info_and_permissions/dyi/?theme=dark](https://accountscenter.instagram.com/info_and_permissions/dyi/?theme=dark)

   Após o processamento, você receberá um arquivo compactado contendo um ou mais arquivos JSON com nome como `followers_1.json`, `followers_2.json`, etc.
   Normalmente, os seguidores são divididos em lotes de 10 mil, dependendo da quantidade total.

6. **Organize os Arquivos de Dados:**

   Extraia os arquivos JSON para uma pasta chamada `data` na raiz do projeto.

   **Exemplo de Nome Base de Arquivo:**

   Se você tiver um nome base `seguidores`, os arquivos devem ser nomeados assim:

   - `seguidores_1.json`
   - `seguidores_2.json`
   - `seguidores_3.json`

   O app irá automaticamente mesclar todos os arquivos com o mesmo nome base selecionado.

## Uso

1. **Execute a Aplicação:**

   ```bash
   python app.py
   ```

2. **Acesse o App:**

   Abra o navegador e vá para:  
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

3. **Realize a Comparação:**

   - Selecione os arquivos correspondentes aos snapshots antigo e novo.
   - Clique em **Comparar**.
   - O resultado exibirá:
     - O total de seguidores em cada snapshot.
     - Uma tabela com os usuários que deixaram de seguir, com destaque para:
       - **Unfollow**: perfil ainda existe.
       - **Excluído**: perfil foi removido.
     - Uma tabela com os novos seguidores.
     - Contadores no topo de cada tabela.

## Estrutura do Projeto

```text
nome-do-repositorio/
├── app.py             # Código principal da aplicação Flask
├── data/              # Pasta contendo os arquivos JSON de seguidores
├── templates/
│   ├── index.html     # Template da página de seleção
│   └── result.html    # Template com os resultados comparativos
├── static/            # (Opcional) Arquivos estáticos (CSS, imagens, etc.)
├── requirements.txt   # Lista de dependências do projeto
└── README.md          # Este arquivo
```

## Contribuições

Contribuições são muito bem-vindas!  
Se você tiver sugestões, melhorias ou encontrar bugs, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
