# -*- coding: utf-8 -*-
"""EKONGA TECH INNOVATION (ETI) - Serveur Flask"""

from flask import Flask, render_template, request, jsonify, session, redirect, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

from database import init_db, save_contact, save_quote, get_all_posts, get_post_by_slug
from translations import get_translations

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eti-secret-key-2026-change-moi-en-production'
CORS(app)

ENTREPRISE = {
    "nom": "EK TECH INNOVATION",
    "sigle": "ETI",
    "slogan": "Connecter votre business au numérique",
    "fondatrice": "Ondoua EKonga Marie Ange",
    "whatsapp": "+237682542148",
    "whatsapp_cn": "+8615695115682",
    "telephone_cm": "+237 682 542 148",
    "telephone_cn": "+86 156 951 156 82",
    "email": "ekongamarie@gmail.com",
    "ville": "Douala, Cameroun",
    "annee": datetime.now().year
}

init_db()


# ============================================================
# GESTION DE LA LANGUE
# ============================================================

@app.before_request
def definir_langue():
    if 'lang' in request.args:
        session['lang'] = request.args.get('lang')
    if 'lang' not in session:
        session['lang'] = 'fr'


def t():
    return get_translations(session.get('lang', 'fr'))


@app.context_processor
def injecter_variables():
    return {
        'entreprise': ENTREPRISE,
        't': t(),
        'lang': session.get('lang', 'fr')
    }


# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def accueil():
    if session.get('lang') == 'en':
        chiffres = [
            {"valeur": "+10", "label": "Projects completed"},
            {"valeur": "100%", "label": "Satisfied clients"},
            {"valeur": "3", "label": "Sectors covered"},
            {"valeur": "24h", "label": "Response time"}
        ]
        services_apercu = [
            {"icone": "🌐", "titre": "Websites", "description": "Professional showcase websites for shops, clinics and schools."},
            {"icone": "📱", "titre": "Mobile apps", "description": "Android/iOS apps tailored to your business needs."},
            {"icone": "🖥️", "titre": "Waiting screens", "description": "Dynamic display solutions for waiting rooms."}
        ]
        temoignages = [
            {"nom": "Paul M.", "activite": "Clothing shop, Douala", "texte": "Thanks to ETI, my sales increased by 40% in 2 months.", "note": 5},
            {"nom": "Dr. Ngo Bakang", "activite": "Medical clinic", "texte": "A clear, professional site, and my patients book online.", "note": 5}
        ]
    else:
        chiffres = [
            {"valeur": "+10", "label": "Projets réalisés"},
            {"valeur": "100%", "label": "Clients satisfaits"},
            {"valeur": "3", "label": "Secteurs couverts"},
            {"valeur": "24h", "label": "Temps de réponse"}
        ]
        services_apercu = [
            {"icone": "🌐", "titre": "Sites Web", "description": "Vitrines professionnelles pour commerces, cliniques et écoles."},
            {"icone": "📱", "titre": "Applications Mobiles", "description": "Apps Android/iOS adaptées à vos besoins métier."},
            {"icone": "🖥️", "titre": "Écrans d'attente", "description": "Solutions d'affichage dynamique pour salles d'attente."}
        ]
        temoignages = [
            {"nom": "Paul M.", "activite": "Boutique de vêtements, Douala", "texte": "Grâce à ETI, mes ventes ont augmenté de 40% en 2 mois.", "note": 5},
            {"nom": "Dr. Ngo Bakang", "activite": "Cabinet médical", "texte": "Un site clair, professionnel, et mes patients prennent RDV en ligne.", "note": 5}
        ]

    return render_template('index.html', chiffres=chiffres, services=services_apercu, temoignages=temoignages)


