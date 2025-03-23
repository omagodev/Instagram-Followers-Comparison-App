from flask import Flask, render_template, request, redirect, url_for
import json
import os
import re
from datetime import datetime
import pandas as pd
import requests  

app = Flask(__name__)
DATA_FOLDER = './data'

def load_file(file_path):
    """
    Carrega um arquivo JSON que contém uma lista de dicionários com a chave "string_list_data"
    e retorna um DataFrame com as colunas:
      - user
      - href
      - timestamp
      - date
    """
    all_records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            string_list = item.get("string_list_data", [])
            if string_list:
                for s in string_list:
                    user = s.get("value")
                    ts = s.get("timestamp")
                    if user and ts:
                        try:
                            date = datetime.fromtimestamp(ts)
                        except Exception as e:
                            print(f"Erro ao converter timestamp {ts}: {e}")
                            continue
                        href = s.get("href", f"https://www.instagram.com/{user}")
                        all_records.append({
                            "user": user,
                            "href": href,
                            "timestamp": ts,
                            "date": date
                        })
            else:
                print(f"Chave 'string_list_data' não encontrada ou vazia em {file_path}.")
    return pd.DataFrame(all_records)

def load_files(selected_file):
    """
    Carrega e mescla todos os arquivos JSON que compartilham o mesmo nome base.
    Exemplo: se o arquivo selecionado for "meuarquivo_1.json", serão carregados
    "meuarquivo_1.json", "meuarquivo_2.json", etc.
    Retorna um único DataFrame com todos os registros.
    """
    base_name = re.sub(r'(_\d+)?\.json$', '', selected_file)
    all_dfs = []
    for f in os.listdir(DATA_FOLDER):
        if f.endswith('.json'):
            current_base = re.sub(r'(_\d+)?\.json$', '', f)
            if current_base == base_name:
                df = load_file(os.path.join(DATA_FOLDER, f))
                all_dfs.append(df)
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()

def profile_exists(user):
    """
    Verifica se o perfil do Instagram existe.
    Realiza uma requisição HTTP, extrai o título da página e verifica se ele contém "Página não encontrada".
    """
    url = f"https://www.instagram.com/{user}/"
    try:
        response = requests.get(url, timeout=5)
        match = re.search(r'<title>(.*?)</title>', response.text)
        if match:
            title = match.group(1)
            if "Instagram" == title:
                return False
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao verificar perfil {user}: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    all_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.json')]
    
    unique_files = []
    for f in all_files:
        base = re.sub(r'(_\d+)?\.json$', '', f)
        if (f.endswith('_1.json') or not re.search(r'_\d+\.json$', f)) and base not in unique_files:
            unique_files.append(base)
    unique_files.sort()

    if request.method == 'POST':
        file_old = request.form.get('file_old')
        file_new = request.form.get('file_new')
        if not file_old or not file_new:
            return redirect(url_for('index'))

        df_old = load_files(file_old)
        df_new = load_files(file_new)

        if not df_old.empty and not df_new.empty:
            if df_old['timestamp'].max() < df_new['timestamp'].max():
                previous_df = df_old
                current_df = df_new
            else:
                previous_df = df_new
                current_df = df_old

            previous_df['user_lower'] = previous_df['user'].str.lower().str.strip()
            current_df['user_lower'] = current_df['user'].str.lower().str.strip()

            old_users = set(previous_df['user_lower'])
            new_users = set(current_df['user_lower'])

            unfollowed_users = old_users - new_users
            unfollowed_details = []
            for user in sorted(unfollowed_users):
                registros = previous_df[previous_df['user_lower'] == user]
                if not registros.empty:
                    registro = registros.iloc[0]
                    href = registro.get("href", f"https://www.instagram.com/{registro['user']}")
                    date_str = registro["date"].strftime("%d/%m/%Y %H:%M:%S")
                    exists = profile_exists(registro['user'])
                    status = "unfollow" if exists else "excluído"
                    unfollowed_details.append({
                        "user": registro['user'],
                        "href": href,
                        "date": date_str,
                        "status": status
                    })

            new_followed_users = new_users - old_users
            new_followed_details = []
            for user in sorted(new_followed_users):
                registros = current_df[current_df['user_lower'] == user]
                if not registros.empty:
                    registro = registros.iloc[0]
                    href = registro.get("href", f"https://www.instagram.com/{registro['user']}")
                    date_str = registro["date"].strftime("%d/%m/%Y %H:%M:%S")
                    new_followed_details.append({
                        "user": registro['user'],
                        "href": href,
                        "date": date_str
                    })

            unfollow_count = len(unfollowed_details)
            new_follow_count = len(new_followed_details)

            return render_template(
                'result.html',
                file_old=file_old,
                file_new=file_new,
                total_old=len(old_users),
                total_new=len(new_users),
                unfollowed_details=unfollowed_details,
                new_followed_details=new_followed_details,
                unfollow_count=unfollow_count,
                new_follow_count=new_follow_count
            )

    return render_template('index.html', files=unique_files)

if __name__ == '__main__':
    app.run(debug=True)
