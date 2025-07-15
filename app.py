from dotenv import load_dotenv
import os
import logging
from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')   # non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from flask import Flask, render_template, url_for, session, redirect, request

def get_locale():
    return session.get("lang", "id")  # default: Indonesia

def load_translations():
    lang = get_locale()
    try:
        with open(f'translations/{lang}.json', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
# Load .env
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv('SECRET_KEY')

    # Config
    app.config.update({
        'CSV_FILE': os.getenv('CSV_FILE', 'data/extended_data_tbc.csv'),
        'STATIC_PLOTS': os.getenv('STATIC_PLOTS', 'static/plots'),
    })

    # Ensure dirs
    Path(app.config['STATIC_PLOTS']).mkdir(parents=True, exist_ok=True)
    Path('data').mkdir(parents=True, exist_ok=True)

    @app.context_processor
    def inject_translations():
        translations = load_translations()
        return dict(_=lambda key: translations.get(key, key))
    
    @app.route("/set-language/<lang_code>")
    def set_language(lang_code):
        session['lang'] = lang_code
        next_page = request.args.get("next") or url_for('index')
        return redirect(next_page)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/')
    def index():
        translations = load_translations()
        slides_raw = translations.get("slides", [])
        slides = [
            {
                "image": url_for('static', filename="images/" + slide.get("image")),
                "title": slide.get("title"),
                "subtitle": slide.get("subtitle")
            }
            for slide in slides_raw
        ]
        layanan_list = translations.get("layanan_list", [])

        return render_template('home.html', slides=slides, layanan_list=layanan_list)

    @app.route('/informasi-publik')
    def informasi_publik():
        # 1) Load data
        df = load_data(app.config['CSV_FILE'])
        if df is None:
            return render_template('InformasiPublik.html', data=[], summary=None, plots={})

        # 2) Filter TBC & compute summary
        df_tbc = df[df['Penyakit'] == 'tbc']
        total_cases = int(df_tbc['Jumlah Kasus'].sum()) if not df_tbc.empty else 0
        summary = {'total_cases': total_cases}

        # 3) Prepare paginated table data
        data_records = df_tbc.to_dict('records')

        # 4) Run all analysis & generate plots
        run_all_analysis(df, app.config['STATIC_PLOTS'])

        # 5) Build plot URLs
        plots = {
            'bar': url_for('static', filename='plots/bar_total_per_disease.png'),
            'corr': url_for('static', filename='plots/heatmap_corr.png'),
            'year_disease': url_for('static', filename='plots/heatmap_year_disease.png'),
            'kmeans': url_for('static', filename='plots/kmeans_cluster.png'),
        }

        return render_template(
            'InformasiPublik.html',
            data=data_records,
            summary=summary,
            plots=plots
        )

    @app.route('/penyakit/tbc')
    def penyakit_tbc():
        return render_template('penyakit_tbc.html')

    @app.route('/penanggulangan')
    def penanggulangan():
        return render_template('penanggulangan-penyakit.html')

    @app.route('/kontak')
    def kontak():
        return render_template('kontak.html')
    
    @app.route('/farmasi')
    def farmasi():
        return render_template('farmasi-alkes.html')
    
    @app.route('/kebijakan-kesehatan')
    def kebijakan_kesehatan():
        return render_template('kebijakan-kesehatan.html')

    @app.route('/pantauan-krisis')
    def pantauan_krisis():
        return render_template('pantauan-krisis.html')
    
    @app.route('/tentang-kami')
    def tentang_kami():
        return render_template('tentang-kami.html')
    @app.route('/kebijakan-privasi')
    def kebijakan_privasi():
        return render_template('kebijakan-privasi.html')

    @app.route('/ketentuan-layanan')
    def ketentuan_layanan():
        return render_template('ketentuan-layanan.html')

    @app.route('/bantuan')
    def bantuan():
        return render_template('bantuan.html')


    return app


def load_data(csv_path):
    try:
        if not os.path.exists(csv_path):
            logger.error(f"File not found: {csv_path}")
            return None
        df = pd.read_csv(csv_path, sep=';')
        df['Penyakit'] = df['Penyakit'].str.lower()
        return df
    except Exception as ex:
        logger.error(f"Error loading data: {ex}")
        return None


def plot_total_per_disease(df, out_dir):
    totals = df.groupby('Penyakit')['Jumlah Kasus'].sum().sort_values()
    plt.figure(figsize=(6,4))
    sns.barplot(x=totals.values, y=totals.index)
    plt.title('Total Kasus per Penyakit')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/bar_total_per_disease.png", dpi=150)
    plt.close()


def plot_corr_heatmap(df, out_dir):
    pivot = df.pivot_table(index='Tahun', columns='Penyakit',
                           values='Jumlah Kasus', aggfunc='sum').fillna(0)
    corr = pivot.corr()
    plt.figure(figsize=(5,4))
    sns.heatmap(corr, annot=True, vmin=-1, vmax=1)
    plt.title('Korelasi Kasus Antar Penyakit')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/heatmap_corr.png", dpi=150)
    plt.close()


def plot_year_disease_heatmap(df, out_dir):
    pivot = df.pivot_table(index='Penyakit', columns='Tahun',
                           values='Jumlah Kasus', aggfunc='sum').fillna(0)
    plt.figure(figsize=(6,3))
    sns.heatmap(pivot, annot=True, fmt='g')
    plt.title('Kasus per Tahun & Penyakit')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/heatmap_year_disease.png", dpi=150)
    plt.close()


def plot_kmeans(df, out_dir, n_clusters=3):
    grouped = df.groupby(['Wilayah','Tahun'])['Jumlah Kasus'].sum().reset_index()
    X = grouped[['Tahun','Jumlah Kasus']]
    X_scaled = StandardScaler().fit_transform(X)
    labels = KMeans(n_clusters=n_clusters, random_state=0).fit_predict(X_scaled)
    grouped['Cluster'] = labels

    plt.figure(figsize=(6,4))
    sns.scatterplot(data=grouped, x='Tahun', y='Jumlah Kasus', hue='Cluster')
    plt.title(f'K-Means Clustering (k={n_clusters})')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/kmeans_cluster.png", dpi=150)
    plt.close()


def run_all_analysis(df, out_dir):
    # menerima DataFrame langsung, menghindari reload CSV berkali-kali
    for func in (plot_total_per_disease, plot_corr_heatmap,
                 plot_year_disease_heatmap, plot_kmeans):
        func(df, out_dir)


if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=(os.getenv('FLASK_ENV')=='production'),
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000))
    )
    # xxx