@app.route('/services')
def services():
    if session.get('lang') == 'en':
        services_detaillees = [
            {"icone": "🌐", "titre": "Showcase Websites", "description": "A professional website to showcase your business.",
             "details": "We create modern, fast and mobile-friendly websites that reflect your brand image.",
             "livrables": ["Responsive design", "Up to 6 pages", "Contact form", "WhatsApp integration", "Basic SEO", "1h training"],
             "prix": "From 150,000 FCFA", "duree": "2 to 3 weeks"},
            {"icone": "📱", "titre": "Mobile Applications", "description": "An Android or iOS app to digitalize your activity.",
             "details": "Give your customers an app that fits in their pocket and strengthens their loyalty.",
             "livrables": ["Android/iOS app", "Intuitive interface", "Push notifications", "Training", "3 months free maintenance"],
             "prix": "On quote (from 500,000 FCFA)", "duree": "4 to 8 weeks"},
            {"icone": "🖥️", "titre": "Waiting Screens", "description": "A dynamic display system to inform your customers.",
             "details": "Turn your waiting room into a communication space.",
             "livrables": ["Customized software", "Content creation", "Installation", "Remote updates", "Staff training"],
             "prix": "From 250,000 FCFA", "duree": "1 to 2 weeks"}
        ]
        faq = [
            {"question": "How long does it take to create a website?", "reponse": "Between 2 and 4 weeks."},
            {"question": "Can I pay in installments?", "reponse": "Yes! 40% on order, 30% on delivery, 30% within 30 days."},
            {"question": "Do you offer maintenance?", "reponse": "Yes, from 15,000 FCFA/month."},
            {"question": "Do you work outside Douala?", "reponse": "Yes, throughout Cameroon and remotely."}
        ]
    else:
        services_detaillees = [
            {"icone": "🌐", "titre": "Sites Web Vitrines", "description": "Un site professionnel pour présenter votre activité.",
             "details": "Nous créons des sites modernes, rapides et adaptés aux mobiles qui reflètent l'image de votre marque.",
             "livrables": ["Design responsive", "Jusqu'à 6 pages", "Formulaire de contact", "Intégration WhatsApp", "SEO de base", "1h de formation"],
             "prix": "À partir de 150 000 FCFA", "duree": "2 à 3 semaines"},
            {"icone": "📱", "titre": "Applications Mobiles", "description": "Une application Android ou iOS pour digitaliser votre activité.",
             "details": "Offrez à vos clients une application qui tient dans leur poche et renforce leur fidélité.",
             "livrables": ["Application Android/iOS", "Interface intuitive", "Notifications push", "Formation", "3 mois de maintenance"],
             "prix": "Sur devis (à partir de 500 000 FCFA)", "duree": "4 à 8 semaines"},
            {"icone": "🖥️", "titre": "Écrans d'Attente", "description": "Un système d'affichage dynamique pour informer vos clients.",
             "details": "Transformez votre salle d'attente en espace de communication.",
             "livrables": ["Logiciel personnalisé", "Contenus", "Installation", "Mise à jour à distance", "Formation"],
             "prix": "À partir de 250 000 FCFA", "duree": "1 à 2 semaines"}
        ]
        faq = [
            {"question": "Combien de temps prend la création d'un site ?", "reponse": "Entre 2 et 4 semaines."},
            {"question": "Puis-je payer en plusieurs fois ?", "reponse": "Oui ! 40% à la commande, 30% à la livraison, 30% à 30 jours."},
            {"question": "Proposez-vous un service de maintenance ?", "reponse": "Oui, à partir de 15 000 FCFA/mois."},
            {"question": "Travaillez-vous en dehors de Douala ?", "reponse": "Oui, partout au Cameroun et à distance."}
        ]

    return render_template('services.html', services=services_detaillees, faq=faq)


