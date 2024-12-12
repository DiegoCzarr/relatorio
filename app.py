from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import json
import plotly.utils

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Ler o arquivo Excel
            df = pd.read_excel(file, sheet_name='Teresina CNPJ')

            column_name = 'OBS'  # Nome da coluna a ser analisada
            if column_name not in df.columns:
                return "Coluna 'OBS' não encontrada no arquivo Excel.", 400

            # Contagem de valores para a tabela (todas as categorias)
            value_counts_table = df[column_name].value_counts().reset_index()
            value_counts_table.columns = ['Categoria', 'Quantidade']

            # Filtrar categorias específicas para o gráfico
            categorias_desejadas = ['Mensagem enviada', 'Não era Whatsapp', 'Demonstrou interesse', 'Não tem interesse', 'Número da contabilidade', 'contabilidade', 'Tem interesse']  # Substitua pelos nomes reais
            df_filtrado = df[df[column_name].isin(categorias_desejadas)]

            # Contagem de valores para o gráfico
            value_counts_chart = df_filtrado[column_name].value_counts().reset_index()
            value_counts_chart.columns = ['Categoria', 'Quantidade']

            # Criar gráfico interativo com Plotly
            fig = px.pie(
                value_counts_chart, 
                names='Categoria', 
                values='Quantidade', 
                title='Distribuição por Categoria (Filtrada)'
            )

            # Converter o gráfico para JSON para renderizar no HTML
            graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            return render_template(
                'index.html',
                total_rows=len(df),
                table_data=value_counts_table.values.tolist(),  # Dados completos para a tabela
                graph_json=graph_json  # Dados filtrados para o gráfico
            )

    return render_template('index.html', total_rows=None, table_data=None, graph_json=None)


if __name__ == '__main__':
    app.run(debug=True)
