# -*- coding: utf-8 -*-
"""
Gestion de la base de données SQLite pour ETI
"""

import sqlite3
import os

DOSSIER_PROJET = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DOSSIER_PROJET, 'eti_database.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL,
            telephone TEXT,
            message TEXT NOT NULL,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            statut TEXT DEFAULT 'nouveau'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL,
            telephone TEXT NOT NULL,
            type_projet TEXT NOT NULL,
            budget TEXT,
            delai TEXT,
            description TEXT NOT NULL,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            statut TEXT DEFAULT 'en_attente'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT NOT NULL,
            langue TEXT NOT NULL DEFAULT 'fr',
            titre TEXT NOT NULL,
            extrait TEXT,
            contenu TEXT NOT NULL,
            image TEXT,
            categorie TEXT,
            temps_lecture INTEGER DEFAULT 5,
            auteur TEXT DEFAULT 'Marie Ange',
            date_publication TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            publie INTEGER DEFAULT 1,
            UNIQUE(slug, langue)
        )
    ''')

    conn.commit()

    # --- Articles de démonstration ---
    cursor.execute("SELECT COUNT(*) FROM articles")
    if cursor.fetchone()[0] == 0:
        articles_demo = [
            # ============ ARTICLE 1 - FR (VEDETTE) ============
            {
                'slug': 'pourquoi-votre-commerce-doit-avoir-un-site',
                'langue': 'fr',
                'titre': 'Pourquoi votre commerce doit avoir un site web en 2026',
                'extrait': "En 2026, 7 clients sur 10 cherchent une entreprise en ligne avant de s'y rendre. Si vous n'êtes pas trouvable sur Google, vous perdez des clients chaque jour — voici pourquoi et comment y remédier.",
                'categorie': 'Digital',
                'temps_lecture': 8,
                'contenu': '''<p class="lead">Vous avez sûrement déjà vécu cette scène : un client potentiel entend parler de votre boutique, sort son téléphone, tape votre nom sur Google… et ne trouve rien. Pas de site. Pas d'horaires. Pas de prix. Juste une page Facebook abandonnée depuis 2021.</p>

<p>Et devinez ce qui se passe ensuite ? Il va voir ailleurs. Chez le concurrent qui, lui, a un site clair, à jour, avec ses prix et ses horaires affichés.</p>

<h2>La réalité du marché camerounais en 2026</h2>

<p>Le comportement des consommateurs camerounais a radicalement changé en quelques années. Voici les chiffres qui font réfléchir :</p>

<ul>
<li><strong>78% des Camerounais</strong> possèdent un smartphone et l'utilisent quotidiennement pour chercher des informations</li>
<li><strong>7 clients sur 10</strong> cherchent une entreprise en ligne <em>avant</em> de s'y rendre physiquement</li>
<li><strong>62% des recherches locales</strong> se font via Google — pas seulement sur Facebook</li>
<li><strong>85% des visiteurs</strong> quittent un site s'il met plus de 3 secondes à charger</li>
</ul>

<blockquote>
<p>« Un commerce sans site web en 2026, c'est comme une boutique sans enseigne : les clients passent devant sans même savoir qu'elle existe. »</p>
</blockquote>

<h2>7 raisons concrètes d'avoir un site web</h2>

<h3>1. Crédibilité immédiate</h3>
<p>Un site professionnel inspire confiance. Imaginez deux prestataires qui proposent le même service : l'un a un site soigné avec photos, témoignages et coordonnées claires ; l'autre n'a qu'une page Facebook. Lequel choisiriez-vous ?</p>
<p>Le site web est aujourd'hui l'équivalent digital d'une belle devanture. C'est ce qui fait la différence entre <em>« ça a l'air sérieux »</em> et <em>« je ne suis pas sûr »</em>.</p>

<h3>2. Visibilité 24h/24, 7j/7</h3>
<p>Votre boutique ferme à 18h ? Votre site, lui, reste ouvert toute la nuit. Vos clients peuvent consulter vos services, vos tarifs, vos disponibilités — même à 23h, même le dimanche, même pendant les fêtes.</p>
<p>Chaque visite sur votre site est un client potentiel qui découvre votre activité <strong>sans que vous ayez à lever le petit doigt</strong>.</p>

<h3>3. Gain de temps considérable</h3>
<p>Combien de fois par jour répondez-vous aux mêmes questions au téléphone ?</p>
<ul>
<li>« Quels sont vos horaires ? »</li>
<li>« Combien coûte votre service X ? »</li>
<li>« Est-ce que vous êtes ouverts le samedi ? »</li>
<li>« Où êtes-vous situés exactement ? »</li>
</ul>
<p>Un site web répond à toutes ces questions <strong>à votre place</strong>. Votre équipe se concentre sur les clients présents, pas sur le téléphone.</p>