@app.route('/portfolio')
def portfolio():
    if session.get('lang') == 'en':
        projets = [
            # ========== COMPLETED PROJECTS ==========
            {
                "titre": "Fairy's Beauty Salon",
                "categorie": "Showcase website + Booking",
                "type": "reel",
                "type_label_key": "portfolio_type_reel",
                "accroche": "A beauty salon could finally showcase its work and receive bookings 24/7.",
                "probleme": "The salon had no online presence. Clients had to call to learn about services, prices and to book — a real headache for a team that spent hours on the phone.",
                "solution": "A clear and elegant website that presents every service (hair, nails), lets clients browse photos of past work, and books appointments online in 2 minutes. The site displays perfectly on phone, tablet and computer.",
                "pourquoi": "Clients can now discover the salon, see styles they love and book without a single phone call.",
                "resultat": "Modern, fully responsive and tested site. An intuitive interface that makes clients want to book.",
                "technologies": ["HTML", "CSS", "JavaScript", "Bootstrap"],
                "icone": "💇‍♀️",
                "couleur": "linear-gradient(135deg, #E91E63, #C2185B)",
                "image_principale": "portfolio/fairy/main.png",
                "galerie": [
                    {"fichier": "portfolio/fairy/main.png", "legende": "Homepage"},
                    {"fichier": "portfolio/fairy/about.png", "legende": "About"},
                    {"fichier": "portfolio/fairy/services.png", "legende": "Services"},
                    {"fichier": "portfolio/fairy/booking.png", "legende": "Booking"},
                    {"fichier": "portfolio/fairy/hairstyles.png", "legende": "Hairstyle catalog"},
                    {"fichier": "portfolio/fairy/nails.png", "legende": "Nails catalog"},
                ]
            },
            {
                "titre": "Pharmacy Management System",
                "categorie": "Web Application",
                "type": "reel",
                "type_label_key": "portfolio_type_reel",
                "accroche": "A pharmacy no longer has to count its stock by hand. Everything is automated.",
                "probleme": "Manual medication tracking was error-prone: some products ran out without being noticed, others piled up unnecessarily. Staff spent precious time checking stock levels instead of serving clients.",
                "solution": "A centralized web app that manages real-time stock, alerts automatically when a medication runs low, handles supplier orders, records sales and generates reports. Three access levels (administrator, pharmacist, technician) so each person has exactly the rights they need.",
                "pourquoi": "No more unexpected stockouts. Staff focus on clients instead of spreadsheets. Every action is traced and secure.",
                "resultat": "Complete system, tested with 4 real scenarios (login, orders, sales, alerts). Reduces stock errors and secures daily operations.",
                "technologies": ["HTML5", "CSS3", "JavaScript", "Bootstrap", "PHP", "MySQL", "XAMPP"],
                "icone": "💊",
                "couleur": "linear-gradient(135deg, #2E7D32, #1B5E20)",
                "image_principale": "portfolio/pharmacy/login.png",
                "galerie": [
                    {"fichier": "portfolio/pharmacy/login.png", "legende": "Login page"},
                    {"fichier": "portfolio/pharmacy/dashboard.png", "legende": "Admin dashboard"},
                    {"fichier": "portfolio/pharmacy/orders.png", "legende": "Purchase orders"},
                    {"fichier": "portfolio/pharmacy/sales.png", "legende": "Medication sales"},
                ]
            },
            {
                "titre": "Restaurant — Restaurant Website",
                "categorie": "Modern Homepage",
                "type": "reel",
                "type_label_key": "portfolio_type_reel",
                "accroche": "A homepage that makes your mouth water within the first 3 seconds.",
                "probleme": "How do you make someone want to book a table without leaving the page? The restaurant wanted an attractive and fast digital storefront.",
                "solution": "A modern homepage with a large visual of the signature dish, a clear booking button, and a simple menu. Everything displays perfectly on any screen.",
                "pourquoi": "In 3 seconds, the visitor understands where they are, what's on offer, and how to book.",
                "resultat": "Modern and immersive design that showcases the restaurant's image.",
                "technologies": ["HTML", "CSS Grid", "Responsive design"],
                "icone": "🍽️",
                "couleur": "linear-gradient(135deg, #FF6B35, #F7931E)",
                "image_principale": "portfolio/restaurant/main.png",
                "galerie": [
                    {"fichier": "portfolio/restaurant/main.png", "legende": "Homepage"},
                ]
            },
            {
                "titre": "Modern Login Page",
                "categorie": "User Interface",
                "type": "reel",
                "type_label_key": "portfolio_type_reel",
                "accroche": "Building trust from the very first second with an elegant login page.",
                "probleme": "Many websites lose users right at the login page because of an outdated or unwelcoming design.",
                "solution": "A clean login page with two columns: the form on one side, an inspiring welcome message on the other. Colors, fonts and buttons were chosen to inspire confidence.",
                "pourquoi": "First impressions matter. A clean page reassures users and makes them want to stay.",
                "resultat": "Modern interface that shows the importance of great design from the very first seconds.",
                "technologies": ["HTML", "CSS", "UI Design"],
                "icone": "🔐",
                "couleur": "linear-gradient(135deg, #7C3AED, #4F46E5)",
                "image_principale": "portfolio/login/main.png",
                "galerie": [
                    {"fichier": "portfolio/login/main.png", "legende": "Login page"},
                ]
            },
            # ========== EXAMPLES FOR BUSINESSES ==========
            {
                "titre": "Medical Clinic with Online Booking",
                "categorie": "Healthcare Website",
                "type": "demo",
                "type_label_key": "portfolio_type_demo",
                "accroche": "No more endless phone calls. Patients book their own appointments.",
                "probleme": "The phone line is always busy, the staff loses time booking appointments, and some patients can't reach the clinic during peak hours.",
                "solution": "A medical website with online booking, automatic WhatsApp reminders, and a patient space to view appointments.",
                "pourquoi": "Every patient can book in 1 minute, even at 10 PM. Staff focus on care.",
                "resultat": "Goal: reduce calls by 60% and allow 30 extra appointments per week.",
                "technologies": ["Website", "Online booking", "WhatsApp notifications"],
                "icone": "🏥",
                "couleur": "linear-gradient(135deg, #00C48C, #0A2540)",
                "image_principale": "",
                "galerie": []
            },
            {
                "titre": "Bilingual School Connected to Parents",
                "categorie": "School Website",
                "type": "demo",
                "type_label_key": "portfolio_type_demo",
                "accroche": "Smooth communication between school and parents, at last.",
                "probleme": "Important information (events, grades, absences) doesn't flow well. Parents miss announcements and the administration keeps answering the same questions.",
                "solution": "A website centralizing school life: news, photo gallery, calendar, parent newsletter. Everyone finds what they need at the right time.",
                "pourquoi": "Better informed parents, fewer calls to the school, and a stronger school image.",
                "resultat": "Goal: +200 parents subscribed to the newsletter and simplified communication.",
                "technologies": ["Website", "News blog", "Newsletter"],
                "icone": "🎓",
                "couleur": "linear-gradient(135deg, #7C3AED, #FF7A00)",
                "image_principale": "",
                "galerie": []
            },
        ]
    else:
        projets = [
            # ========== PROJETS RÉALISÉS ==========
            {
                "titre": "Fairy's Beauty Salon",
                "categorie": "Site vitrine + Réservation",
                "type": "reel",
                "type_label_key": "portfolio_type_reel",
                "accroche": "Un salon de beauté pouvait enfin montrer ses créations et recevoir des réservations 24h/24.",
                "probleme": "Le salon n'avait aucune présence en ligne. Les clientes devaient appeler pour connaître les services, les tarifs et réserver — un vrai casse-tête pour l'équipe qui passait son temps au téléphone.",
                "solution": "Un site clair et élégant qui présente tous les services (coiffure, ongles), permet de voir les réalisations en photos et de réserver en ligne en 2 minutes. Le site s'affiche parfaitement sur téléphone, tablette et ordinateur.",
                "pourquoi": "Les clientes peuvent maintenant découvrir le salon, voir les styles qui leur plaisent et réserver sans appeler.",
                "resultat": "Site moderne, entièrement responsive et testé. Interface intuitive qui donne envie de réserver.",
                "technologies": ["HTML", "CSS", "JavaScript", "Bootstrap"],
                "icone": "💇‍♀️",
                "couleur": "linear-gradient(135deg, #E91E63, #C2185B)",
                "image_principale": "portfolio/fairy/main.png",
                "galerie": [
                    {"fichier": "portfolio/fairy/main.png", "legende": "Page d'accueil"},
                    {"fichier": "portfolio/fairy/about.png", "legende": "À propos"},
                    {"fichier": "portfolio/fairy/services.png", "legende": "Services"},
                    {"fichier": "portfolio/fairy/booking.png", "legende": "Réservation"},
                    {"fichier": "portfolio/fairy/hairstyles.png", "legende": "Catalogue coiffures"},
                    {"fichier": "portfolio/fairy/nails.png", "legende": "Catalogue ongles"},
                ]
            },
            {
                "titre": "Système de gestion de pharmacie",
                "categorie": "Application Web",
                "type": "reel",
                "type_label_key": "portfolio_type_reel",
                "accroche": "Une pharmacie n'avait plus à compter ses stocks à la main. Tout est automatisé.",
                "probleme": "Le suivi manuel des médicaments était source d'erreurs : certains produits manquaient en stock sans qu'on le remarque, d'autres s'accumulaient inutilement. Le personnel passait un temps précieux à vérifier les niveaux au lieu de servir les clients.",
                "solution": "Une application web centralisée qui gère le stock en temps réel, alerte automatiquement quand un médicament devient rare, gère les commandes auprès des fournisseurs, enregistre les ventes et génère des rapports. Trois niveaux d'accès (administrateur, pharmacien, technicien) pour que chacun ait exactement les droits dont il a besoin.",
                "pourquoi": "Fini les ruptures de stock imprévues. Le personnel se concentre sur les clients plutôt que sur les tableurs. Chaque action est tracée et sécurisée.",
                "resultat": "Système complet, testé avec 4 scénarios réels (connexion, commandes, ventes, alertes). Réduit les erreurs de stock et sécurise les opérations quotidiennes.",
                "technologies": ["HTML5", "CSS3", "JavaScript", "Bootstrap", "PHP", "MySQL", "XAMPP"],
                "icone": "💊",
                "couleur": "linear-gradient(135deg, #2E7D32, #1B5E20)",
                "image_principale": "portfolio/pharmacy/login.png",
                "galerie": [
                    {"fichier": "portfolio/pharmacy/login.png", "legende": "Page de connexion"},
                    {"fichier": "portfolio/pharmacy/dashboard.png", "legende": "Tableau de bord admin"},
                    {"fichier": "portfolio/pharmacy/orders.png", "legende": "Bons de commande"},
                    {"fichier": "portfolio/pharmacy/sales.png", "legende": "Vente de médicaments"},
                ]
            },
            {
                "titre": "Restaurant — Site de Restaurant",
                "categorie": "Page d'accueil moderne",
                "type": "reel",
                "type_label_key": "portfolio_type_reel",
                "accroche": "Une page d'accueil qui met l'eau à la bouche dès les premières secondes.",
                "probleme": "Comment donner envie de réserver une table sans que le client quitte la page ? Le restaurant voulait une vitrine digitale attractive et rapide.",
                "solution": "Une page d'accueil moderne avec un grand visuel du plat signature, un bouton de réservation bien visible et un menu clair. Le tout s'affiche parfaitement sur tous les écrans.",
                "pourquoi": "Le client comprend en 3 secondes où il est, ce qu'on propose et comment réserver.",
                "resultat": "Design moderne et immersif qui valorise l'image du restaurant.",
                "technologies": ["HTML", "CSS Grid", "Design responsive"],
                "icone": "🍽️",
                "couleur": "linear-gradient(135deg, #FF6B35, #F7931E)",
                "image_principale": "portfolio/restaurant/main.png",
                "galerie": [
                    {"fichier": "portfolio/restaurant/main.png", "legende": "Page d'accueil"},
                ]
            },
            {
                "titre": "Page de connexion moderne",
                "categorie": "Interface Utilisateur",
                "type": "reel",
                "type_label_key": "portfolio_type_reel",
                "accroche": "Redonner confiance dès la première seconde avec une page de connexion élégante.",
                "probleme": "Beaucoup de sites perdent des utilisateurs dès la page de connexion, à cause d'un design vieillissant ou peu rassurant.",
                "solution": "Une page de connexion épurée avec deux colonnes : d'un côté le formulaire, de l'autre un message d'accueil inspirant. Les couleurs, les polices et les boutons ont été choisis pour inspirer confiance.",
                "pourquoi": "La première impression est essentielle. Une page propre rassure et donne envie de rester.",
                "resultat": "Interface moderne qui montre l'importance d'un bon design dès les premières secondes.",
                "technologies": ["HTML", "CSS", "Design UI"],
                "icone": "🔐",
                "couleur": "linear-gradient(135deg, #7C3AED, #4F46E5)",
                "image_principale": "portfolio/login/main.png",
                "galerie": [
                    {"fichier": "portfolio/login/main.png", "legende": "Page de connexion"},
                ]
            },
            # ========== EXEMPLES POUR ENTREPRISES ==========
            {
                "titre": "Clinique médicale avec RDV en ligne",
                "categorie": "Site de santé",
                "type": "demo",
                "type_label_key": "portfolio_type_demo",
                "accroche": "Fini les appels téléphoniques sans fin. Les patients réservent leur rendez-vous eux-mêmes.",
                "probleme": "Le standard téléphonique est saturé, l'équipe perd du temps à prendre des rendez-vous, et certains patients n'arrivent pas à joindre la clinique aux heures de pointe.",
                "solution": "Un site médical avec un espace de réservation en ligne, des rappels automatiques par WhatsApp et un espace patient pour retrouver ses rendez-vous.",
                "pourquoi": "Chaque patient peut réserver en 1 minute, même à 22h. L'équipe se concentre sur les soins.",
                "resultat": "Objectif : réduire les appels de 60% et permettre 30 rendez-vous supplémentaires par semaine.",
                "technologies": ["Site web", "Réservation en ligne", "Notifications WhatsApp"],
                "icone": "🏥",
                "couleur": "linear-gradient(135deg, #00C48C, #0A2540)",
                "image_principale": "",
                "galerie": []
            },
            {
                "titre": "École bilingue connectée aux parents",
                "categorie": "Site scolaire",
                "type": "demo",
                "type_label_key": "portfolio_type_demo",
                "accroche": "Une communication fluide entre l'école et les parents, enfin.",
                "probleme": "Les informations importantes (événements, notes, absences) circulent mal. Les parents ratent des annonces et l'administration reçoit sans cesse les mêmes questions.",
                "solution": "Un site qui centralise toute la vie de l'école : actualités, galerie photos, calendrier, newsletter aux parents. Chacun consulte ce dont il a besoin au bon moment.",
                "pourquoi": "Les parents sont mieux informés, moins d'appels à l'école, et l'image de l'établissement se renforce.",
                "resultat": "Objectif : +200 parents inscrits à la newsletter et une communication simplifiée.",
                "technologies": ["Site web", "Blog d'actualités", "Newsletter"],
                "icone": "🎓",
                "couleur": "linear-gradient(135deg, #7C3AED, #FF7A00)",
                "image_principale": "",
                "galerie": []
            },
        ]
    return render_template('portfolio.html', projets=projets)