<h3>4. Différenciation de la concurrence</h3>
<p>Au Cameroun, très peu de commerces ont un <strong>vrai</strong> site web professionnel. La plupart se contentent d'une page Facebook ou d'un compte Instagram.</p>
<p>En ayant un site, vous vous placez immédiatement <strong>au-dessus de 90% de vos concurrents</strong>. Et cette avance se voit dès le premier contact avec un client.</p>

<h3>5. Retour sur investissement rapide</h3>
<p>Un site vitrine professionnel coûte entre <strong>150 000 et 300 000 FCFA</strong>. Cela peut sembler élevé, mais faisons le calcul :</p>
<ul>
<li>Si votre panier moyen est de <strong>15 000 FCFA</strong></li>
<li>Et que votre site vous apporte <strong>3 nouveaux clients par mois</strong></li>
<li>Vous générez <strong>45 000 FCFA supplémentaires chaque mois</strong></li>
<li>Votre site est rentabilisé en <strong>moins de 6 mois</strong></li>
</ul>
<p>Ensuite ? Tout est bénéfice.</p>

<h3>6. Constitution d'une base de données clients</h3>
<p>Avec un simple formulaire d'inscription ou une newsletter, vous constituez progressivement un <strong>fichier clients</strong> que vous pouvez contacter directement.</p>
<p>Imaginez : vous lancez une promotion, vous envoyez un email à 500 personnes, et vous avez 30 ventes en 24h. <strong>C'est ça, le pouvoir d'une liste email.</strong></p>

<h3>7. Évolutivité</h3>
<p>Vous commencez avec un simple site vitrine ? Demain, vous pourrez y ajouter :</p>
<ul>
<li>Un catalogue de produits</li>
<li>Un blog pour partager vos conseils</li>
<li>Un système de réservation en ligne</li>
<li>Une boutique e-commerce complète</li>
</ul>
<p>Votre site <strong>grandit avec vous</strong>, sans que vous ayez à tout recommencer.</p>

<h2>« Mais un site web, c'est cher, non ? »</h2>

<p>C'est l'objection numéro 1. Et elle part d'une bonne intention : on ne veut pas investir à perte. Voyons les chiffres réels.</p>

<table>
<thead>
<tr><th>Type de site</th><th>Prix indicatif</th><th>Pour qui ?</th></tr>
</thead>
<tbody>
<tr><td>Site vitrine simple</td><td>150 000 – 250 000 FCFA</td><td>Commerces, salons, restaurants</td></tr>
<tr><td>Site vitrine + réservation</td><td>250 000 – 400 000 FCFA</td><td>Cliniques, écoles, hôtels</td></tr>
<tr><td>Application mobile</td><td>À partir de 500 000 FCFA</td><td>Entreprises avec besoins spécifiques</td></tr>
</tbody>
</table>

<p>Comparez maintenant avec le coût de la publicité traditionnelle :</p>

<ul>
<li>Un panneau publicitaire : <strong>800 000 FCFA/an</strong> — et il disparaît le jour où vous arrêtez de payer</li>
<li>Une campagne radio : <strong>500 000 FCFA</strong> pour deux semaines d'antenne</li>
<li>Des flyers distribués : <strong>100 000 FCFA</strong> jetés dès le lendemain</li>
</ul>

<p>Un site web, à l'inverse, est un <strong>investissement unique</strong> qui travaille pour vous tous les jours de l'année, sans que vous ayez à repayer.</p>

<h2>Comment se lancer concrètement ?</h2>

<h3>Étape 1 : Définir votre objectif principal</h3>
<p>Posez-vous la bonne question. Voulez-vous :</p>
<ul>
<li>Montrer vos produits et services ? → <strong>Site vitrine</strong></li>
<li>Recevoir des rendez-vous ou des commandes ? → <strong>Site + réservation</strong></li>
<li>Vendre directement en ligne ? → <strong>E-commerce</strong></li>
</ul>