@app.route('/blog')
def blog():
    langue = session.get('lang', 'fr')
    articles = get_all_posts(langue)
    return render_template('blog.html', articles=articles)


@app.route('/blog/<slug>')
def article(slug):
    langue = session.get('lang', 'fr')
    article_data = get_post_by_slug(slug, langue)
    if not article_data:
        return render_template('404.html'), 404
    return render_template('article.html', article=article_data)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        email = request.form.get('email', '').strip()
        telephone = request.form.get('telephone', '').strip()
        message = request.form.get('message', '').strip()

        if not nom or not email or not message:
            return jsonify({"success": False, "message": "Champs obligatoires manquants"}), 400

        try:
            save_contact(nom, email, telephone, message)
            return jsonify({"success": True, "message": "✅ Merci ! Votre message a bien été envoyé."})
        except Exception as e:
            return jsonify({"success": False, "message": f"Erreur : {str(e)}"}), 500

    return render_template('contact.html')


@app.route('/devis', methods=['GET', 'POST'])
def devis():
    if request.method == 'POST':
        data = {
            'nom': request.form.get('nom', '').strip(),
            'email': request.form.get('email', '').strip(),
            'telephone': request.form.get('telephone', '').strip(),
            'type_projet': request.form.get('type_projet', '').strip(),
            'budget': request.form.get('budget', '').strip(),
            'delai': request.form.get('delai', '').strip(),
            'description': request.form.get('description', '').strip()
        }

        champs_requis = ['nom', 'email', 'telephone', 'type_projet', 'description']
        for champ in champs_requis:
            if not data[champ]:
                return jsonify({"success": False, "message": f"Le champ '{champ}' est obligatoire"}), 400

        try:
            save_quote(**data)
            return jsonify({"success": True, "message": "✅ Merci ! Votre demande a été reçue."})
        except Exception as e:
            return jsonify({"success": False, "message": f"Erreur : {str(e)}"}), 500

    return render_template('devis.html')


@app.route('/mentions-legales')
def mentions_legales():
    return render_template('mentions.html')


@app.route('/changer-langue/<lang>')
def changer_langue(lang):
    if lang in ['fr', 'en']:
        session['lang'] = lang
    referrer = request.referrer or '/'
    return redirect(referrer)


@app.route('/favicon.ico')
def favicon():
    """Sert le favicon à la racine du site"""
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


@app.errorhandler(404)
def page_non_trouvee(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    print("=" * 60)
    print(f"🚀 {ENTREPRISE['nom']} ({ENTREPRISE['sigle']})")
    print(f"📍 {ENTREPRISE['ville']}")
    print("=" * 60)
    print("🌐 Serveur lancé sur : http://127.0.0.1:5000")
    print("=" * 60)
    port = int(os.environ.get('PORT', 5000))
    # debug uniquement en local (pas en production)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)