<h3>Étape 2 : Rassembler vos contenus</h3>
<p>Avant de contacter un professionnel, préparez :</p>
<ul>
<li>Votre logo (ou demandez d'en créer un)</li>
<li>Des photos de qualité de vos produits ou de votre équipe</li>
<li>La liste complète de vos services avec les tarifs</li>
<li>Vos coordonnées : téléphone, WhatsApp, email, adresse</li>
</ul>

<h3>Étape 3 : Faire appel à un professionnel</h3>
<p>Beaucoup pensent pouvoir créer leur site eux-mêmes avec des outils gratuits. En réalité, un site fait maison coûte souvent plus cher en temps perdu… sans parler du résultat final qui ne reflète pas vos ambitions.</p>
<p>Faire appel à un professionnel vous garantit un site <strong>rapide, sécurisé, adapté au mobile</strong> et optimisé pour être trouvé sur Google.</p>

<h2>Le mot de la fin</h2>

<p>En 2026, un site web n'est plus un luxe. C'est le <strong>minimum vital</strong> pour toute entreprise qui veut être prise au sérieux.</p>

<p>Vos concurrents se digitalisent. Vos clients cherchent en ligne. La seule question qui reste c'est : <strong>êtes-vous visible ?</strong></p>

<div class="article-cta">
<h3>🚀 Prêt à passer à l'action ?</h3>
<p>Chez ETI, nous créons des sites web modernes pour les entreprises camerounaises, à des prix adaptés à votre réalité.</p>
<a href="/devis" class="btn-primary">Demander un devis gratuit →</a>
</div>'''
            },
            # ============ ARTICLE 1 - EN ============
            {
                'slug': 'pourquoi-votre-commerce-doit-avoir-un-site',
                'langue': 'en',
                'titre': 'Why your business needs a website in 2026',
                'extrait': "In 2026, 7 out of 10 clients search for a business online before visiting. If you can't be found on Google, you're losing customers every day — here's why and how to fix it.",
                'categorie': 'Digital',
                'temps_lecture': 8,
                'contenu': '''<p class="lead">You've probably experienced this scene: a potential client hears about your shop, pulls out their phone, types your name into Google… and finds nothing. No website. No opening hours. No prices. Just an abandoned Facebook page from 2021.</p>

<p>And guess what happens next? They go elsewhere. To the competitor who has a clear, up-to-date website with prices and hours displayed.</p>

<h2>The reality of the Cameroonian market in 2026</h2>

<p>The behavior of Cameroonian consumers has radically changed in a few years. Here are the numbers that make you think:</p>

<ul>
<li><strong>78% of Cameroonians</strong> own a smartphone and use it daily to search for information</li>
<li><strong>7 out of 10 clients</strong> search for a business online <em>before</em> visiting it</li>
<li><strong>62% of local searches</strong> happen on Google — not just Facebook</li>
<li><strong>85% of visitors</strong> leave a site if it takes more than 3 seconds to load</li>
</ul>

<blockquote>
<p>"A business without a website in 2026 is like a shop without a sign: clients walk by without even knowing it exists."</p>
</blockquote>

<h2>7 concrete reasons to have a website</h2>

<h3>1. Immediate credibility</h3>
<p>A professional website inspires trust. Imagine two providers offering the same service: one has a polished website with photos, testimonials and clear contact information; the other only has a Facebook page. Which one would you choose?</p>
<p>A website is now the digital equivalent of a beautiful storefront. It's what makes the difference between <em>"looks serious"</em> and <em>"I'm not sure"</em>.</p>

<h3>2. Visibility 24/7</h3>
<p>Your shop closes at 6 PM? Your website stays open all night. Your clients can browse your services, prices, and availability — even at 11 PM, even on Sunday, even during holidays.</p>
<p>Every visit to your site is a potential client discovering your business <strong>without you lifting a finger</strong>.</p>

<h3>3. Considerable time savings</h3>
<p>How many times a day do you answer the same questions on the phone?</p>
<ul>
<li>"What are your opening hours?"</li>
<li>"How much does service X cost?"</li>
<li>"Are you open on Saturday?"</li>
<li>"Where exactly are you located?"</li>
</ul>
<p>A website answers all these questions <strong>for you</strong>. Your team focuses on the clients in front of them, not on the phone.</p>

<h3>4. Standing out from the competition</h3>
<p>In Cameroon, very few businesses have a <strong>real</strong> professional website. Most settle for a Facebook page or an Instagram account.</p>
<p>By having a website, you immediately place yourself <strong>above 90% of your competitors</strong>. And this advantage shows from the very first contact with a client.</p>

<h3>5. Fast return on investment</h3>
<p>A professional showcase website costs between <strong>150,000 and 300,000 FCFA</strong>. That may sound high, but let's do the math:</p>
<ul>
<li>If your average sale is <strong>15,000 FCFA</strong></li>
<li>And your website brings you <strong>3 new clients per month</strong></li>
<li>You generate <strong>45,000 FCFA extra every month</strong></li>
<li>Your website pays for itself in <strong>less than 6 months</strong></li>
</ul>
<p>After that? It's all profit.</p>

<h3>6. Building a client database</h3>
<p>With a simple sign-up form or newsletter, you gradually build a <strong>client list</strong> you can contact directly.</p>
<p>Imagine: you launch a promotion, send an email to 500 people, and get 30 sales in 24 hours. <strong>That's the power of an email list.</strong></p>

<h3>7. Scalability</h3>
<p>You start with a simple showcase website? Tomorrow, you can add:</p>
<ul>
<li>A product catalog</li>
<li>A blog to share your tips</li>
<li>An online booking system</li>
<li>A full e-commerce store</li>
</ul>
<p>Your website <strong>grows with you</strong>, without having to start over.</p>

<h2>"But a website is expensive, isn't it?"</h2>

<p>That's the #1 objection. And it comes from a good place: no one wants to invest and lose money. Let's look at the real numbers.</p>

<table>
<thead>
<tr><th>Type of website</th><th>Indicative price</th><th>For whom?</th></tr>
</thead>
<tbody>
<tr><td>Simple showcase website</td><td>150,000 – 250,000 FCFA</td><td>Shops, salons, restaurants</td></tr>
<tr><td>Showcase website + booking</td><td>250,000 – 400,000 FCFA</td><td>Clinics, schools, hotels</td></tr>
<tr><td>Mobile application</td><td>From 500,000 FCFA</td><td>Businesses with specific needs</td></tr>
</tbody>
</table>

<p>Now compare with the cost of traditional advertising:</p>

<ul>
<li>A billboard: <strong>800,000 FCFA/year</strong> — and it disappears the day you stop paying</li>
<li>A radio campaign: <strong>500,000 FCFA</strong> for two weeks on air</li>
<li>Distributed flyers: <strong>100,000 FCFA</strong> thrown away the next day</li>
</ul>

<p>A website, by contrast, is a <strong>one-time investment</strong> that works for you every day of the year, without repaying.</p>

<h2>How to get started concretely?</h2>

<h3>Step 1: Define your main goal</h3>
<p>Ask yourself the right question. Do you want to:</p>
<ul>
<li>Show your products and services? → <strong>Showcase website</strong></li>
<li>Receive appointments or orders? → <strong>Website + booking</strong></li>
<li>Sell directly online? → <strong>E-commerce</strong></li>
</ul>

<h3>Step 2: Gather your content</h3>
<p>Before contacting a professional, prepare:</p>
<ul>
<li>Your logo (or ask to have one created)</li>
<li>Quality photos of your products or team</li>
<li>The full list of your services with prices</li>
<li>Your contact details: phone, WhatsApp, email, address</li>
</ul>

<h3>Step 3: Hire a professional</h3>
<p>Many think they can build their website themselves with free tools. In reality, a homemade site often costs more in lost time… not to mention the final result that doesn't reflect your ambitions.</p>
<p>Hiring a professional guarantees a <strong>fast, secure, mobile-friendly</strong> website optimized to be found on Google.</p>

<h2>Final word</h2>

<p>In 2026, a website is no longer a luxury. It's the <strong>bare minimum</strong> for any business that wants to be taken seriously.</p>

<p>Your competitors are going digital. Your clients search online. The only question that remains is: <strong>are you visible?</strong></p>

<div class="article-cta">
<h3>🚀 Ready to take action?</h3>
<p>At ETI, we build modern websites for Cameroonian businesses, at prices adapted to your reality.</p>
<a href="/devis" class="btn-primary">Request a free quote →</a>
</div>'''
            },
        ]

        for art in articles_demo:
            cursor.execute('''
                INSERT INTO articles (slug, langue, titre, extrait, contenu, categorie, temps_lecture, auteur)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                art['slug'], art['langue'], art['titre'], art['extrait'],
                art['contenu'], art['categorie'], art['temps_lecture'], 'Marie Ange'
            ))
        conn.commit()

    conn.close()
    print("✅ Base de données initialisée avec succès")


def save_contact(nom, email, telephone, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contacts (nom, email, telephone, message)
        VALUES (?, ?, ?, ?)
    ''', (nom, email, telephone, message))
    conn.commit()
    conn.close()
    print(f"📩 Nouveau contact : {nom} ({email})")


def save_quote(nom, email, telephone, type_projet, budget, delai, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO devis (nom, email, telephone, type_projet, budget, delai, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nom, email, telephone, type_projet, budget, delai, description))
    conn.commit()
    conn.close()
    print(f"💰 Nouveau devis : {nom} - {type_projet}")


def get_all_posts(langue='fr'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, slug, titre, extrait, image, categorie, temps_lecture, auteur, date_publication
        FROM articles
        WHERE publie = 1 AND langue = ?
        ORDER BY date_publication DESC
    ''', (langue,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_post_by_slug(slug, langue='fr'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM articles WHERE slug = ? AND langue = ? AND publie = 1',
        (slug, langue)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


if __name__ == '__main__':
    init_db()